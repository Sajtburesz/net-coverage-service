from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
from db import db
from routes.coverage_routes import coverage_bp
from config import Config
import models

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)

app.register_blueprint(coverage_bp)
swagger = Swagger(app)

if __name__ == "__main__":
    app.run(debug=True)
