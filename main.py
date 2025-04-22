from flask import Flask
from routes import register_all_routes
from flask_cors import CORS

app = Flask(__name__)
register_all_routes(app)
CORS(app, origins=["http://localhost:3000"])


if __name__ == "__main__":
    app.run(debug=True)
