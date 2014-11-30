from rest_framework import serializers
from united_geonames.forms import ApiSearchForm
from united_geonames.models import UserGeoName, GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchedPlaces, \
    UnitedGeoNameSynonim, UnitedGeoName

from advanceddate.serializers import AdvancedDateNestedSerializer




class UserGeoNameSerializer(serializers.ModelSerializer):
    def from_native(self, data, z):
        # very dirty hack to allow null temporal field but still create advanced date object
        data['temporal'] = data.get('temporal', [{}])
        return super(UserGeoNameSerializer, self).from_native(data, z)
    temporal = AdvancedDateNestedSerializer()
    class Meta:
        model = UserGeoName
        fields = ('name', 'region', 'subregion', 'country', 'coordinates', 'language', 'temporal')


class UnitedGeoNameSynonimSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitedGeoNameSynonim

class UnitedGeoNameSerializer(serializers.ModelSerializer):
    synonims = UnitedGeoNameSynonimSerializer(source='get_synonyms')
    class Meta:
        model = UnitedGeoName

class GeoNamesMatchingLogMatchedPlacesSerializer(serializers.ModelSerializer):
    synonims = UnitedGeoNameSynonimSerializer(source='get_synonyms')
    matchinglogmatch_id = serializers.Field(source='get_matchinglogmatch_id')

    class Meta:
        model = GeoNamesMatchingLogMatchedPlaces
        fields = ('synonims', 'matchinglogmatch_id', 'id', 'united_geoname', 'geographical_distance',
        'ngram_distance', 'percentage', 'remark', 'best_match')


class GeoNamesMatchingLogMatchSerializer(serializers.ModelSerializer):
    matched_places = GeoNamesMatchingLogMatchedPlacesSerializer(source='matched')

    class Meta:
        model = GeoNamesMatchingLogMatch

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        form = ApiSearchForm
