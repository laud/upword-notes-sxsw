__author__ = 'dlau'

from django.conf.urls import patterns, url
from sxsw.views import set_recommended

urlpatterns = patterns('',
                      url(r"^mark_recommended/(\d*)/$", set_recommended),

)