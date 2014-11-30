# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UnitedGeoName'
        db.create_table('united_geonames_unitedgeoname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('united_geonames', ['UnitedGeoName'])

        # Adding model 'UnitedGeoNameSynonim'
        db.create_table('united_geonames_unitedgeonamesynonim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('united_geoname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['united_geonames.UnitedGeoName'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('united_geonames', ['UnitedGeoNameSynonim'])


    def backwards(self, orm):
        
        # Deleting model 'UnitedGeoName'
        db.delete_table('united_geonames_unitedgeoname')

        # Deleting model 'UnitedGeoNameSynonim'
        db.delete_table('united_geonames_unitedgeonamesynonim')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'united_geonames.unitedgeoname': {
            'Meta': {'object_name': 'UnitedGeoName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'united_geonames.unitedgeonamesynonim': {
            'Meta': {'object_name': 'UnitedGeoNameSynonim'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'united_geoname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['united_geonames.UnitedGeoName']", 'null': 'True'})
        }
    }

    complete_apps = ['united_geonames']
