from admin_extensions.forms import AutoCompleteModelForm

from gmf.fields import GMField

from django.forms import ModelForm

from django.contrib.gis import forms

from .models import UnitedGeoNameSynonim, GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchedPlaces, UserGeoName, Database

from ajax_select.fields import AutoCompleteSelectField
import autocomplete_light


class DatabaseForm(ModelForm):
    class Meta:
        model = Database

class UnitedGeoNameSynonimForm(ModelForm):
    coordinates = GMField()

    class Meta:
        model = UnitedGeoNameSynonim


class UserUnitedGeoNameSynonimForm(ModelForm):
    class Meta:
        model = UnitedGeoNameSynonim


autocomplete_light.autodiscover()

class GeoNamesMatchingLogMatchedPlacesForm(AutoCompleteModelForm):
    united_geoname = AutoCompleteSelectField('united_geo_name', required=False)


class UserGeoNameForm(ModelForm):
    coordinates = GMField()
    class Meta:
        model = UserGeoName
        exclude = ('user')

class UserGeoNameFormWithoutMap(ModelForm):
    name = forms.CharField(required=True)
    class Meta:
        model = UserGeoName
        exclude = ('user')


class GeoNamesMatchingLogMatchForm(ModelForm):
    object_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = GeoNamesMatchingLogMatch
        exclude = ('display_for_users', 'number_of_alternatives', 'content_type')


class GeoNamesMatchingLogMatchedPlacesFormUser(autocomplete_light.ModelForm):
    united_geoname = autocomplete_light.ModelChoiceField('UnitedGeoNameAutocomplete')
    remark = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}), required=False)

    class Meta:
        model = GeoNamesMatchingLogMatchedPlaces
        exclude = ('matchinglogmatch', )

class ApiSearchForm(forms.Form):
    name = forms.CharField()
    region = forms.CharField()
    subregion = forms.CharField()
    country = forms.CharField()