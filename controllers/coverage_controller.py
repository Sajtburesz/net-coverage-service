from flask_sqlalchemy import SQLAlchemy

from helpers.geo_coding_helper import GeoCodingHelper
from models import NetworkCoverage

class CoverageController:

    def __init__(self, geo_coding_helper: GeoCodingHelper, db: SQLAlchemy):
        self.geo_coding_helper = geo_coding_helper
        self.db = db

    def coverage_check(self, params: dict):

        address = params.get("q")
        lon, lat = params.get("lon"), params.get("lat")

        if lon and lat and not address:
            try:
                insee, post = self.geo_coding_helper.get_insee_and_post_with_gps(float(lon), float(lat))
            except ValueError:
                raise ValueError("Longitude and Latitude must be valid numbers.")
        else:
            insee, post = self.geo_coding_helper.get_insee_and_post_with_address(address)

        coverage_records = self.db.session.execute(
            self.db.select(NetworkCoverage).filter_by(
                insee_code=insee,
                post_code=post
            )
        ).scalars().all()

        coverage_by_operator = {}
        for record in coverage_records:
            operator_name = record.provider.operator_name

            if operator_name not in coverage_by_operator:
                coverage_by_operator[operator_name] = {
                    "2G": record.type_2g,
                    "3G": record.type_3g,
                    "4G": record.type_4g
                }
            else:
                coverage_by_operator[operator_name]["2G"] |= record.type_2g
                coverage_by_operator[operator_name]["3G"] |= record.type_3g
                coverage_by_operator[operator_name]["4G"] |= record.type_4g

        return coverage_by_operator
