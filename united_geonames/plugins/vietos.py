from django.core.exceptions import ObjectDoesNotExist
# import logging
from main.models.vietos.models import Vietos, SubregionAruodai
from united_geonames.plugins.default import UnitedGeoNamePlugin
from united_geonames.utils import subregions, update_best_match


class AruodaiVietosUnitedGeoNamePlugin(UnitedGeoNamePlugin):

    class Meta:
        model = Vietos

    def migrate_subrigion_aruodai_to_vietos_subrigion(self, subrigion_aruodai_name, savivaldybe_not_full_name):
        aruodai_vietos = self.Meta.model
        try:
            subrigion = SubregionAruodai.objects.get(name=subrigion_aruodai_name)
            for vieta in aruodai_vietos.objects.filter(savivaldybe=savivaldybe_not_full_name):
                if not vieta.subregion:
                    vieta.subregion = subrigion
                    vieta.save()
        except ObjectDoesNotExist:
            print "Does Not Exists"

    def subregion_migrator(self):
        for subregion in subregions:
            city_subregion_name = subregion[0]
            analogic_aruodu_savivaldybes_name = subregion[1]
            self.migrate_subrigion_aruodai_to_vietos_subrigion(city_subregion_name, analogic_aruodu_savivaldybes_name)

    def replace_apskritis(self):
        for vieta in self.Meta.model.objects.all():
            apsk = (vieta.apskritis).replace('apskr.', 'Apskritis')
            vieta.apskritis = apsk
            vieta.save()

    def create_matching_log_entries_for_similar_models(self, create_missing_log):
        aruodai_vietos = self.Meta.model
        data = aruodai_vietos.objects.all()
        for vieta in data.iterator():
            try:
                coordinates = vieta.vikoordinates_set.all()[0].koord
            except:
                coordinates = None

            if vieta.salis == 'Lietuvos Respublika':
                country = 'Lithuania'
            else:
                country = None


            if vieta.pavadinimas is None: continue
            matched_log = self.run_matching(vieta.pk, vieta.pavadinimas, coordinates, None, None, create_missing_log, country)
            update_best_match(matched_log)
