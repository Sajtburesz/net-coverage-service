import time

from flask import Flask
from flask_migrate import Migrate, upgrade
from db import db
from helpers.data_loader import DataLoader
from models import NetworkCoverage
from routes.coverage_routes import coverage_bp
from config import Config
import asyncio
from transformers.network_coverage_transformer import transform_network_coverage
import models

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)


time.sleep(10)
with app.app_context():
    print("Checking for pending migrations...")
    upgrade()

    print("Loading csv...")

    data_loader = DataLoader()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_loader.load_csv(
        csv_path="static/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv",
        model=NetworkCoverage,
        unique_keys=["operator", "insee_code"],
        transform_functions=[transform_network_coverage]
    ))

app.register_blueprint(coverage_bp)

if __name__ == "__main__":
    app.run(debug=True)
