import os
from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def root():
        return jsonify({"status": "ok", "env": os.getenv("APP_ENV", "dev")})

    return app
