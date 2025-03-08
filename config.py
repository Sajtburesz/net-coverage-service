import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://coverage_user:coverage_password@localhost/coverage_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
