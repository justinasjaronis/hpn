# coding=utf-8
from united_geonames.plugins.default import UnitedGeoNamePlugin
from united_geonames.utils import update_best_match
from aruodai.pleiades.models import PleiadePlace

class PleiadesPlugin(UnitedGeoNamePlugin):

    class Meta:

        model = PleiadePlace

    def create_matching_log_entries_for_similar_models(self, create_missing_log):
        place = self.Meta.model
        data = place.objects.only('title', 'repr_lat_long').all()
        for place in data.iterator():
            if place.title == 'Untitled' or place.title == 'untitled' or place.title == 'Unnamed villa':
                place.title = None
            else:
                place.title = place.title.split('/')
            matched_instance = self.run_matching(place.pk, place.title, place.repr_lat_long, None, None, create_missing_log, None)
            update_best_match(matched_instance)
