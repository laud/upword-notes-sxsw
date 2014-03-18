from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from tastypie.api import Api
from sxsw.api import PresenterResource, EventResource, TagResource
from django.views.generic import RedirectView, TemplateView
import settings

# API resources
v1_api = Api(api_name='v1')
v1_api.register(PresenterResource())
v1_api.register(EventResource())
v1_api.register(TagResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sxswtweets.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(v1_api.urls)),

    url(r'^sxsw/', include('sxsw.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon\.ico$', RedirectView.as_view(url='http://' + settings.CLOUDFRONT_DOMAIN + settings.STATIC_DIRECTORY+ 'favicon.ico')),

    url(r'^$', TemplateView.as_view(template_name='index.html')),
)

# if settings.DEBUG:
urlpatterns += patterns('',
    url(r'^search/', include('haystack.urls')),
    url(r'^autocomplete/', TemplateView.as_view(template_name='search/autocomplete.html'))
)

print settings.STATIC_URL + 'favicon.ico'