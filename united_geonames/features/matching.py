# coding=utf-8
from lettuce import step
from django.contrib.gis.geos import Point

from cities.models import City

from nose.tools import assert_equals

from united_geonames.models import UnitedGeoName
from united_geonames.plugins.user import UserGeoNamePlugin
from mock import MagicMock
import mock

@step(u'we have a City object "(.*)"')
def have_city_object(step, object):
    city_name = City.objects.get(name=object)
    assert_equals(city_name.name, object)


@step(u'get United Geo object "(.*)"')
def united_geo_object(step, name):
    united_geo = UnitedGeoName.objects.get(main_name=name)
    assert_equals(united_geo.main_name, name)

from mock import patch
@step(u'we will run matching for name "(.*)"')
def run_metching_for_name(step, name):
    # By UnitedGeoNameSynonym
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}

    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    if len(log.matched.all()) == 1:
        assert_equals(log.matched.all()[0].united_geoname.main_name, "Vilnius")
    else:
        raise Exception('It is necessary to improve the test.')
    log.delete()


@step(u'by user country "(.*)" and name "(.*)"')
def user_run_matching_country_name(step, country, name):
    # By UnitedGeoName
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}

    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, name)
    log.delete()


@step(u'Given by user country "([^"]*)" and coordinates x "([^"]*)" y "([^"]*)"')
def given_by_user_country_and_coordinates_x_y(step, country, x, y):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Vilnius')
    log.delete()


@step(u'Given by user country "([^"]*)" and region "([^"]*)"')
def given_by_user_country_and_region(step, country, region):
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': None,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user country "([^"]*)" and subregion "([^"]*)"')
def given_by_user_country_and_subregion(step, country, subregion):
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user name "([^"]*)" and coordinates x "([^"]*)" y "([^"]*)"')
def given_by_user_name_and_coordinates_x_y(step, name, x, y):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': coordinates,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user name "([^"]*)" and subregion "([^"]*)"')
def given_by_user_name_and_subregion(step, name, subregion):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user name "([^"]*)" and region "([^"]*)"')
def given_by_user_name_and_region(step, name, region):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user only region "([^"]*)"')
def given_by_user_only_region(step, region):
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': None,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user only subregion "([^"]*)"')
def given_by_user_only_subregion(step, subregion):
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user only coordinates x "([^"]*)" y "([^"]*)"')
def given_by_user_only_coordinates_x_y(step, x, y):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user only name "([^"]*)"')
def given_by_user_only_name(step, name):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Vilnius')
    log.delete()


@step(u'Given by user only country "([^"]*)"')
def given_by_user_only_country(step, country):
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user coordinates x "([^"]*)" y "([^"]*)" and region "([^"]*)"')
def given_by_user_coordinates_x_y_and_region(step, x, y, region):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user coordinates x "([^"]*)" y "([^"]*)" and city "([^"]*)"')
def given_by_user_coordinates_x_y_and_city(step, x, y, name):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': coordinates,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by user coordinates x "([^"]*)" y "([^"]*)" and country "([^"]*)"')
def given_by_user_coordinates_x_y_and_country(step, x, y, country):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': None,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


# Scenario: three different variations of input
@step(u'Given by three: user name "([^"]*)" coordinates x "([^"]*)" y "([^"]*)" and region "([^"]*)"')
def given_by_three_user_name_coordinates_x_y_and_region(step, name, x, y, region):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by three: user name "([^"]*)" region "([^"]*)" subregion "([^"]*)"')
def given_by_three_user_name_region_subregion(step, name, region, subregion):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': region,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by three: user name "([^"]*)" country "([^"]*)" subregion "([^"]*)"')
def given_by_three_user_name_country_subregion(step, name, country, subregion):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': None,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by three: user name "([^"]*)" country "([^"]*)" region "([^"]*)"')
def given_by_three_user_name_country_region(step, name, country, region):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by three: user coord x "([^"]*)" coord y "([^"]*)" and region "([^"]*)" subregion "([^"]*)"')
def given_by_three_user_coord_x_coord_y_and_region_subregion(step, x, y, region, subregion):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by three: user coord x "([^"]*)" coord y "([^"]*)" and region "([^"]*)" country "([^"]*)"')
def given_by_three_user_coord_x_coord_y_and_region_country(step, x, y, region, country):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


# Scenario: four different variations of input
@step(u'Given by four: user name "([^"]*)" coordinates x "([^"]*)" y "([^"]*)" and region "([^"]*)" subregion "([^"]*)"')
def given_by_four_user_name_coordinates_x_y_and_region_subregion(step, name, x, y, region, subregion):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': None}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by four: user name "([^"]*)" coordinates x "([^"]*)" y "([^"]*)" and region "([^"]*)" country "([^"]*)"')
def given_by_four_user_name_coordinates_x_y_and_region_country(step, name, x, y, region, country):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': None,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by four: user name "([^"]*)" and region "([^"]*)" country "([^"]*)" subregion "([^"]*)"')
def given_by_four_user_name_and_region_country_subregion(step, name, region, country, subregion):
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': None,
              'place_region': region,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


@step(u'Given by four: user coordinates x "([^"]*)" y "([^"]*)" and region "([^"]*)" country "([^"]*)" subregion "([^"]*)"')
def given_by_four_user_coordinates_x_y_and_region_country_subregion(step, x, y, region, country, subregion):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': None,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()


# Scenario: five different variations of input
@step(u'Given by five: user name "([^"]*)" coordinates x "([^"]*)" y "([^"]*)" and region "([^"]*)" subregion "([^"]*)" country "([^"]*)"')
def given_by_five_user_name_coordinates_x_y_and_region_subregion_country(step, name, x, y, region, subregion, country):
    coordinates = Point(float(x), float(y))
    kwargs = {'place_pk': 1,
              'place_name': name,
              'place_coordinates': coordinates,
              'place_region': region,
              'place_subregion': subregion,
              'create_missing_log': False,
              'place_country': country}
    log = UserGeoNamePlugin(None).run_matching(**kwargs)
    assert_equals(len(log.matched.all()), 1)
    assert_equals(log.matched.all()[0].united_geoname.main_name, 'Paris')
    log.delete()