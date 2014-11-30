from geonames_stedsnavn_norge.models import NorwayGeoName
from united_geonames.plugins.default import UnitedGeoNamePlugin
from united_geonames.utils import update_best_match


class NorwayGeoNamePlugin(UnitedGeoNamePlugin):

    class Meta:
        model = NorwayGeoName

    def create_matching_log_entries_for_similar_models(self, create_missing_log):
        #negalima matchinti su norway duomenu baze, reikia macthinti tik su visom kitom
        norway_geo_name = self.Meta.model

        data = norway_geo_name.objects.all()
        for vieta in data.iterator():
            matched_instance = self.run_matching(vieta.pk, vieta.enh_snavn, vieta.coordinates, None, None, create_missing_log)
            update_best_match(matched_instance)