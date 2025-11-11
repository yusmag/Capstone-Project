from sqlalchemy import text, exc
from flask_jwt_extended import create_access_token

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def initialize_database():
    """Create user tables if they don't exist before the first request."""