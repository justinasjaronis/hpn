# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'UnitedGeoNameSynonim.subregion'
        db.alter_column('united_geonames_unitedgeonamesynonim', 'subregion', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))


    def backwards(self, orm):
        
        # Changing field 'UnitedGeoNameSynonim.subregion'
        db.alter_column('united_geonames_unitedgeonamesynonim', 'subregion', self.gf('django.db.models.fields.CharField')(default='', max_length=300))


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'united_geonames.geonamesmatchinglogmatch': {
            'Meta': {'ordering': "['-matching_index']", 'object_name': 'GeoNamesMatchingLogMatch'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matching_index': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_alternatives': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'united_geonames.geonamesmatchinglogmatchedplaces': {
            'Meta': {'object_name': 'GeoNamesMatchingLogMatchedPlaces'},
            'best_match': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geographical_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matchinglogmatch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matched'", 'null': 'True', 'to': "orm['united_geonames.GeoNamesMatchingLogMatch']"}),
            'ngram_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'united_geoname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['united_geonames.UnitedGeoName']", 'null': 'True', 'blank': 'True'})
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
            'region': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'subregion': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'synonim_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'synonim_content_type_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'synonim_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'synonim_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'united_geoname': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'geonames'", 'null': 'True', 'to': "orm['united_geonames.UnitedGeoName']"})
        }
    }

    complete_apps = ['united_geonames']
