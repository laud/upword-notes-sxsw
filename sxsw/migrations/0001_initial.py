# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'sxsw_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'sxsw', ['Tag'])

        # Adding model 'Event'
        db.create_table(u'sxsw_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sxsw_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('details_url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('is_interactive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_film', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_music', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('location_venue', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('location_detail', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('location_address', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateField')()),
            ('time_range', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('hash_tags', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sxsw', ['Event'])

        # Adding M2M table for field tags on 'Event'
        m2m_table_name = db.shorten_name(u'sxsw_event_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'sxsw.event'], null=False)),
            ('tag', models.ForeignKey(orm[u'sxsw.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'tag_id'])

        # Adding model 'Presenter'
        db.create_table(u'sxsw_presenter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sxsw_presenter_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('image', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='presenter_event', null=True, to=orm['sxsw.Event'])),
        ))
        db.send_create_signal(u'sxsw', ['Presenter'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'sxsw_tag')

        # Deleting model 'Event'
        db.delete_table(u'sxsw_event')

        # Removing M2M table for field tags on 'Event'
        db.delete_table(db.shorten_name(u'sxsw_event_tags'))

        # Deleting model 'Presenter'
        db.delete_table(u'sxsw_presenter')


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
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'location_detail': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'location_venue': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'start_time': ('django.db.models.fields.DateField', [], {}),
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