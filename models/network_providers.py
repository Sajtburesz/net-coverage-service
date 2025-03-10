from sqlalchemy.orm import relationship

from db import db

class NetworkProviders(db.Model):
    __tablename__ = "network_providers"

    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.Integer, nullable=False)
    operator_name = db.Column(db.String(50), nullable=False)

    coverages = relationship("NetworkCoverage", back_populates="provider", lazy=True)