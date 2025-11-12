from extensions import db, bcrypt
from sqlalchemy import text, exc
from flask_jwt_extended import create_access_token


# SQL table creation
def create_user_tables():
    # User table
    user_table_sql = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(120) UNIQUE NOT NULL,
            phone_number VARCHAR(20) DEFAULT NULL,
            password VARCHAR(64) NOT NULL, 
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )ENGINE=InnoDB;
    """)
    with db.engine.begin() as connection:
        connection.execute(user_table_sql)


def initialize_database():
    """Create user tables if they don't exist before the first request."""
    create_user_tables()

    ### CRUD USER ###
#CREATE USER
def create_user(email, phone_number, password):
    try:
        # Hashed the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Insert into users table
        user_sql = text("""
        INSERT INTO users (email, phone_number, password) VALUES (:email, :phone_number, :password);
        """)

        db.session.execute(user_sql, {'email': email, 'phone_number': phone_number, 'password': hashed_password})
        
        # Fetch the last inserted user_id
        user_id = db.session.execute(text('SELECT LAST_INSERT_ID();')).fetchone()[0] 

        db.session.commit()
        return user_id
    
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        raise e   

def get_user_by_id(user_id):
    try:
        sql = text("SELECT id, email, phone_number, password FROM users WHERE id = :user_id;")
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
