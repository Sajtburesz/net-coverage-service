from helpers.get_insee_and_post_with_gps import get_insee_and_post_with_gps
from flask import jsonify
class CoverageController:

    def get_citycode(self, lon, lat):
        insee, post =  get_insee_and_post_with_gps(lon, lat)
        return jsonify({"insee": insee, "post": post})