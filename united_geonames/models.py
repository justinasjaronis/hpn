# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.gis.db import models as gis_models

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from advanceddate import fields as date_fields
# import logging

from cities.models import City
from django.conf import settings
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from django.core.files.storage import FileSystemStorage
import os
from united_geonames.utils import get_centroid

fs_projects = FileSystemStorage(location=os.path.join(settings.PROJECT_DIR,  'attachments'))


class Database(models.Model):
    file = models.FileField(storage=fs_projects, upload_to='user_databases', blank=True, null=True,
                            verbose_name="Database file")
    email = models.CharField(max_length=255, null=True)
    information = models.TextField(blank=True)


class UserGeoName(models.Model):
    """
    Lentelė, kurią pildys išoriniai vartotojai iš Front-Endo.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    subregion = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=300, blank=True, null=True)
    coordinates = gis_models.PointField(null=True, blank=True, spatial_index=False)
    user = models.ForeignKey(User, null=True, blank=True)
    objects = gis_models.GeoManager()
    language = models.CharField(max_length=300, blank=True)
    temporal = date_fields.AdvancedDateField(related_name="user_geonames", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        super(UserGeoName, self).save(*args, **kwargs)


class UserProject(models.Model):
    """
    Kiekvienam projektui (Pleiades, Cities, Norway database ir pan - yra priskyriami žmonės kuravimui)
    """

    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(ContentType, null=True, blank=True)
    user = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class UnitedGeoName(models.Model):
    main_name = models.CharField(max_length=300, verbose_name=u'Main name')
    region = models.CharField(max_length=300, null=True, blank=True)
    subregion = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=300, blank=True, null=True)
    centroid = gis_models.PointField(null=True, blank=True, spatial_index=False)
    objects = gis_models.GeoManager()

    def __unicode__(self):
        return self.main_name

    def get_synonyms(self):
        return self.related_synonyms.all()


class UnitedGeoNameSynonim(models.Model):
    """
    SYNONIM - aruodų vietose tai pavadinimo varijantai, cities appse - tai alter names
    """
    united_geoname = models.ForeignKey(UnitedGeoName, null=True, related_name="related_synonyms")

    name = models.CharField(max_length=300, blank=True, verbose_name=u"Synonim Name")
    # original resource
    content_type = models.ForeignKey(ContentType, null=True, verbose_name=u'Original Source')
    object_id = models.PositiveIntegerField(null=True, verbose_name=u'Original place')
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    synonim_name = models.CharField(max_length=300, blank=True, verbose_name=u'Synonim name')
    synonim_content_type = models.ForeignKey(ContentType, null=True, blank=True,
                                             verbose_name=u'Original synonim source',
                                             related_name="synonim_content_type_set")
    synonim_object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Original synonim place')
    synonim_content_object = generic.GenericForeignKey('synonim_content_type', 'synonim_object_id')
    language = models.CharField(max_length=300, blank=True)
    temporal = date_fields.AdvancedDateField(related_name="temporal", blank=True, null=True)

    identifier = models.CharField(max_length=300, blank=True, verbose_name=u'Additional information')

    coordinates = gis_models.PointField(null=True, spatial_index=False)
    objects = gis_models.GeoManager()

    def __unicode__(self):
        return self.name

    def city_alt_names(self):
        from cities.models import AlternativeName
        cont_type_alt = ContentType.objects.get_for_model(AlternativeName)
        alter_names = self.content_object.alt_names.all()
        for alt_name in alter_names.iterator():
            obj, created = UnitedGeoNameSynonim.objects.get_or_create(name=alt_name.name,
                                                                      synonim_name=alt_name.name,
                                                                      synonim_object_id=alt_name.id,
                                                                      synonim_content_type=cont_type_alt,
                                                                      content_type=self.content_type,
                                                                      object_id=self.object_id,
                                                                      united_geoname=self.united_geoname,
                                                                      coordinates=self.coordinates,
                                                                      identifier='Alt. name')
            obj.save()

    def get_alter_language(self):
        from cities.models import AlternativeName
        alter_name = AlternativeName.objects.get(id=self.synonim_object_id)
        return alter_name.language

    @staticmethod
    def run_city_alt_names():
        """
        City Alt Names migravimas i sinonimus.

        Paleidimas:

        In [1]: from united_geonames.models import UnitedGeoNameSynonim
        In [2]: UnitedGeoNameSynonim.run_city_alt_names()

        """
        cont_type_city = ContentType.objects.get_for_model(City)
        ugnsinonims = UnitedGeoNameSynonim.objects.filter(content_type=cont_type_city)
        for ugnsinonim in ugnsinonims.iterator():
            ugnsinonim.city_alt_names()

    def get_project_name(self):
        project_name = self.content_type.app_label.title()
        if project_name == u'Cities':
            return "%s (%s)" % (u'Geo Names', 1034733)
        else:
            return project_name


class GeoNamesMatchingLogMatch(models.Model):

    start_date = models.DateTimeField(null=True, auto_now_add=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    model_matching = generic.GenericForeignKey('content_type', 'object_id')

    number_of_alternatives = models.IntegerField(null=True, blank=True)
    matching_index = models.FloatField(null=True, blank=True)

    display_for_users = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        from main.models.vietos.models import Vietos
        if self.content_type.id == 44:
            # TODO: automatizuoti uzhardcodinima. Taip nereikes importuoti aruodu i postgresql.
            return Vietos.objects.using('default').get(viid=self.object_id).pavadinimas

        if hasattr(self.model_matching, 'name'):
            return self.model_matching.name

        if hasattr(self.model_matching, 'title'):
            return self.model_matching.title

        if hasattr(self.model_matching, 'enh_snavn'):
            return self.model_matching.enh_snavn

        else:
            raise Exception("Not implemented")


    def get_places(self):
        return self.matched.all()

    class Meta:
        ordering = ['-matching_index']


class GeoNamesMatchingLogMatchedPlaces(models.Model):
    """
        Informacija apie kiekvieną atitinkanti (Matched) objektą
    """
    matchinglogmatch = models.ForeignKey(GeoNamesMatchingLogMatch, null=True, related_name='matched')
    united_geoname = models.ForeignKey(UnitedGeoName, null=True, blank=True)
    geographical_distance = models.FloatField(null=True, blank=True)
    ngram_distance = models.FloatField(null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    best_match = models.BooleanField(blank=True)

    def __unicode__(self):
        return unicode(self.matchinglogmatch)

    def get_matchinglogmatch_id(self):
        return unicode(self.matchinglogmatch.id)

    def get_synonyms(self):
        """
        Grazina visus MatchedPlace sinonimus.
        """
        return self.united_geoname.related_synonyms.all()


@receiver(post_save, sender=UnitedGeoNameSynonim)
def update_centroid(sender, instance, **kwargs):
    """
    On saving each UnitedGeoNameSynonym object this method gets all
    UnitedGeoNameSynonym objects in current UnitedGeoName and calculate
    centroid of each UnitedGeoNameSynonyms. Then writes centroid to table
    UnitedGeoName (column "centroid").
    """
    synonyms = instance.united_geoname.related_synonyms.all()
    coordinates = []
    for i in synonyms:
        if i.coordinates:
            coordinates.append(i.coordinates.tuple)

    centroid = get_centroid(coordinates)
    if centroid is not None:
        instance.united_geoname.centroid = centroid
        instance.united_geoname.save()
    else:
        # If matching place does not have coordinates
        # centroid is staying the same.
        pass


from django.contrib.auth.models import User as AuthUser, Group

def add_to_default_group(sender, instance, signal, *args, **kwargs):
    try:
        g = Group.objects.get(name='hpn_rest_group')
        # instance.is_staff = True
        g.user_set.add(instance)
    except:
        pass
    return instance

post_save.connect(add_to_default_group, sender=AuthUser)


