from sqlalchemy import UniqueConstraint

from db import db

class NetworkCoverage(db.Model):
    __tablename__ = "network_providers_coverage"

    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.Integer, nullable=False)
    insee_code = db.Column(db.Integer, nullable=False)
    post_code = db.Column(db.Integer, nullable=False)
    type_2g = db.Column(db.Boolean, nullable=False, default=False)
    type_3g = db.Column(db.Boolean, nullable=False, default=False)
    type_4g = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (UniqueConstraint('operator', 'insee_code', 'post_code','type_2g','type_3g','type_4g', name='unique_coverage_data'),)
