from extensions import db, bcrypt
from sqlalchemy import text, exc
from flask_jwt_extended import create_access_token


# SQL table creation
def create_user_tables():
    # User table
    user_table_sql = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(120) DEFAULT NULL,
            last_name VARCHAR(120) DEFAULT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL, 
            phone_number VARCHAR(20) DEFAULT NULL,
            address VARCHAR(256) DEFAULT NULL,
            city VARCHAR(120) DEFAULT NULL,
            postal_code VARCHAR(20) DEFAULT NULL,
            is_admin TINYINT(1) DEFAULT 0,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )ENGINE=InnoDB;
    """)
    with db.engine.begin() as connection:
        connection.execute(user_table_sql)

def create_product_tables():
    # catalogue tables
    product_table_sql = text("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category ENUM('Boards','Apparel','Gear') NOT NULL,
            product_name VARCHAR(120) NOT NULL,
            brand VARCHAR(120) NOT NULL,
            size VARCHAR(120) NOT NULL,
            colour VARCHAR(120),
            traction_colour VARCHAR(120),
            shape VARCHAR(120),
            quantity INT NOT NULL DEFAULT 0,
            price DECIMAL(6,2) NOT NULL DEFAULT 0.00,
            image VARCHAR(256),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )ENGINE=InnoDB;
    """)
    with db.engine.begin() as connection:
        connection.execute(product_table_sql)

def initialize_database():
    """Create user tables if they don't exist before the first request."""
    create_user_tables()
    create_product_tables()

### CRUD USER ###
#CREATE USER
def create_user(first_name, last_name, email, password, phone_number, address, city, postal_code):
    try:
        # Hashed the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Insert into users table
        user_sql = text("""
        INSERT INTO users (first_name, last_name, email, password, phone_number, address, city, postal_code) VALUES (:first_name, :last_name, :email, :password, :phone_number, :address, :city, :postal_code);
        """)

        db.session.execute(user_sql, {'first_name': first_name,'last_name': last_name,'' 'email': email, 'password': hashed_password, 'phone_number': phone_number, 'address': address, 'city': city, 'postal_code': postal_code})
        
        # Fetch the last inserted user_id
        user_id = db.session.execute(text('SELECT LAST_INSERT_ID();')).fetchone()[0] 

        db.session.commit()
        return user_id
    
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e   

#GET USER
def get_user_by_id(user_id):
    try:
        sql = text("SELECT id, first_name, last_name, email, password, phone_number, address, city, postal_code FROM users WHERE id = :user_id;")
        result = db.session.execute(sql, {'user_id': user_id})
        user = result.fetchone()

        # No need to commit() as no changes are being written to the database
        if user:
            # Convert the result into a dictionary if not None
            user_details = user._asdict()
            return user_details
        else:
            return None
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e

#UPDATE USER
def update_user_details(user_id, update_fields):
    try:
        # Dynamically build the SET part of the SQL query
        set_clause = ", ".join([f"{field} = :{field}" for field in update_fields.keys()])
        update_sql = text(f"""
        UPDATE users SET {set_clause}, modified_at = CURRENT_TIMESTAMP WHERE id = :user_id;
        """)
        
        # Add user_id to the parameters
        params = update_fields.copy()
        params['user_id'] = user_id
        
        db.session.execute(update_sql, params)
        db.session.commit()
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e

### CRUD PRODUCT ###
# Create product
def create_product(category, product_name, brand, size, colour, traction_colour, shape, quantity, price, image_path):
    try: 
        product_table_sql = text("""
        INSERT INTO products (category, product_name, brand, size, colour, traction_colour, shape, quantity, price, image) VALUES (:category, :product_name, :brand, :size, :colour, :traction_colour, :shape, :quantity, :price, :image);
        """)
        db.session.execute(product_table_sql, {'category': category, 'product_name' : product_name, 'brand' : brand, 'size' : size, 'colour' : colour, 'traction_colour' : traction_colour, 'shape' : shape, 'quantity' : quantity, 'price' : price, 'image': image_path})
        product_id = db.session.execute(text('SELECT LAST_INSERT_ID();')).fetchone()[0] 

        db.session.commit()
        return product_id
    
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e   

def get_product_by_id(product_id):
    try:
        sql = text("SELECT id, category, product_name, brand, size, colour, traction_colour, shape, quantity, price, image FROM products WHERE id = :product_id;")
        result = db.session.execute(sql, {'product_id': product_id})
        products = result.fetchone()

        # No need to commit() as no changes are being written to the database
        if products:
            # Convert the result into a dictionary if not None
            product_details = products._asdict()
            return product_details
        else:
            return None
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e
    
def update_product_details(product_id, update_fields):
    try:
        # Dynamically build the SET part of the SQL query
        set_clause = ", ".join([f"{field} = :{field}" for field in update_fields.keys()])
        update_sql = text(f"""
        UPDATE products SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = :product_id;
        """)
        
        # Add product_id to the parameters
        params = update_fields.copy()
        params['product_id'] = product_id
        
        db.session.execute(update_sql, params)
        db.session.commit()
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e