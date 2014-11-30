# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from django.forms.models import inlineformset_factory

from django.http import HttpResponseRedirect, HttpResponse, Http404

from united_geonames.forms import UserGeoNameForm, GeoNamesMatchingLogMatchedPlacesFormUser, \
    GeoNamesMatchingLogMatchForm, UserGeoNameFormWithoutMap, UserUnitedGeoNameSynonimForm, DatabaseForm
from united_geonames.models import GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchedPlaces, \
    UnitedGeoNameSynonim, UnitedGeoName, UserGeoName

from rest_framework import status
from united_geonames.plugins.user import UserGeoNamePlugin
from united_geonames.serializers import UserGeoNameSerializer, GeoNamesMatchingLogMatchSerializer, \
    UnitedGeoNameSerializer
from united_geonames.utils import update_best_match

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

def get_matching_object(instance):
    cont_type = ContentType.objects.get_for_model(UserGeoName)
    if instance.name:
        name = instance.name
    else:
        name = None

    if instance.region:
        region = instance.region
    else:
        region = None

    if instance.subregion:
        subregion = instance.subregion
    else:
        subregion = None

    if instance.coordinates:
        coordinates = instance.coordinates
    else:
        coordinates = None

    if instance.country:
        country = instance.country
    else:
        country = None

    if instance.name:
        name = name.encode("utf-8")
    matched_log = UserGeoNamePlugin(cont_type).run_matching(instance.pk, name, coordinates, region, subregion, False, country)
    update_best_match(matched_log)
    return matched_log


def new_user_geoname(request):
    if request.method == 'POST':
        rp = request.POST
        # Saugant tuščią GMF lauką metą klaidas. Kad jų išvengti, jeigu request.POST mato, kad
        # vartotojas neįvedė koordinačių - yra naudojama kitą forma, kurioje fieldas coordinatės
        # exludintas.
        if not rp['coordinates_lat'] and not rp['coordinates_lon']:
            user_geo_name_form = UserGeoNameFormWithoutMap(request.POST)
        else:
            user_geo_name_form = UserGeoNameForm(request.POST)

        if user_geo_name_form.is_valid():

            instance = user_geo_name_form.save()
            # from pudb import set_trace; set_trace()
            matched_log = get_matching_object(instance)
            redirect_to = ('/unitedgeo/matched_object/{0}/').format(matched_log.id)
            return HttpResponseRedirect(redirect_to)

    else:
        user_geo_name_form = UserGeoNameForm()

    return render(request, 'tags/forms/user_form.html', {
        'user_geo_name_form': user_geo_name_form,
    })


def matched_logs(request, matching_id, center_x="54.89850", center_y="23.90354"):
    mas = []

    matched_object = get_object_or_404(GeoNamesMatchingLogMatch, id=matching_id)
    GeoNamesMatchingLogMatchedPlacesFormSet = inlineformset_factory(GeoNamesMatchingLogMatch,
                                                                    GeoNamesMatchingLogMatchedPlaces,
                                                                    form=GeoNamesMatchingLogMatchedPlacesFormUser,
                                                                    extra=1,
                                                                    can_delete=False)
    Synonyms = inlineformset_factory(UnitedGeoName,
                                     UnitedGeoNameSynonim,
                                     form=UserUnitedGeoNameSynonimForm,
                                     extra=0,
                                     can_delete=False)
    searched_language = matched_object.model_matching.language
    if request.method == "POST":
        matched_log = GeoNamesMatchingLogMatchForm(request.POST)
        formset = GeoNamesMatchingLogMatchedPlacesFormSet(request.POST, request.FILES, instance=matched_object)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/unitedgeo/thanks/')
    else:
        matched_log = GeoNamesMatchingLogMatchForm(instance=matched_object)
        formset = GeoNamesMatchingLogMatchedPlacesFormSet(instance=matched_object)
        for i in formset.forms:
            synonym_objects = i.instance.united_geoname
            i.synonim = Synonyms(instance=synonym_objects)

        objects = []
        for i in matched_log.instance.matched.all():
            for a in i.united_geoname.related_synonyms.all():
                objects.append(a)

        for a in objects:
            if a.coordinates:
                x_coord = str(a.coordinates[1])
                y_coord = str(a.coordinates[0])
                mas.append(dict(
                    x=x_coord,
                    y=y_coord,
                    id=a.pk,
                    name=a.name,
                ))

    return render(request, 'united_geonames/maching_geo_form.html', {
        'searched_language': searched_language,
        'formset': formset,
        'mas': mas,
        'center_x': center_x,
        'center_y': center_y,
        'map_name': 'map',

    })


def send_database(request):
    database_form = DatabaseForm()
    if request.method == 'POST':
        database_form = DatabaseForm(request.POST)
        if database_form.is_valid():
            database_form.save()
            return HttpResponseRedirect('/unitedgeo/thanks/')
    else:
        database_form = DatabaseForm()
    return render(request, 'tags/forms/database_form.html', {
        'database_form': database_form,
    })


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class MatchedObjectDetailApiView(APIView):
    """
    Return matched objects.
    """
    def get_object(self, match_object_id):
        try:
            return GeoNamesMatchingLogMatch.objects.get(pk=match_object_id)
        except UserGeoName.DoesNotExist:
            raise Http404

    def get(self, request, matching_log_id, format=None):
        geo_name_matching_log_match = self.get_object(matching_log_id)
        serializer = GeoNamesMatchingLogMatchSerializer(geo_name_matching_log_match)
        return Response(serializer.data)


from rest_framework.permissions import IsAuthenticated

class UserGeoNameApiDetail(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    """
    Search/Propose User Geo Name
    """
#    @authentication_classes((SessionAuthentication, BasicAuthentication))
    
    
    def get(self, request, format=None):
        if not request.user.is_authenticated or isinstance(request.user, AnonymousUser):
            user_id = -1
        else:
            user_id = request.user
        snippets = UserGeoName.objects.filter(user=user_id)
        serializer = UserGeoNameSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserGeoNameSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            serializer.object.user = request.user
            serializer.object.save()
            matched_log = get_matching_object(serializer.object)
            matched_serializer = GeoNamesMatchingLogMatchSerializer(matched_log)
            return Response(matched_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGeoNameSearchApiDetail(APIView):
    def post(self, request, format=None):
        # Kokia yra prasme praleisti siuos duomenis per serializeri? Ar ne verciau butu tiesiai paieska is post'o vykdyt?
#        serializer = UserGeoNameSerializer(data=request.DATA)
        if True: #serializer.is_valid()
            data = {'main_name__icontains': request.DATA.get('name'),
                    'region__icontains': request.DATA.get('region'),
                    'subregion__icontains': request.DATA.get('subregion'),
                    'country__icontains': request.DATA.get('country'),
                    'centroid__icontains': request.DATA.get('coordinates')
            }
            not_none_values_for_filter = dict((k, v) for k, v in data.iteritems() if v is not None)
            if len(not_none_values_for_filter.keys()) == 0:
                from pprint import pprint
                pprint(request.DATA)
                pprint(data)
                raise Exception("None filter values detected!")
                
            qs = UnitedGeoName.objects.filter(**not_none_values_for_filter)
            result = UnitedGeoNameSerializer(qs)
            return Response(result.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ExampleView(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)