__author__ = 'dlau'

from django.core.management.base import BaseCommand
from scraper import scraper

class Command(BaseCommand):

    help = "Scrape SXSW site for events"

    option_list = BaseCommand.option_list + (
    )

    def handle(self, *args, **options):
        scraper.fetch_sxsw_event_list()
        print 'Punting out! All done!'

