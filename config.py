import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://coverage_user:coverage_password@localhost/coverage_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # For sake of simplicity I pushed the csv data to git but generally upon startup it should be provided and configured
    CSV_COVERAGE_DATA_PATH = os.getenv("CSV_COVERAGE_DATA_PATH", "./static/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv")