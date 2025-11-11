import os
from flask import Flask, request, jsonify
from config import Config, DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from models import db, initialize_database
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

## Below library not yet track
from sqlalchemy import create_engine, Integer, String, TIMESTAMP, func, select
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
CORS(app)

#config_class='DevelopmentConfig'
config_class = os.getenv('FLASK_CONFIG', 'DevelopmentConfig')
app.config.from_object(f'config.{config_class}')
jwt = JWTManager()

# UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = app.config.get('UPLOAD_FOLDER', 'static/images')
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
jwt.init_app(app)

with app.app_context():
    initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

#Hello world
@app.route("/")
def hello():
    return "Hello, World!"