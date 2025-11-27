import os
from flask import Flask, request, jsonify, render_template
from config import Config, DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from models import db, initialize_database, create_user, get_user_by_id, create_product, get_product_by_id
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

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

# Catalogue folder
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#CATEGORIES = {"Apparel", "Boards", "Gears"}

def _ext_ok(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
    
#GET USER
@app.route('/user/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404
 

#REGISTER A PRODUCT
@app.route('/products', methods=['POST'])
def register_product():
    data = request.get_json(silent=True) or request.form.to_dict()
    category = (data.get('category') or "").strip()
    product_name = (data.get('product_name') or "").strip()
    brand = (data.get('brand') or "").strip()
    size  = (data.get('size') or "").strip()
    colour = (data.get('colour') or "").strip()
    traction_colour = (data.get('traction_colour') or "").strip()
    shape = (data.get('shape') or "").strip()
    quantity = (data.get('quantity') or "").strip()
    price = (data.get('price') or "").strip()
    
    image_path = None
    file = request.files.get("image") 
    if file and file.filename: 
        if not _ext_ok(file.filename):
            return jsonify({"error": "Unsupported image type"}), 415
        fname = secure_filename(file.filename)
        save_dir = os.path.join(ASSETS_DIR, category)
        os.makedirs(save_dir, exist_ok=True)
        full_path = os.path.join(save_dir, fname)
        file.save(full_path)
        image_path = f"/assets/{category}/{fname}"
    else:
        # If client passed a URL/path in text field 'image'
        img_text = (data.get("image") or "").strip()
        if img_text:
            image_path = img_text  # e.g., "/assets/Boards/board1.jpg"

    try:
        product_id = create_product(category, product_name, brand, size, colour, traction_colour, shape, quantity, price, image_path)
        return jsonify({"message": "Product created successfully", "product_id": product_id}), 201
    
    except Exception as e:
        # Handle errors and conflicts, such as a duplicate username
        return jsonify({"error": "Product creation failed", "details": str(e)}), 400
    
#GET PRODUCT DETAILS
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


