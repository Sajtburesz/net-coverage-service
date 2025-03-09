import multiprocessing
import time
from flask import Flask
from flask_migrate import Migrate, upgrade
from db import db
from helpers.data_loader import DataLoader
from models import NetworkCoverage
from config import Config
from transformers.network_coverage_transformer import transform_network_coverage
import models


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)


def apply_migrations():
    with app.app_context():
        print("Checking for pending migrations...")
        upgrade()


def load_data():

    with app.app_context():

        data_loader = DataLoader()

        print("Loading network coverage csv...")
        data_loader.load_csv(
            csv_path="static/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv",
            model=NetworkCoverage,
            unique_keys=["operator", "insee_code", "post_code"],
            transform_functions=[transform_network_coverage]
        )


if __name__ == "__main__":
    time.sleep(15)
    apply_migrations()

    process = multiprocessing.Process(target=load_data)
    process.start()