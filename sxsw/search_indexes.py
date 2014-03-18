__author__ = 'dlau'
from haystack import indexes
from sxsw.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    start_time = indexes.DateTimeField(model_attr='start_time')
    num_notes = indexes.IntegerField(model_attr='num_notes', boost=1.125)
    title_auto = indexes.NgramField(model_attr='title')
    title = indexes.CharField(model_attr='title')


    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_interactive=True)\
            .exclude(title__startswith='Book Signing')\
            .exclude(hash_tags='#nextstage').exclude(hash_tags='#sxgood')\
            .exclude(hash_tags__isnull=True).exclude(hash_tags__exact='')