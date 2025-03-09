from helpers.get_insee_and_post_with_gps import get_insee_and_post_with_gps

class CoverageController:

    def get_citycode(self, lon, lat):
        return get_insee_and_post_with_gps(lon, lat)
