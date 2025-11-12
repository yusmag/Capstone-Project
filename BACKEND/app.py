import os
from flask import Flask, request, jsonify, render_template
from config import Config, DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from models import db, initialize_database, create_user, get_user_by_id
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

#Hello world
@app.route("/")
def hello():
    return "Hello, World!"

#REGISTER OR CREATE AN USER
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')  
    phone_number = data.get('phone_number')
    
    try:
        user_id = create_user(email, phone_number, password)
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    
    except Exception as e:
        # Handle errors and conflicts, such as a duplicate username
        return jsonify({"error": "User creation failed", "details": str(e)}), 400
    

@app.route('/user/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404
 
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


