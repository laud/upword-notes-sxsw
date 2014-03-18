from django.db import models
from django.core.urlresolvers import reverse
import urllib

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    sxsw_id = models.CharField(max_length=128)
    title = models.CharField(max_length=512)
    details_url = models.CharField(max_length=512)
    is_interactive = models.BooleanField(default=False)
    is_film = models.BooleanField(default=False)
    is_music = models.BooleanField(default=False)
    event_type = models.CharField(max_length=256)
    category = models.CharField(max_length=256, blank=True)
    theme = models.CharField(max_length=256, blank=True)
    location_venue = models.CharField(max_length=256)
    location_detail = models.CharField(max_length=256, blank=True)
    location_address = models.CharField(max_length=256, blank=True)
    start_time = models.DateTimeField()
    time_range = models.CharField(max_length=256, blank=True)
    hash_tags = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_recommended = models.BooleanField(default=False)
    recommended_for = models.CharField(max_length=256, blank=True)
    num_notes = models.IntegerField(default=0)
    presenters_string = None

    @property
    def presenters_string(self):
        return ', '.join([presenter.name for presenter in self.presenter_event.all()])

    def description_link(self):
        return 'http://schedule.sxsw.com' + self.details_url

    def description_anchor(self):
        link = self.description_link()
        return """<a href="%s">Details</a>""" % link
    description_anchor.allow_tags = True

    def set_recommended(self):
        link_name = 'Un-Recommend' if self.is_recommended else 'Recommend'
        return ("<a href='%s'>" + link_name + "</a>") % reverse("sxsw.views.set_recommended", args=[self.pk])
    set_recommended.allow_tags = True

    def get_main_hashtag(self):
        hash_tag = self.hash_tags.split()[:1][0]
        if '#' not in hash_tag:
            hash_tag = self.hash_tags[self.hash_tags.rfind('#'):].split()[0]
        return hash_tag

    twitter_query_template = '%s #upwordsxsw filter:links'

    def get_twitter_search_query(self):
        return self.twitter_query_template % self.get_main_hashtag()

    def get_twitter_hashtag_url(self):
        return 'https://twitter.com/search?q=%s&src=hash' % urllib.quote_plus(self.get_main_hashtag())

    def get_twitter_search_url(self, encode=True):
        search_query = self.twitter_query_template % self.get_main_hashtag()
        if encode:
            search_query = urllib.quote_plus(search_query)
        twitter_search_url = 'https://twitter.com/search/?q=%s&f=realtime' % search_query

        return twitter_search_url

    def __unicode__(self):
        return self.title

class Presenter(models.Model):
    sxsw_presenter_id = models.CharField(max_length=512)
    name = models.CharField(max_length=256)
    image = models.TextField(blank=True)
    title = models.CharField(max_length=256, blank=True)
    company = models.CharField(max_length=256, blank=True)
    bio = models.TextField(blank=True)
    event = models.ForeignKey(Event, related_name='presenter_event', null=True, blank=True)

    def thumbnail(self):
        if self.image:
            return """<a href="%s"><img border="0" src="%s" height="40" /></a>""" % (
                (self.image, self.image))
        else:
            return """No image"""
    thumbnail.allow_tags = True

    def __unicode__(self):
        return self.name