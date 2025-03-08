from crypt import methods

from flask import Blueprint
from controllers.coverage_controller import CoverageController

coverage_bp = Blueprint("coverage", __name__)

@coverage_bp.route("/coverage", methods=['GET'])
def get_coverage():
    pass

