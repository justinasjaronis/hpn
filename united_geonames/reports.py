# coding=utf-8
from model_report.report import reports, ReportAdmin
from united_geonames.models import GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchedPlaces
from django.utils.translation import ugettext_lazy as _
from model_report.utils import count_column


class MatchingLogReport(ReportAdmin):

    title = _(u'Matching Logs')
    model = GeoNamesMatchingLogMatch

    fields = ['start_date', 'content_type', 'object_id', 'number_of_alternatives', 'matching_index']

    list_filter = ('start_date', 'content_type', 'object_id', 'number_of_alternatives', 'matching_index')

    list_group_by = ('number_of_alternatives', 'matching_index')

    type = 'chart'

    chart_types = ('pie', 'column')

    report_totals = {
        'number_of_alternatives': count_column,
    }

    group_totals = {
        'number_of_alternatives': count_column
    }

reports.register('matching-report', MatchingLogReport)


def round_ngram_value(value):
    return round(value, 1)


def round_geo_distance_value(value):
    if isinstance(value, float):
        return round(value, 1)

    else:
        return 'None'


class MatchingPlacesLogReport(ReportAdmin):

    title = _(u'Matching Logs Places')
    model = GeoNamesMatchingLogMatchedPlaces

    fields = ['geographical_distance', 'ngram_distance', 'percentage']

    list_filter = ('geographical_distance', 'ngram_distance', 'percentage')

    list_group_by = ('geographical_distance', 'ngram_distance', 'percentage')

    override_group_value = {
        'ngram_distance': round_ngram_value,
        'geographical_distance': round_geo_distance_value,
    }
    type = 'chart'

    chart_types = ('pie', 'column')

    report_totals = {
        'geographical_distance': count_column,
    }

    group_totals = {
        'geographical_distance': count_column
    }

reports.register('matching-places-report', MatchingPlacesLogReport)
