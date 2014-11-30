# coding=utf-8
from django.contrib.gis.geos import Point
from utils import load_django
load_django()

from django.contrib.contenttypes.models import ContentType

from united_geonames.models import UserGeoName
from united_geonames.plugins.default import UnitedGeoNamePlugin
from united_geonames.models import UnitedGeoName
from mock_django.query import QuerySetMock
from mock_django.managers import ManagerMock

import unittest

import mock

class DefaultPluginTest(unittest.TestCase):

    def setUp(self):
        cont_type = ContentType.objects.get_for_model(UserGeoName)
        self.plugin = UnitedGeoNamePlugin(cont_type)


    def tearDown(self):
        pass

    def test_get_distance_between_two_points(self):
        self.assertEquals(self.plugin.get_distance_between_two_points(None, 3), None)

    def test_get_ngram_distance(self):
        UnitedGeoName = mock.MagicMock()
        UnitedGeoNameSynonymVilnius = mock.MagicMock()
        UnitedGeoNameSynonymVilnius.name = 'Vilnius'
        UnitedGeoNameSynonymWilno = mock.MagicMock()
        UnitedGeoNameSynonymWilno.name = 'Wilno'
        UnitedGeoName.get_synonyms.return_value = [UnitedGeoNameSynonymVilnius, UnitedGeoNameSynonymWilno]
        self.assertEquals(self.plugin.get_ngram_distance(None, []), float(0.0))
        self.assertEquals(self.plugin.get_ngram_distance('Wilno', UnitedGeoName), float(1.0))

    def test_get_matching_synonims(self):
        UnitedGeoName.objects = ManagerMock(UnitedGeoName,  UnitedGeoName(country='Lithuania'))
        result = self.plugin.get_matching_synonyms(None, None, None, None, 'Minsk')
        self.assertEquals(result[0].country, 'Lithuania')
