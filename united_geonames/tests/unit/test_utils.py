# coding=utf-8
from django.contrib.gis.geos import Point
from utils import load_django
load_django()

from united_geonames.utils import get_ngram_percentage, get_distance_percentage, get_middle_point, get_triangle_centroid, \
    get_polygon_centroid, get_centroid
import unittest

class UtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_distance_percentage(self):
        self.assertEquals(get_distance_percentage(0.0), float(100))
        self.assertEquals(get_distance_percentage(3.0), float(0.0))
        self.assertEquals(get_distance_percentage(1.5), float(50.0))
        self.assertEquals(get_distance_percentage(float(1.0)), float(33.33))

    def test_get_ngram_percentage(self):
        self.assertEquals(get_ngram_percentage(float(0.0)), float(0.0))
        self.assertEquals(get_ngram_percentage(float(1.0)), float(100))
        self.assertEquals(get_ngram_percentage(1.0), float(100))
        self.assertRaises(ValueError, get_ngram_percentage, 'string')
        self.assertRaises(ValueError, get_ngram_percentage, '1.0')

    def test_get_middle_point(self):
        self.assertEqual(get_middle_point([(3, 3), (4, 4)]), Point(3.5, 3.5))

    def test_get_polygon_centroid(self):
        self.assertEquals(get_polygon_centroid([(22.33, 22.33), (22.33, 22.33), (22.33, 22.33), (22.33, 22.33)]), Point(22.33, 22.33))

    def test_get_triangle_centroid(self):
        self.assertEqual(get_triangle_centroid([(22.33, 22.33), (22.33, 22.33), (22.33, 22.33)]), Point(22.33, 22.33))
        self.assertRaises(ValueError, get_triangle_centroid, [(22.33, 22.33), (22.33, 22.33)])
        self.assertRaises(ValueError, get_triangle_centroid, [(22.33, 22.33)])
        self.assertRaises(ValueError, get_triangle_centroid, [(22.33, 22.33), (22.33, 22.33), (22.33, 22.33), (22.33, 22.33)])
        self.assertRaises(ValueError, get_triangle_centroid, ['Test', 'Test2', 'Test3', 'test4'])

    def test_get_centroid(self):
        self.assertEquals(get_centroid([(22.33, 22.33), (22.33, 22.33), (22.33, 22.33), (22.33, 22.33)]), Point(22.33, 22.33))
