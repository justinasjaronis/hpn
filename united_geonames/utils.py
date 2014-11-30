# -*- coding: utf-8 -*-
from django.contrib.gis.geos import Point, Polygon


def get_distance_percentage(distance):
    """
    Distancija - distancija tarp nagrinėjamo objekto ir mached objekto
    Skaičiuojam distancini atitikimą procentais. Distancija 0.0 laikoma 100% atitikimu.
    1.0 - 1km maksimalus distancinis atstumas, ir laikomas 0% atitikimas.
    """
    if distance is None or distance > float(3.0) or distance < float(0.0) or distance == float(3.0):
        return float(0.0)

    elif distance == 0.0:
        return float(100)

    else:
        percentage = float(100) * float(distance) / float(3) #3km distancija
        return round(percentage, 2)
        # return float(300) - float(100) * distance # 1km distancija


def get_ngram_percentage(ngram_distance):
    """
    Ngram skaičiavimo algoritmas.
    Ngram 1.0 - laikomas 100% atitikimu.
    """
    if isinstance(ngram_distance, float) or isinstance(ngram_distance, int):
        if ngram_distance > float(1.0) or ngram_distance is None or ngram_distance < float(0.0):
            return float(0.0)

        else:
            return (float(100) * ngram_distance)
    else:
        raise ValueError('ngram_distance must be int or float, not {0}'.format(type(ngram_distance)))




def disable_reindex():
    from django.db import models
    from haystack import signal_processor

    models.signals.post_save.disconnect(signal_processor.handle_save)
    models.signals.post_delete.disconnect(signal_processor.handle_delete)


def get_middle_point(matched_synonyms_locations):
    """
    Centras tarp dviejų geo taškų
    """
    first_matched_synonym_location_x = float(matched_synonyms_locations[0][0])
    first_matched_synonym_location_y = float(matched_synonyms_locations[0][1])

    second_matched_synonym_location_x = float(matched_synonyms_locations[1][0])
    second_matched_synonym_location_y = float(matched_synonyms_locations[1][1])

    return Point((first_matched_synonym_location_x + second_matched_synonym_location_x) / 2, (first_matched_synonym_location_y + second_matched_synonym_location_y) / 2)


def get_polygon_centroid(polygon):
    """
    Centroid calcutaion in polygon. Minimum points: 4
    """
    first = polygon[0]
    if len(polygon) >= 4:
        polygon.append(first)
        poly = Polygon(tuple(polygon))
        return poly.centroid
    else:
        raise ValueError('Minimum points of centroid must be 4')


def get_triangle_centroid(matched_synonims_polygon):
    if len(matched_synonims_polygon) == 3:
        first = matched_synonims_polygon[0]
        second = matched_synonims_polygon[1]
        third = matched_synonims_polygon[2]

        x = (first[0] + second[0] + third[0]) / 3
        y = (first[1] + second[1] + third[1]) / 3
        return Point(round(float(x), 5), round(float(y), 5))
    else:
        raise ValueError('Must be 3 Points')


def get_centroid(matched_united_geo_synonyms_poly):
    """
    Skaičiuojama geografinė distancija priklausomai nuo kiek yra sumatchintų sinonimų.
    """
    matched_united_geo_synonims_polygon = list(set(matched_united_geo_synonyms_poly))
    if len(matched_united_geo_synonims_polygon) > int(3):
        centroid = get_polygon_centroid(matched_united_geo_synonims_polygon)

    elif len(matched_united_geo_synonims_polygon) == int(3):
        centroid = get_triangle_centroid(matched_united_geo_synonims_polygon)

    elif len(matched_united_geo_synonims_polygon) == int(2):
        centroid = get_middle_point(matched_united_geo_synonims_polygon)

    elif len(matched_united_geo_synonims_polygon) == int(1):
        centroid = Point(round(float(matched_united_geo_synonims_polygon[0][0]), 5), round(float(matched_united_geo_synonims_polygon[0][1]), 5))
    else:
        centroid = None

    return centroid


def update_best_match(instance):
    matched_places = instance.matched.all()
    percentages = []
    if len(matched_places) >= 1:
        for i in matched_places:
            percentages.append(i.percentage)

        for i in matched_places:
            if i.percentage == max(percentages):
                i.best_match = True
                i.save()
                matching_index = format(get_distance_percentage(i.geographical_distance) + get_ngram_percentage(i.ngram_distance), '.2f')
                i.matchinglogmatch.number_of_alternatives = len(matched_places)
                i.matchinglogmatch.matching_index = matching_index
                i.matchinglogmatch.save()
                break
    else:
        instance.number_of_alternatives = int(0)
        instance.matching_index = int(0)
        instance.save()

subregions \
    = [
        ['Kretingos rajonas', u'Kretingos'],
        ['Alytaus rajonas', u'Alytaus r. sav.'],
        ['Alytus', u'Alytaus m. sav.'],
        ['Akmenės Rajonas', u'Akmenės r. sav.'],
        ['Anykščių Rajonas', u'Anykščių r. sav.'],
        ['Anykščiai', u'Anykščių m. sav.'],
        ['Kauno Rajonas', u'Kauno r. sav.'],
        ['Kaunas', u'Kauno m. sav.'],
        ['Panevėžys District Municipality', u'Panevėžio r. sav.'],
        ['Panevėžys City', u'Panevėžio m. sav.'],
        ['Vilnius', u'Vilniaus m. sav.'],
        ['Vilniaus Rajonas', u'Vilniaus r. sav.'],
        ['Marijampolė', u'Marijampolės m. sav.'],
        ['Marijampolės Rajonas', u'Marijampolės sav.'],
        ['Šilalės Rajonas', u'Šilalės r. sav.'],
        ['Telšiai', u'Telšių m. sav.'],
        ['Telšių Rajonas', u'Telšių r. sav.'],
        ['Šiauliai', u'Šiaulių m. sav.'],
        ['Šiaulių Rajonas', u'Šiaulių r. sav.'],
        ['Kupiškio r. sav.', u'Kupiškio Rajonas'],
        ['Trakų Rajonas', u'Trakų r. sav.'],
        ['Šilutės Rajonas', u'Šilutės r. sav.'],
        ['Klaipėda', u'Klaipėdos m. sav.'],
        ['Klaipėdos Rajonas', u'Klaipėdos r. sav.'],
        ['Šalčininkų Rajonas', u'Šalčininkų r. sav.'],
        ['Utenos Rajonas', u'Utenos r. sav.'],
        ['Jonavos Rajonas', u'Jonavos r. sav.'],
        ['Kretinga', u'Kretingos m.'],
        ['Kretingos Rajonas', u'Kretingos r. sav.'],
        ['Palanga', u'Palangos sav.'],
        ['Druskininkai', u'Druskininkų sav.'],
        ['Šakių Rajonas', u'Šakių r. sav.'],
        ['Varėnos Rajonas', u'Varėnos r. sav.'],
        ['Birštonas', u'Birštono sav.'],
        ['Rokiškio Rajonas', u'Rokiškio r. sav.'],
        ['Biržų Rajonas', u'Biržų r. sav.'],
        ['Lazdijų Rajonas', u'Lazdijų r. sav.'],
        ['Zarasų Rajonas', u'Zarasų r. sav.'],
        ['Varėnos Rajonas', u'Alytaus, Varėnos r. sav.'],
        ['Ignalinos Rajonas', u'Ignalinos r. sav.'],
        ['Joniškio Rajonas', u'Joniškio r. sav.'],
        ['Jurbarko Rajonas', u'Jurbarko r. sav.'],
        ['Kaišiadorių Rajonas', u'Kaišiadorių r. sav.'],
        ['Marijampolės Rajonas', u'Kalvarijos sav.'],
        ['Marijampolės Rajonas', u'Kazlų Rūdos sav.'],
        ['Kėdainių Rajonas', u'Kėdainių r. sav.'],
        ['Kelmės Rajonas', u'Kelmės r. sav.'],
        ['Lazdijų Rajonas', u'Lazdijų, Kalvarijos sav.'],
        ['Šalčininkų Rajonas', u'Lydos r.'],
        ['Mažeikių Rajonas', u'Mažeikių r. sav.'],
        ['Mažeikių Rajonas', u'Mažeikių, Telšių r. sav.'],
        ['Molėtų Rajonas', u'Molėtų r. sav.'],
        ['Molėtų Rajonas', u'Molėtų, Švenčionių r. sav.'],
        ['Neringa', u'Neringos m. sav.'],
        ['Tauragė', u'Pagėgių sav.'],
        ['Tauragės Rajonas', u'Tauragės r. sav.'],
        ['Pakruojo Rajonas', u'Pakruojo r. sav.'],
        ['Pasvalio Rajonas', u'Panevėžio, Pasvalio r. sav.'],
        ['Pasvalio Rajonas', u'Pasvalio r. sav.'],
        ['Plungės Rajonas', u'Plungės r. sav.'],
        ['Plungės Rajonas', u'Plungės, Telšių r. sav.'],
        ['Prienų Rajonas', u'Prienų r. sav.'],
        ['Radviliškio Rajonas', u'Radviliškio r. sav.'],
        ['Raseinių Rajonas', u'Raseinių r. sav.'],
        ['Plungės Rajonas', u'Rietavo sav.'],
        ['Širvintų Rajonas', u'Širvintų r. sav.'],
        ['Širvintos', u'Širvintų, Vilniaus r. sav.'],
        ['Skuodo Rajonas', u'Skuodo r. sav.'],
        ['Švenčionių Rajonas', u'Švenčionių r. sav.'],
        ['Ukmergės Rajonas', u'Ukmergės r. sav.'],
        ['Vilkaviškio Rajonas', u'Vilkaviškio r. sav.'],
        ['Visaginas', u'Visagino sav.'],
        ['Zarasų Rajonas', u'Rokiškio, Zarasų r. sav.'],
    ]

