# import logging
from cities.models import City
from united_geonames.plugins.default import UnitedGeoNamePlugin
from united_geonames.utils import disable_reindex, update_best_match
from united_geonames.models import UnitedGeoNameSynonim, GeoNamesMatchingLogMatch

class GeoNameUnitedGeoNamePlugin(UnitedGeoNamePlugin):

    class Meta:
        model = City

    def create_matching_log_entries_for_similar_models(self, create_missing_log):
        disable_reindex()
        city_vietos = self.Meta.model
        data = city_vietos.objects.only('region', 'subregion', 'name', 'location', 'country').all()
        for place in data.iterator():
            print place
            try:
                region = place.region.name_std
            except:
                region = None
            try:
                subregion = place.subregion.name_std
            except:
                subregion = None

            try:
                country = place.country.name
            except:
                country = None

            returned = self.run_matching(place.pk, place.name, place.location, region,
                              subregion, create_missing_log, country)

            if returned is not False:
                returned.city_alt_names()
