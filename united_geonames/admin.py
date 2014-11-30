# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import UnitedGeoNameSynonimForm, GeoNamesMatchingLogMatchedPlacesForm
from main.models.vietos.models import Vietos

from united_geonames.filters import GisNgramPercentage, GisOrNgramPercentage, ProjectDatabaseFilter
from united_geonames.models import UnitedGeoName, UnitedGeoNameSynonim, GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchedPlaces, \
    UserProject, UserGeoName, Database
from united_geonames.plugins.default import UnitedGeoNamePlugin


def create_only_synonym(ugn_object, place_name, content_type, object_id, coordinates):
    UnitedGeoNameSynonim.objects.get_or_create(
        united_geoname=ugn_object,
        name=place_name,
        content_type=content_type,
        object_id=object_id,
        coordinates=coordinates,
    )


def vietos_coordinates(matched_object):
    try:
        return Vietos.objects.using('default').get(viid=matched_object.object_id).vikoordinates_set.all()[0].koord
    except:
        return None


def get_place_detail_accord_by_content_type(obj):
    # Vietos
    if obj.content_type.id == 44:
        obj.model_matching = Vietos.objects.using('default').get(viid=obj.object_id)
        place_name = obj.model_matching.pavadinimas
        coordinates = vietos_coordinates(obj)
        region = obj.model_matching.apskritis
        country = obj.model_matching.salis
        try:
            subregion = obj.model_matching.subregion.name_std
        except:
            subregion = None

    # Norway
    if hasattr(obj.model_matching, 'enh_snavn'):
        place_name = obj.model_matching.enh_snavn
        coordinates = obj.model_matching.coordinates
        region = None
        subregion = None
        country = None

    # Pleiades
    if hasattr(obj.model_matching, 'title'):
        place_name = obj.model_matching.title
        coordinates = obj.model_matching.coordinates
        region = None
        subregion = None
        country = None

    return (obj.model_matching, place_name, coordinates, region, subregion, country)


def create_new_geoname(modeladmin, request, queryset):
    for obj in queryset:
        place, place_name, coordinates, region, subregion, country = get_place_detail_accord_by_content_type(obj)
        UnitedGeoNamePlugin().create_united_geo_with_synonym(place, place_name, coordinates, region, subregion, country)
        obj.delete()
create_new_geoname.short_description = u'Create new United Geo Name'


def merge_with_proposed_geoname(modeladmin, request, queryset):
    for obj in queryset:
        for matched in obj.matched.all():
            if matched.best_match:
                ungeo_object = matched.united_geoname
                matched_object = matched.matchinglogmatch
                place, place_name, coordinates, region, subregion, country = get_place_detail_accord_by_content_type(obj)
                create_only_synonym(ungeo_object, place_name, matched_object.content_type, matched_object.object_id, coordinates)
        obj.delete()
merge_with_proposed_geoname.short_description = u'Link to the proposed Geo Name'


def merge_with_selected_geoname(modeladmin, request, queryset):
    link_with_pk = request.POST['import_place']
    for obj in queryset:
        for matched in obj.matched.all():
            matched_object = matched.matchinglogmatch
            ungeo_object = matched.united_geoname
            if str(matched.pk) == str(link_with_pk):
                place, place_name, coordinates, region, subregion, country = get_place_detail_accord_by_content_type(obj)
                create_only_synonym(ungeo_object, place_name, matched_object.content_type, matched_object.object_id, coordinates)
        obj.delete()
merge_with_selected_geoname.short_description = u'Link with the selected Geo Name'


class UnitedGeoNameSynonimInline(admin.StackedInline):
    model = UnitedGeoNameSynonim
    form = UnitedGeoNameSynonimForm
    extra = 0
    raw_id_fields = ('united_geoname', 'content_type', 'synonim_content_type',)


class UnitedGeoNameAdmin(admin.ModelAdmin):
    model = UnitedGeoName
    inlines = [
        UnitedGeoNameSynonimInline,
    ]
    search_fields = ['main_name', ]
    ordering = ['main_name']


class GeoNamesMatchingLogMatchedPlacesInline(admin.StackedInline):
    model = GeoNamesMatchingLogMatchedPlaces
    form = GeoNamesMatchingLogMatchedPlacesForm
    extra = 0


class GeoNamesMatchingLogMatchedPlacesAdmin(admin.ModelAdmin):
    model = GeoNamesMatchingLogMatchedPlaces
    form = GeoNamesMatchingLogMatchedPlacesForm


class UnitedGeoNameSynonimAdmin(admin.ModelAdmin):
    model = UnitedGeoNameSynonim


class GeoNamesMatchingLogMatchAdmin(admin.ModelAdmin):
    actions = [merge_with_proposed_geoname, merge_with_selected_geoname, create_new_geoname]
    inlines = [
        GeoNamesMatchingLogMatchedPlacesInline,
    ]
    ordering = ('-matching_index',)
    list_display = ('place_object', 'start_date', 'matching_index', 'number_of_alternatives', 'matched_objects')
    list_filter = (GisNgramPercentage, GisOrNgramPercentage, ProjectDatabaseFilter)

    def queryset(self, request):
        qs = super(GeoNamesMatchingLogMatchAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(display_for_users=request.user)

    def place_object(self, obj):
        # Aruodai vietos (kad nemigruoti duomenu)
        if obj.content_type.id == 44:
            return Vietos.objects.using('default').get(viid=obj.object_id).pavadinimas
        # Kitos
        else:
            return obj.model_matching

    @staticmethod
    def check_if_checked(bool):
        if bool:
            return 'checked'
        else:
            return ''

    def matched_objects(self, obj):
        if any(obj.matched.all()):
            return '<form>{0}</form><br /><a href=\"/admin/{1}/{2}/{3}/?_popup=1">Add another place</a>'.format("<br />".join(
                [
                    "<a href=\"/admin/%s/%s/%d\">The proposed place %s Distance %s %s%s</a>  <input type='radio' name='import_place' value='%s' %s/>" %
                    (i.united_geoname._meta.app_label, i.united_geoname._meta.module_name, i.united_geoname.id, i.united_geoname, i.geographical_distance, i.percentage, '%', i.pk, self.check_if_checked(i.best_match))
                    for i in obj.matched.all()
                ]
            ), obj._meta.app_label, obj._meta.module_name, obj.id)
        else:
            return '<b>There is no Matched Places</b><br /><a href=\"/admin/{0}/{1}/{2}/?_popup=1">Add place</a>'.format(
                obj._meta.app_label, obj._meta.module_name, obj.id
            )
    matched_objects.allow_tags = True


class UserProjectAdmin(admin.ModelAdmin):
    model = UserProject

admin.site.register(UnitedGeoName, UnitedGeoNameAdmin)
admin.site.register(UnitedGeoNameSynonim, UnitedGeoNameSynonimAdmin)
admin.site.register(GeoNamesMatchingLogMatchedPlaces, GeoNamesMatchingLogMatchedPlacesAdmin)
admin.site.register(GeoNamesMatchingLogMatch, GeoNamesMatchingLogMatchAdmin)
admin.site.register(UserProject, UserProjectAdmin)
admin.site.register(UserGeoName)
admin.site.register(Database)
