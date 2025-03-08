from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Flask is running with Gunicorn!"}

if __name__ == "__main__":
    app.run(debug=True)
