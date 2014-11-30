# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from united_geonames.models import GeoNamesMatchingLogMatch


class GisNgramPercentage(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Ngram with Geo Percentage')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'percentage'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('equals_200', _('=200 %')),
            ('above_190', _('>190 %')),
            ('above_180', _('>180 %')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'equals_200':
            return queryset.filter(matching_index=float(200))

        if self.value() == 'above_190':
            return queryset.filter(matching_index__gte=(float(190)))

        if self.value() == 'above_180':
            return queryset.filter(matching_index__gte=(float(180)))


class GisOrNgramPercentage(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Ngram or Geo Percentage')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'one_of_percentage'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('equals_100', _('=100 %')),
            ('above_95', _('>95 %')),
            ('above_90', _('>90 %')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'equals_100':
            geo_queryset = GeoNamesMatchingLogMatch.objects.filter(matched__geographical_distance__isnull=True, matched__ngram_distance__isnull=False, matching_index=float(100))
            ngram_queryset = GeoNamesMatchingLogMatch.objects.filter(matched__geographical_distance__isnull=False, matched__ngram_distance__isnull=True, matching_index=float(100))
            matches = geo_queryset | ngram_queryset
            return matches

        if self.value() == 'above_95':
            geo_queryset = GeoNamesMatchingLogMatch.objects.filter(matched__geographical_distance__isnull=True, matched__ngram_distance__isnull=False, matching_index__gte=float(95))
            ngram_queryset = GeoNamesMatchingLogMatch.objects.filter(matched__geographical_distance__isnull=False, matched__ngram_distance__isnull=True, matching_index__gte=float(95))
            matches = geo_queryset | ngram_queryset
            return matches

        if self.value() == 'above_90':
            geo_queryset = GeoNamesMatchingLogMatch.objects.filter(matched__geographical_distance__isnull=True, matched__ngram_distance__isnull=False, matching_index__gte=float(90))
            ngram_queryset = GeoNamesMatchingLogMatch.objects.filter(matched__geographical_distance__isnull=False, matched__ngram_distance__isnull=True, matching_index__gte=float(90))
            matches = geo_queryset | ngram_queryset
            return matches



class ProjectDatabaseFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Project filter')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'project_filter'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('matched_vietos', _('Matched Vietos')),
            ('matched_pleiades', _('Matched Pleiades')),
            ('matched_norway', _('Matched Norway')),
            # ('above_90', _('>90 %')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'matched_vietos':
            vietos = GeoNamesMatchingLogMatch.objects.filter(content_type=44)
            return vietos

        if self.value() == 'matched_pleiades':
            vietos = GeoNamesMatchingLogMatch.objects.filter(content_type=360)
            return vietos

        if self.value() == 'matched_norway':
            vietos = GeoNamesMatchingLogMatch.objects.filter(content_type=361)
            return vietos
