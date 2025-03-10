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
    }), 404

@coverage_bp.errorhandler(Exception)
def handle_general_exception(err):
    return jsonify({
        "error": str(err)
    }), 400

ALLOWED_COVERAGE_PARAMS = {'q', 'lon', 'lat'}
@coverage_bp.route("/coverage", methods=['GET'])
def get_coverage():
    """
    Retrieve coverage hints using an address (which can be an approximate point of interest) or GPS coordinates (Longitude, Latitude).
    ---
    parameters:
      - name: q
        in: query
        type: string
        description: An address.
      - name: lon
        in: query
        type: number
        format: float
        description: Longitude.
      - name: lat
        in: query
        type: number
        format: float
        description: Latitude.
    responses:
      200:
        description: A dictionary of providers and their network availability.
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              2G:
                type: boolean
                description: Indicates if 2G is available for the provider.
              3G:
                type: boolean
                description: Indicates if 3G is available for the provider.
              4G:
                type: boolean
                description: Indicates if 4G is available for the provider.
        examples:
          application/json:
            orange:
              2G: true
              3G: true
              4G: false
            SFR:
              2G: true
              3G: true
              4G: true
      404:
        description: In case no Geocoding location was found.
      400:
        description: In case input parameters were faulty.
    """

    query_params = set(request.args.keys())
    disallowed_params = query_params - ALLOWED_COVERAGE_PARAMS
    if disallowed_params:
        return jsonify({
            'error': 'Invalid query parameters',
            'disallowed_params': list(disallowed_params)
        }), 400

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


