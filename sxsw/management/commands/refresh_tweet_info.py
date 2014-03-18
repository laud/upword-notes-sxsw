__author__ = 'dlau'

from django.core.management.base import BaseCommand, make_option
from django.db.models import Sum
from sxsw.models import Event
from birdy.twitter import AppClient, TwitterRateLimitError

import sys

api_keys = [
    # UpWord Notes SXSW @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 1 @upwordsxsw2
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 2 @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 3 @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 4 @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 5 @upwordsxsw2
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 6 @upwordsxsw2
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 7 @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 8 @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    },
    # UpWord Notes SXSW 9 @dlauzzz
    {
        'consumer_key' : 'SECRET_KEY', #This should really be an environment variable...but HACK!
        'consumer_secret' : 'SECRET_SECRET', #This should really be an environment variable...but HACK!
    }
]

class Command(BaseCommand):

    help = "Refresh twitter info for events"

    option_list = BaseCommand.option_list + (
        make_option('--debug', action='store_true', dest='debug', default=False,
                    help='Don\'t actually update twitter info. Just do a dry run'),
    )

    def handle(self, *args, **options):
        debug = options['debug']
        print 'Debug mode: ' + ('On' if debug else 'Off')

        clients = []
        for api_key in api_keys:
            client = AppClient(api_key['consumer_key'], api_key['consumer_secret'])
            access_token = client.get_access_token()
            client = AppClient(api_key['consumer_key'], api_key['consumer_secret'], access_token)
            clients.append(client)

        self.grab_qualifying_sxsw_events(clients)
        print 'Punting out! All done!'

    def grab_qualifying_sxsw_events(self, twitter_clients):
        num_notes = Event.objects.filter(is_interactive=True)\
            .exclude(hash_tags__isnull=True).exclude(hash_tags__exact='').aggregate(Sum('num_notes'))['num_notes__sum']
        qualifying_events = Event.objects.filter(is_interactive=True)\
            .exclude(hash_tags__isnull=True).exclude(hash_tags__exact='')

        resources = []
        for client in twitter_clients:
            resource = client.api.search.tweets
            resources.append(resource)

        cumulative_num_notes = 0
        num_refreshed = 0
        num_rate_limited = 0
        num_error = 0
        count = 0
        for event in qualifying_events:
            search_query =  event.get_twitter_search_query()

            try:
                resource = resources[count % len(resources)]
                response = resource.get(q=search_query, count=100)
                event.num_notes = len(response.data.statuses)
                cumulative_num_notes = cumulative_num_notes + event.num_notes
                event.save()
                num_refreshed = num_refreshed + 1
                print event.title.encode('utf8'), search_query.encode('utf8'), event.num_notes
            except TwitterRateLimitError, e:
                print search_query, 'Rate Limited'
                num_rate_limited = num_rate_limited + 1
            except Exception, e:
                print search_query, 'General Exception'
                print e
                print sys.exc_traceback.tb_lineno
                num_error = num_error + 1
            finally:
                count = count + 1

        print 'Done Statistics, num refreshed: %d, num rate limited: %d, num error: %d' % \
              (num_refreshed, num_rate_limited, num_error)
        print 'Num New Notes: %d, Old Num Notes: %d, Num Diff: %d' % (cumulative_num_notes, num_notes, cumulative_num_notes - num_notes)
