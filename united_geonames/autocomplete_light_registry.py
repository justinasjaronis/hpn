from .models import UnitedGeoName
import autocomplete_light


class UnitedGeoNameAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['main_name', ]
    limit_choices = 20
    autocomplete_js_attributes = {'placeholder': 'Other model name?'}

autocomplete_light.register(UnitedGeoName, UnitedGeoNameAutocomplete)
