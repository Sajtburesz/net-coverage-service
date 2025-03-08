from flask import Flask
from routes.coverage_routes import coverage_bp

app = Flask(__name__)
app.register_blueprint(coverage_bp)

if __name__ == "__main__":
    app.run(debug=True)
