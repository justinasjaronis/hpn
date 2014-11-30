from united_geonames.models import UserGeoName
from united_geonames.plugins.default import UnitedGeoNamePlugin


class UserGeoNamePlugin(UnitedGeoNamePlugin):
    class Meta:
        model = UserGeoName
