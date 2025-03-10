import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://coverage_user:coverage_password@localhost/coverage_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # For sake of simplicity I pushed the csv data to git but generally upon startup it should be provided and configured
    CSV_COVERAGE_DATA_PATH = os.getenv("CSV_COVERAGE_DATA_PATH", "./static/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv")
    CSV_PROVIDERS_DATA_PATH = os.getenv("CSV_PROVIDERS_DATA_PATH", "./static/France_network_providers.csv")

    # Convert LOAD_CSV_DATA to bool, default to False
    LOAD_CSV_DATA = os.getenv("LOAD_CSV_DATA", "").lower() in {"true", "1", "yes"}

    # Convert DB_INSERT_BATCH_SIZE to int, default to 100
    try:
        DB_INSERT_BATCH_SIZE = int(os.getenv("DB_INSERT_BATCH_SIZE", 100))
    except ValueError:
        DB_INSERT_BATCH_SIZE = 100