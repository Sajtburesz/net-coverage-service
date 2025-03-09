from helpers import get_insee_with_gps

class CoverageController:

    def get_citycode(self, lon, lat):
        return get_insee_with_gps(lon, lat)
