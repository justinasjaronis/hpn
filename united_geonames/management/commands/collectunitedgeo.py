# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from cities.models import City

from main.models.vietos.models import Vietos
from geonames_stedsnavn_norge.models import NorwayGeoName
from pleiades.models import PleiadePlace
from united_geonames.plugins.city import GeoNameUnitedGeoNamePlugin
from united_geonames.plugins.vietos import AruodaiVietosUnitedGeoNamePlugin
from united_geonames.plugins.pleiades import PleiadesPlugin
from united_geonames.plugins.norway import NorwayGeoName, NorwayGeoNamePlugin
from optparse import make_option


class Command(BaseCommand):
    args = '<none>'
    help = 'This is special united geo collecting management command'

    option_list = BaseCommand.option_list + (
        make_option('--automatically-create-missing',
                    dest='create_missing',
                    default=False,
                    help='On run automatically create UnitedGeoSynonims if matched objects does not exists.'),
        make_option('--cities',
                    dest='cities',
                    default=False,
                    help='Run matching script on Cities objects.'),
        make_option('--vietos',
                    dest='vietos',
                    default=False,
                    help='Run matching script on Vietos objects.'),
        make_option('--pleiades',
                    dest='pleiades',
                    default=False,
                    help='Run matching script on Pleiades objects.'),
        make_option('--norway',
                    dest='norway',
                    default=False,
                    help='Run matching script on Norway objects.'),
    )

    def handle(self, *args, **options):
        if options['create_missing'] == 'true' and options['cities'] == 'true':
            cont_type = ContentType.objects.get_for_model(City)
            GeoNameUnitedGeoNamePlugin(cont_type).create_matching_log_entries_for_similar_models(create_missing_log=True)

        elif options['create_missing'] == 'false' and options['vietos'] == 'true':
            print("Matchinamos Aruodu vietos")
            cont_type = ContentType.objects.get_for_model(Vietos)
            AruodaiVietosUnitedGeoNamePlugin(cont_type).create_matching_log_entries_for_similar_models(create_missing_log=False)

        elif options['create_missing'] == 'false' and options['pleiades'] == 'true':
            cont_type = ContentType.objects.get_for_model(PleiadePlace)
            PleiadesPlugin(cont_type).create_matching_log_entries_for_similar_models(create_missing_log=False)

        elif options['create_missing'] == 'false' and options['norway'] == 'true':
            print("Norway matching")
            cont_type = ContentType.objects.get_for_model(NorwayGeoName)
            NorwayGeoNamePlugin(cont_type).create_matching_log_entries_for_similar_models(create_missing_log=False)