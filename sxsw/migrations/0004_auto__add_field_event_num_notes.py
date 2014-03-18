# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.num_notes'
        db.add_column(u'sxsw_event', 'num_notes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.num_notes'
        db.delete_column(u'sxsw_event', 'num_notes')


    models = {
        u'sxsw.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details_url': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'hash_tags': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_film': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_interactive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_music': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'location_detail': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'location_venue': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'num_notes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'recommended_for': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'sxsw_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sxsw.Tag']", 'symmetrical': 'False'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'time_range': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'sxsw.presenter': {
            'Meta': {'object_name': 'Presenter'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'presenter_event'", 'null': 'True', 'to': u"orm['sxsw.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'sxsw_presenter_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'sxsw.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['sxsw']