import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from config import Config, DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from models import db, initialize_database, create_user, get_user_by_id, update_user_details, create_product, get_product_by_id, update_product_details
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from decimal import Decimal, InvalidOperation

## Below library not yet track
from sqlalchemy import create_engine, Integer, String, TIMESTAMP, func, select, text
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
# app.config['UPLOAD_FOLDER'] = app.config.get('UPLOAD_FOLDER', 'static/images')
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Upload folder
#os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Product Catalogue folder
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
CATEGORIES = {"Apparel", "Boards", "Gears"}

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
for cat in CATEGORIES:
    os.makedirs(os.path.join(ASSETS_DIR, cat), exist_ok=True)


def _ext_ok(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/assets/<path:filename>")
def server_asset(filename):
    return send_from_directory(ASSETS_DIR, filename, as_attachment=False)

#file handling
# INSERT FILE HANDLING FUNCTION HERE


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
    data = request.get_json(silent=True) or request.form.to_dict()
    first_name = (data.get('first_name') or "").strip()
    last_name = (data.get('last_name') or "").strip()
    email = data.get('email') or "".strip()
    password = data.get('password') or "".strip()
    phone_number = data.get('phone_number') or "".strip()
    address = data.get('address') or "".strip()
    city = data.get('city') or "".strip()
    postal_code = data.get('postal_code') or "".strip()
    
     # Basic validation for required fields
    if not first_name or not last_name or not email or not password:
        return jsonify({"error": "First name, last name, email, and password are required"}), 400       

    try:
        user_id = create_user(first_name, last_name, email, password, phone_number, address, city, postal_code)
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
    
#UPDATE USER DETAILS
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):  
    data = request.get_json()
    update_fields = {}
    allowed_fields = {"first_name", "last_name", "email", "password", "phone_number", "address", "city", "postal_code"}
    
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field].strip() if isinstance(data[field], str) else data[field]
    
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    
    try:
        updated_user = update_user_details(user_id, update_fields)
        if updated_user:
            return jsonify({"message": "User updated successfully", "user": updated_user}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "User update failed", "details": str(e)}), 400
 

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
    decscription = (data.get('description') or "").strip()
    price = Decimal(data.get("price") or "0.00")
    
    if category not in CATEGORIES:
        return{"error": f"Invalid category. Use one of {sorted(CATEGORIES)}"}, 422
    
    # file upload handling
    image_path = None
    file = request.files.get('image') 
    if file and file.filename: 
        if not _ext_ok(file.filename):
            return jsonify({"error": "Unsupported image type"}), 415
        fname = secure_filename(file.filename)
        save_dir = os.path.join(ASSETS_DIR, category)
        os.makedirs(save_dir, exist_ok=True)
        full_path = os.path.join(save_dir, fname)
        file.save(full_path)
        image_path = f"/assets/{category}/{fname}"
    if not image_path and data.get("image"):
            image_path = data["image"].strip()
    
    #debugging purpose
    #app.logger.info("create product image_path=%s", image_path)

    try:
        product_id = create_product(category, product_name, brand, size, colour, traction_colour, shape, quantity, decscription, price, image_path)
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


#HELPER FUNCTION TO UPDATE PRODUCT DETAILS
UPDATABLE_FIELDS = {
    "category", "product_name", "brand", "size", "colour", "traction_colour", "shape", "quantity", "description", "price", "image"
}

ALLOWED_EXT = {"jpg", "jpeg", "png", "webp", "gif"}

def _ext_ok(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def _to_int(v, default=None):
    try: return int(v)
    except Exception: return default

def _to_decimal(v, default=None):
    try: return Decimal(str(v))
    except (InvalidOperation, TypeError, ValueError): return default

@app.get("/assets/<path:filename>")
def serve_asset(filename):
    return send_from_directory(ASSETS_DIR, filename, as_attachment=False)



#UPDATE PRODUCT DETAILS
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    # Accept JSON or form-data
    data = request.get_json(silent=True) or request.form.to_dict()

    # Start with incoming fields (ignore unknowns later)
    fields = {
        "category": (data.get("category") or "").strip() or None,
        "product_name": (data.get("product_name") or "").strip() or None,
        "brand": (data.get("brand") or "").strip() or None,
        "size": (data.get("size") or "").strip() or None,
        "colour": (data.get("colour") or "").strip() or None,
        "traction_colour": (data.get("traction_colour") or "").strip() or None,
        "shape": (data.get("shape") or "").strip() or None,
        "quantity": _to_int(data.get("quantity"), None),
        "description": (data.get("description") or "").strip() or None,
        "price": _to_decimal(data.get("price"), None),
        "image": (data.get("image") or "").strip() or None,
    }

    # If category is provided, validate against your enum
    if fields["category"] is not None and fields["category"] not in CATEGORIES:
        return jsonify({"error": f"Invalid category. Use one of {sorted(CATEGORIES)}"}), 422

    # Optional: handle image file upload (form-data key 'image')
    # If a file is provided, it overrides any 'image' text value.
    file = request.files.get("image")
    if file and file.filename:
        if not _ext_ok(file.filename):
            return jsonify({"error": "Unsupported image type"}), 415
        # Save to assets/<Category or existing category>/<filename>
        # Prefer new category if supplied; otherwise we need the current category from DB.
        target_category = fields["category"]
        if target_category is None:
            # fetch current category
            cur = db.session.execute(text("SELECT category FROM products WHERE id=:id"), {"id": product_id}).scalar()
            if not cur:
                return jsonify({"error": "Product not found"}), 404
            target_category = cur

        save_dir = os.path.join(ASSETS_DIR, target_category)
        os.makedirs(save_dir, exist_ok=True)
        fname = secure_filename(file.filename)
        file.save(os.path.join(save_dir, fname))
        fields["image"] = f"/assets/{target_category}/{fname}"

    try:
        updated = update_product_details(product_id, fields)
        if not updated:
            return jsonify({"error": "Product not found or nothing to update"}), 404
        return jsonify({"message": "Product updated", "product": updated}), 200
    except Exception as e:
        return jsonify({"error": "Update failed", "details": str(e)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


