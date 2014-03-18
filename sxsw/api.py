__author__ = 'dlau'

from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.throttle import BaseThrottle
from tastypie.resources import ModelResource, ALL
from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization

from haystack.query import SearchQuerySet
from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Sum
from tastypie.utils import trailing_slash
from models import Event, Tag, Presenter
from urlparse import urljoin

class TagResource(ModelResource):

    class Meta:
        queryset = Tag.objects.all()
        allowed_methods = ['get']
        fields = ['name']
        filtering = {}
        cache = SimpleCache()
        throttle = BaseThrottle()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class PresenterResource(ModelResource):
    event = fields.ForeignKey('sxsw.api.EventResource', 'event')

    class Meta:
        queryset = Presenter.objects.all()
        allowed_methods = ['get']
        fields = ['name', 'company']
        filtering = {}
        cache = SimpleCache()
        throttle = BaseThrottle()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

class EventResource(ModelResource):
    # tags = fields.ToManyField(TagResource, 'tags', full=True)
    presenter = fields.ToManyField(PresenterResource, 'presenter_event', full=True)
    twitter_url = fields.CharField()
    hashtag_url = fields.CharField()

    class Meta:
        queryset = Event.objects.filter(is_interactive=True).exclude(title__startswith='Book Signing')\
            .exclude(hash_tags__isnull=True).exclude(hash_tags__exact='').order_by('start_time')
        allowed_methods = ['get']
        fields = ['title', 'details_url', 'theme', 'start_time', 'hash_tags', 'description', 'num_notes']
        filtering = {'num_notes' : ALL}
        ordering = ['num_notes']
        cache = SimpleCache()
        throttle = BaseThrottle()
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()

    def dehydrate_twitter_url(self, bundle):
        if len(bundle.obj.hash_tags) > 0:
            return bundle.obj.get_twitter_search_url()
        return None

    def dehydrate_hashtag_url(self, bundle):
        return bundle.obj.get_twitter_hashtag_url()

    def dehydrate_details_url(self, bundle):
        raw_details_url = bundle.obj.details_url
        if 'http://www.upwordnotes.com' in raw_details_url:
            raw_details_url = None
        else:
            raw_details_url = urljoin('http://schedule.sxsw.com', raw_details_url)
        return raw_details_url

    def get_object_list(self, request):
        event_resource_obj_list = super(EventResource, self).get_object_list(request)

        if request.GET.get('suggested'):
            event_resource_obj_list = Event.objects.filter(is_interactive=True).filter(num_notes__gt=1).order_by('?')[:3]

        return event_resource_obj_list

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            url(r"^(?P<resource_name>%s)/auto%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_autocomplete'), name="api_get_autocomplete"),
            url(r"^(?P<resource_name>%s)/browse%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_browse'), name="api_get_browse"),
        ]

    search_page_size_default = 20
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        query = request.GET.get('q', '').replace('/', ' ').replace("'", ' ').replace("&", ' ')
        showAll = request.GET.get('showAll') in ['true', '1']

        sqs = SearchQuerySet().models(Event).load_all().auto_query(query)
        total_search_count =  len(sqs)
        if total_search_count > 1 and not showAll:
            sqs = sqs.filter(num_notes__gt=0)
        hidden_events_count = total_search_count - len(sqs)
        total_num_notes = sum([result.object.num_notes for result in sqs])
        paginator = Paginator(sqs, self.search_page_size_default)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            page = None

        objects = []
        if page:
            for result in page.object_list:
                bundle = self.build_bundle(obj=result.object, request=request)
                bundle = self.full_dehydrate(bundle)
                objects.append(bundle)

        num_pages = sqs._result_count / self.search_page_size_default
        if sqs._result_count % self.search_page_size_default > 0:
            num_pages = num_pages + 1

        object_list = {
            'objects': objects,
            'meta' : {
                'limit' : self.search_page_size_default,
                'pages' : num_pages,
                'total_count' : total_search_count,
                'hidden_count' : hidden_events_count,
                'count' : len(sqs),
                'page' : int(request.GET.get('page', 1)),
                'total_num_notes' : total_num_notes
            }
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def get_autocomplete(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        # sqs = SearchQuerySet().models(Event).autocomplete(title_auto=request.GET.get('q', ''))
        query = request.GET.get('q', '').replace('/', ' ').replace("'", ' ').replace("&", ' ')
        sqs = SearchQuerySet().models(Event).filter(title__startswith=query)[:10]
        suggestions = [result.object.title for result in sqs]

        object_list = {
            'query' : request.GET.get('q', ''),
            'suggestions' : list(set(suggestions)),
            'meta' : {
                'total_count' : len(sqs),
            }
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def get_browse(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        events = Event.objects.filter(is_interactive=True).exclude(hash_tags='#nextstage').exclude(hash_tags='#sxgood')\
            .exclude(title__startswith='Book Signing').exclude(hash_tags__isnull=True).exclude(hash_tags__exact='').filter(num_notes__gt=0).order_by('-start_time', '-num_notes')
        total_num_notes = Event.objects.filter(is_interactive=True).exclude(hash_tags='#nextstage').exclude(hash_tags='#sxgood')\
            .exclude(title__startswith='Book Signing').exclude(hash_tags__isnull=True).exclude(hash_tags__exact='').aggregate(Sum('num_notes'))['num_notes__sum']
        total_num_events =  len(events)
        paginator = Paginator(events, self.search_page_size_default)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            page = None

        objects = []
        count = 0
        if page:
            for result in page.object_list:
                bundle = self.build_bundle(obj=result, request=request)
                bundle = self.full_dehydrate(bundle)
                objects.append(bundle)
            count = len(page.object_list)

        num_pages = total_num_events / self.search_page_size_default
        if total_num_events % self.search_page_size_default > 0:
            num_pages = num_pages + 1

        object_list = {
            'objects': objects,
            'meta' : {
                'limit' : self.search_page_size_default,
                'pages' : num_pages,
                'total_count' : total_num_events,
                'count' : count,
                'page' : int(request.GET.get('page', 1)),
                'total_num_notes' : total_num_notes
            }
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

