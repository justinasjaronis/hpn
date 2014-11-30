from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from .views import matched_logs, new_user_geoname, MatchedObjectDetailApiView, UserGeoNameSearchApiDetail, UserGeoNameApiDetail, send_database, ExampleView

urlpatterns = \
    patterns('',
             url(r'^unitedgeo/user-form/$', new_user_geoname, name='new_user_geoname'),
             url(r'^unitedgeo/database-form/$', send_database, name='send_database'),
             url(r'^unitedgeo/matched_object/(?P<matching_id>\d+)/$', matched_logs, name='log_object'),

             url(r'^api/hpn/example/$', ExampleView.as_view()),
             url(r'^api/hpn/$', UserGeoNameApiDetail.as_view()),
             url(r'^api/hpn/search/$', UserGeoNameSearchApiDetail.as_view()),
             url(r'^api/hpn/matched_object/(?P<matching_log_id>\d+)/$', MatchedObjectDetailApiView.as_view()),

             url(r'^unitedgeo/thanks/', direct_to_template, {'template': 'united_geonames/thank_you.html'}),)
