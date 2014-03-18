__author__ = 'dlau'

from django.core.management.base import BaseCommand
from sxsw.models import Event
from haystack.query import SearchQuerySet

class Command(BaseCommand):

    help = "Check the searching of titles"

    option_list = BaseCommand.option_list + (
    )

    def handle(self, *args, **options):

        qualifying_events = Event.objects.filter(is_interactive=True)\
            .exclude(hash_tags__isnull=True).exclude(hash_tags__exact='')

        num_events = 0
        num_without_result = 0
        for event in qualifying_events:
            num_events = num_events + 1
            query = event.title.replace('/', ' ').replace("'", ' ').replace("&", ' ')
            sqs = SearchQuerySet().models(Event).load_all().auto_query(query)
            if len(sqs) == 0:
                num_without_result = num_without_result + 1
                print '%s does not have a search result: %s' % (event.title, query)



        print 'Punting out! All done!'

