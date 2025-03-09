from flask import request, jsonify
from flask import Blueprint
from controllers.coverage_controller import CoverageController

coverage_bp = Blueprint("coverage", __name__)
coverage_controller = CoverageController()

@coverage_bp.route("/coverage", methods=['GET'])
def get_coverage():
    pass

@coverage_bp.route("/insee", methods=['GET'])
def get_insee_with_gps():
    lon = request.args.get("lon")
    lat = request.args.get("lat")

    res = coverage_controller.get_citycode(lon, lat)
    return jsonify({"insee": res})
