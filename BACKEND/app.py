import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from config import Config, DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from models import db, initialize_database, create_user, get_user_by_id, create_product, get_product_by_id
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from decimal import Decimal

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


#HELPER FUNCTION TO UPDATE PRODUCT DETAILS
UPDATATABLE_FIELDS = {
    "category", "product_name", "brand", "size", "colour", "traction_colour", "shape", "quantity", "price", "image"
}


def _to_int(v):
    try: 
        return int(v)
    except Exception:
        return None
    
def _to_dec(v):
    try:
        return Decimal(v)
    except Exception:
        return None
    
def _cleaned_updates_from_form(form) -> dict[str, any]:
    """"Return only non-empty fields(no '', no whitespace)"""
    updates: dict[str, any] = {}
    for k, v in form.items():
        if v is None:
            continue
        v2 = v.strip()
        if v2 == "":
            continue
        updates[k] = v2
    return updates

#UPDATE PRODUCT DETAILS
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    #JSON or FORM data
    data = request.get_json(silent=True)
    if data is None:
        data = _cleaned_updates_from_form(request.form) # run function to clean form data

    candidate = {
        "category": data.get("category") or None,
        "product_name": data.get("product_name") or None,
        "brand": data.get("brand") or None,
        "size": data.get("size") or None,
        "colour": data.get("colour") or None,
        "traction_colour": data.get("traction_colour") or None,
        "shape": data.get("shape") or None,
        "quantity": _to_int(data.get("quantity")) if "quantity" in data else None,
        "price": _to_dec(data.get("price")) if "price" in data else None,
        "image": (data.get("image") or None) if "image" in data else None,
    }
    #drop any keys if no value
    fields = {k: v for k, v in candidate.items() if v is not None and k in UPDATATABLE_FIELDS}

    #verify category if any
    if "category" in fields and fields["category"] not in CATEGORIES:
        return jsonify({"error": f"Invalid category. Use one of {sorted(CATEGORIES)}"}), 422
    
    # file upload handling
    image_path = None
    file = request.files.get('image') 
    if file and file.filename: 
        if not _ext_ok(file.filename):
            return jsonify({"error": "Unsupported image type"}), 415
        target_category = fields.get("category")
        if not target_category:
            row = db.session.execute(
                text("SELECT category FROM products WHERE id=:id"),
                {"id":product_id}
            ).first()
            if not row:
                return jsonify({"error": "Product not found"}), 404
            target_category = row[0]

        os.makedirs(os.path.join(ASSETS_DIR, target_category), exist_ok=True)
        fname = secure_filename(file.filename)
        file.save(os.path.join(ASSETS_DIR, target_category, fname))
        fields["image"] = f"/assets/{target_category}/{fname}"

        # IF NOTHING TO UPDATE
        if not fields:
            current = db.session.execute(text("""
                SELECT id, category, product_name, brand, size, colour, traction_colour, shape, quantity, price, image, created_at, update_at
                FROM products WHERE id=:id
                """), {"id":product_id}).mappings().first()
            if not current:
                return jsonify({"error": "Product not found"}), 404
            d = dict(current)
            if d.get("price") is not None: d["price"] = str(d["price"])
            return jsonify({"message": "No changes", "product":d}), 200
    set_clause = ", ".join(f"{col} = :{col}" for col in fields.keys())
    sql = text(f"""
        UPDATE products
        SET {set_clause}, update_at=CURRENT_TIMESTAMP
        WHERE id = :id
    """)
    params = {"id": product_id, **fields}

    try:
        res = db.session.execute(sql, params)
        if res.rowcount == 0:
            db.session.rollback()
            return jsonify({"error": "Product not found"}), 404

        row = db.session.execute(text("""
            SELECT id, category, product_name, brand, size, colour, traction_colour,
                   shape, quantity, price, image, created_at, update_at
            FROM products WHERE id=:id
        """), {"id": product_id}).mappings().one()

        db.session.commit()

        out = dict(row)
        if out.get("price") is not None:
            out["price"] = str(out["price"])  # JSON-safe for DECIMAL
        return jsonify({"message": "Product updated", "product": out}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Update failed", "details": str(e)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


