#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'dlau'

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from sxsw.models import Event, Tag, Presenter
from datetime import datetime
from pytz import timezone


def fetch_sxsw_event_list():

    for i in xrange(6, 17): # should be March 6th - 16th  xrange(6, 17)
        url = 'http://schedule.sxsw.com/?day=%d' % i

        d = pq(url=url)
        for event in (d('[id^="cell_event_"]')):
            d = d(event)
            sxsw_event = {}

            title = d('div.conf-desc a').html()
            sxsw_event['title'] = title

            detail_url = d('div.conf-desc a').attr('href')
            sxsw_event['detail_url'] = detail_url

            sxsw_id = detail_url[detail_url.rfind('_')+1:]
            sxsw_event['id'] = sxsw_id

            conference_type = []
            for conference_type_span in  d('div.conf-desc div.conf-dots').find('span'):
                conference_type.append(d(conference_type_span).attr('title'))
            sxsw_event['conference_type'] = conference_type

            event_type = d('div.col2 div.type b').html()
            sxsw_event['event_type'] = event_type

            category = d('div.col2 div.type i').html()
            sxsw_event['category'] = category

            theme = d('div.col2 div.type a').html()
            sxsw_event['theme'] = theme

            sxsw_event['location'] = {}
            location = d('div.col3 div.location')
            if location('i'):
                sxsw_event['location']['location_main'] = location.html()[:location.html().rfind('<br')].strip()
                sxsw_event['location']['location_detail'] = location('i').html().strip()
            else:
                sxsw_event['location']['location_main'] = location.html().strip()

            date_time = d('div.col4 div.date_time').html()
            sxsw_event['date_time'] = {}
            sxsw_event['date_time']['date'] = i
            sxsw_event['date_time']['time_range'] = date_time.strip()

            if fetch_sxsw_event_details(detail_url, sxsw_event):
                upsert_sxsw_event(sxsw_event)

            print sxsw_event

def fetch_sxsw_event_details(event_url, sxsw_event_dict):
    try:
        d = pq(url='http://schedule.sxsw.com' + event_url)

        hash_tag = d('div.data div.meta p')
        if hash_tag.html() is not None:
            sxsw_event_dict['hash_tags'] = hash_tag.html().lstrip('#sxsw').strip()

        # STRIP OUT the part that reads "ATTENTION: You must sign up to attend this workshop", wherever that occurs
        description = d('div.data div.block')
        if description is not None:
            if description('p').html() is not None and 'ATTENTION:' in description('p').html():
                description = description.remove('p:first-child')
            if description.html() is not None:
                description_text = BeautifulSoup(description.html()).get_text()
                sxsw_event_dict['description_text'] = description_text

        presenters_array = []
        presenters = d('div.data div.presenter')
        for presenter in presenters:
            presenter = d(presenter)
            presenter_img = presenter('div.presenters_image img').attr('src')
            presenter_name = presenter('.pres_name').html().strip()
            presenter_title = presenter('.pres_title').html()
            presenter_company = presenter('.pres_company').html()
            presenter_bio = BeautifulSoup(presenter('.pres_bio').html()).get_text()

            presenter = {
                'img' : presenter_img,
                'name' : presenter_name,
                'title' : presenter_title,
                'company' : presenter_company,
                'bio' : presenter_bio
            }
            presenters_array.append(presenter)

        if len(presenters_array) > 0:
            sxsw_event_dict['presenters'] = presenters_array


        location_address =  d('div#sidebar .address').html()
        sxsw_event_dict['location']['address'] = location_address

        tags = []
        for tag in d('div#sidebar a.tag'):
            tags.append(d(tag).html())
        sxsw_event_dict['tags'] = tags
        return True

    except Exception, e:
        print 'Error for url: ' + event_url, e
        print '>!!! REVISIT'
        return False

def upsert_sxsw_event(info):
    event = Event.objects.filter(sxsw_id = info.get('id')).first()
    if event is None:
        event = Event()
        event.sxsw_id = info.get('id')

    event.title = info.get('title', '') or ''
    event.details_url = info.get('detail_url', '') or ''
    conference_type = info.get('conference_type', [])
    event.is_interactive = 'Interactive' in conference_type
    event.is_film = 'Film' in conference_type
    event.is_music = 'Music' in conference_type
    event.event_type = info.get('event_type', '') or ''
    event.category = info.get('category', '') or ''
    event.theme = info.get('theme', '') or ''
    event.location_venue = info['location'].get('location_main', '') or ''
    event.location_detail = info['location'].get('location_detail', '') or ''
    event.location_address = info['location'].get('address', '') or ''

    march_date = info['date_time']['date']
    event.time_range = info['date_time'].get('time_range', '') or ''
    if len(event.time_range.strip()) > 0:
        start_time = event.time_range[:event.time_range.find('-')].strip()
        date = datetime.strptime('%d Mar 2014 %s' % (march_date, start_time), '%d %b %Y %I:%M%p')
    else:
        date = datetime.strptime('%d Mar 2014' % march_date, '%d %b %Y')
    central = timezone('US/Central')
    event.start_time = central.localize(date)

    event.hash_tags = info.get('hash_tags', '') or ''
    event.description = info.get('description_text', '') or ''
    event.save()

    for presenter_info in info.get('presenters', []):
        presenter_id = presenter_info.get('name') + event.sxsw_id
        presenter = Presenter.objects.filter(sxsw_presenter_id = presenter_id).first()
        if presenter is None:
            presenter = Presenter()
            presenter.sxsw_presenter_id = presenter_id
        presenter.name = presenter_info.get('name', '') or ''
        presenter.image = presenter_info.get('img', '') or ''
        presenter.title = presenter_info.get('title', '') or ''
        presenter.company = presenter_info.get('company', '') or ''
        presenter.bio = presenter_info.get('bio', '') or ''
        presenter.event = event
        presenter.save()

    for tag_name in info.get('tags', []):
        tag = Tag.objects.filter(name=tag_name).first()
        if tag is None:
            tag = Tag()
            tag.name = tag_name
            tag.save()
        event.tags.add(tag)


def main():
    fetch_sxsw_event_list()

if __name__ == '__main__':
   main()