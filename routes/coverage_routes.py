from flask import request, jsonify
from flask import Blueprint
from controllers.coverage_controller import CoverageController
from exceptions.GeoCodingExceptions import BaseGeoCodingException
from helpers.geo_coding_helper import GeoCodingHelper
from db import db

coverage_bp = Blueprint("coverage", __name__)
coverage_controller = CoverageController(GeoCodingHelper(), db)

@coverage_bp.errorhandler(BaseGeoCodingException)
def handle_base_geocoding_exception(err):
    return jsonify({
        "error": str(err)
    }), 400

ALLOWED_COVERAGE_PARAMS = {'q', 'lon', 'lat'}
@coverage_bp.route("/coverage", methods=['GET'])
def get_coverage():
    query_params = set(request.args.keys())
    disallowed_params = query_params - ALLOWED_COVERAGE_PARAMS
    if disallowed_params:
        return jsonify({
            'error': 'Invalid query parameters',
            'disallowed_params': list(disallowed_params)
        }), 400
    try:
        params = {}
        if "q" in query_params:
            params["q"] = request.args.get("q")

        if "lon" in query_params and "lat" in query_params:
            params["lon"] = request.args.get("lon")
            params["lat"] = request.args.get("lat")

        if params:
            coverage_data = coverage_controller.coverage_check(params)
            return jsonify(coverage_data)

        return jsonify({
            'error': 'Necessary query parameters are missing to perform search'
        }), 400
    except Exception as err:
        return jsonify({
            "error": str(err)
        }), 400

