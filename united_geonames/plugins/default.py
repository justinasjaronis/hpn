# -*- coding: utf-8 -*-
from united_geonames.models import UnitedGeoName, GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchedPlaces, \
    UnitedGeoNameSynonim
from united_geonames.utils import get_distance_percentage, get_ngram_percentage

import ngram


class UnitedGeoNamePlugin(object):
    def __init__(self, cont_type):
        self.cont_type = cont_type

    class Meta:
        abstract = True
        model = None

    @staticmethod
    def get_distance_between_two_points(place_coordinates, matched_geo_name_id):
        """
        Distance between two points
        """
        if place_coordinates is not None:
            if UnitedGeoName.objects.filter(id=matched_geo_name_id).exists():
                for i in UnitedGeoName.objects.distance(place_coordinates).filter(id=matched_geo_name_id):
                    return i.distance.km
        else:
            return None

    def create_matching_log_entries_for_similar_models(self, create_missing_log):
        pass

    @staticmethod
    def get_ngram_distance(place_name, matched_geoname):
        """
        Skaičiuojamas ngram atitikimas.
        """
        if place_name:
            names = [i.name.encode('utf-8') for i in matched_geoname.get_synonyms()]

            G = ngram.NGram(names, key=lambda x: x.lower(), N=1)
            ngrams = G.searchitem(place_name)
            if len(ngrams) > 0:
                return float(ngrams[0][-1])
            else:
                return float(0.0)
        else:
            return float(0.0)

    def create_matching_logs(self, matched_geonames, place_pk, place_coordinates, place_name):
        gnmlm = GeoNamesMatchingLogMatch(content_type=self.cont_type, object_id=place_pk)
        gnmlm.save()
        for matched_geoname in matched_geonames:

            ngram_distance = self.get_ngram_distance(place_name, matched_geoname)
            distance = self.get_distance_between_two_points(place_coordinates, matched_geoname.id)

            percentage = \
                (get_distance_percentage(distance) + get_ngram_percentage(ngram_distance)) / float(2)

            percentage = format(percentage, '.2f')
            if distance:
                distance = format(distance, '.2f')

            ngram_distance = format(ngram_distance, '.2f')

            created_matching_logs = GeoNamesMatchingLogMatchedPlaces.objects.create(matchinglogmatch=gnmlm,
                                                                     united_geoname=matched_geoname,
                                                                     percentage=percentage,
                                                                     geographical_distance=distance,
                                                                     ngram_distance=ngram_distance)
        return gnmlm

    def create_united_geo_with_synonym(self, place_pk, place_name, place_coordinates, place_region,
                           place_subregion, place_country):

        obj, ugn = UnitedGeoName.objects.get_or_create(main_name=place_name,
                           country=place_country,
                           region=place_region,
                           subregion=place_subregion)

        object, ugns = UnitedGeoNameSynonim.objects.get_or_create(
                                united_geoname=obj, name=place_name,
                                content_type=self.cont_type, object_id=place_pk,
                                coordinates=place_coordinates,
                                synonim_content_type=None)

        return object

    @staticmethod
    def names_by_ngram(name):
        if name is not None:
            # TODO: reikia ieskoti pagal UnitedGeoNameSynonyms dar.
            ngrams = UnitedGeoName.objects.raw(
                      """SELECT *, similarity(main_name, '{0}') AS sml
                      FROM united_geonames_unitedgeoname
                      WHERE main_name %% '{0}'
                      ORDER BY sml DESC, main_name""".format(name.encode('ascii', 'ignore').replace("'", ""))
            )
            return [n.id for n in ngrams]
        else:
            return None

    def get_matching_synonyms(self, place_name, place_coordinates, place_region, place_subregion, place_country):
        dict_for_filter = {'region__icontains': place_region,
                           'subregion__icontains': place_subregion,
                           'country__icontains': place_country}
        not_none_values_for_filter = dict((k, v) for k, v in dict_for_filter.iteritems() if v is not None)
        matched_geonames = UnitedGeoName.objects.filter(**not_none_values_for_filter)
        if place_name:
            matched_geonames = matched_geonames.filter(related_synonyms__name__icontains=place_name)

        if place_name and isinstance(place_name, list):
        #TODO: Padaryti, kad ir listui contains kviestu
            matched_geonames = matched_geonames.filter(related_synonyms__name__in=place_name)

        if place_coordinates:
            matched_geonames = matched_geonames.filter(centroid__dwithin=(place_coordinates, 0.03))
            matched_geonames_with_good_distance = []
            for i in UnitedGeoName.objects.distance(place_coordinates)\
                                         .filter(id__in=[i.id for i in matched_geonames]):
                 if i.distance.km < float(3):
                     matched_geonames_with_good_distance.append(i)
            return list(set(matched_geonames_with_good_distance))
        return list(set(matched_geonames))

    def run_matching(self, place_pk, place_name, place_coordinates, place_region, place_subregion,
                     create_missing_log, place_country):
        if create_missing_log:
            return self.create_united_geo_with_synonym(place_pk, place_name, place_coordinates, place_region,
                                   place_subregion, place_country)
        else:
            matched_geonames = self.get_matching_synonyms(place_name, place_coordinates, place_region, place_subregion,
                                                          place_country)
            if matched_geonames:
                return self.create_matching_logs(matched_geonames, place_pk, place_coordinates, place_name)
            else:
                return GeoNamesMatchingLogMatch.objects.create(content_type=self.cont_type, object_id=place_pk)