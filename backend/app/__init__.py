from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # Database Configuration - MySQL only (XAMPP compatible)
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'login_system')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to False for localhost HTTP
    app.config['SESSION_COOKIE_DOMAIN'] = None  # Let Flask set domain automatically
    app.config['SESSION_COOKIE_PATH'] = '/'
    # Initialize CORS for frontend server only
    CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:8080', 'http://127.0.0.1:8080'], allow_headers="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models
    from app.models import User
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Handle both old integer IDs (for backward compatibility) and new string IDs
        try:
            # Try to get user by user_id (string)
            return User.query.filter_by(user_id=user_id).first()
        except:
            # Fallback for any errors
            return None
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Register internships blueprint
    try:
        from app.internships_routes import internships_bp
        app.register_blueprint(internships_bp)
    except ImportError as e:
        print(f"Warning: Could not import internships blueprint: {e}")
    
    # Register company blueprint
    try:
        from app.company_routes import company_bp
        app.register_blueprint(company_bp)
    except ImportError as e:
        print(f"Warning: Could not import company blueprint: {e}")
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app