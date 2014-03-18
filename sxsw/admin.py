from django.contrib import admin
from models import Event, Presenter, Tag

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'sxsw_id', 'title', 'num_notes', 'description_anchor', 'is_interactive', 'is_film', 'is_music', 'hash_tags', 'event_type', 'start_time', 'set_recommended', 'recommended_for']
    date_hierarchy = 'start_time'
    search_fields = ['title']
    ordering = ['start_time', 'id']

class PresenterAdmin(admin.ModelAdmin):
    list_display = ['id', 'sxsw_presenter_id', 'name', 'title', 'company', 'thumbnail']
    search_fields = ['name']

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(Event, EventAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(Tag, TagAdmin)