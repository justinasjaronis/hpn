# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GeoNamesMatchingLogMatch'
        db.create_table('united_geonames_geonamesmatchinglogmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('united_geoname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['united_geonames.UnitedGeoName'])),
            ('geographical_distance', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ngram_distance', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('percentage', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('united_geonames', ['GeoNamesMatchingLogMatch'])


    def backwards(self, orm):
        
        # Deleting model 'GeoNamesMatchingLogMatch'
        db.delete_table('united_geonames_geonamesmatchinglogmatch')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'united_geonames.geonamesmatchinglogmatch': {
            'Meta': {'object_name': 'GeoNamesMatchingLogMatch'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'geographical_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ngram_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'united_geoname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['united_geonames.UnitedGeoName']"})
        },
        'united_geonames.unitedgeoname': {
            'Meta': {'object_name': 'UnitedGeoName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'united_geonames.unitedgeonamesynonim': {
            'Meta': {'object_name': 'UnitedGeoNameSynonim'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'coordinates': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'synonim_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'synonim_content_type_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'synonim_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'united_geoname': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'geonames'", 'null': 'True', 'to': "orm['united_geonames.UnitedGeoName']"})
        }
    }

    complete_apps = ['united_geonames']
