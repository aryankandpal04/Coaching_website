from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
cache = Cache()

def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the default configuration
    if config_name == "development":
        app.config.from_object("config.DevelopmentConfig")
    elif config_name == "testing":
        app.config.from_object("config.TestingConfig")
    elif config_name == "production":
        app.config.from_object("config.ProductionConfig")
    
    # Load instance config
    app.config.from_pyfile("config.py", silent=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    
    # Configure login manager
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.teacher import teacher_bp
    from app.routes.student import student_bp
    from app.routes.parent import parent_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(teacher_bp, url_prefix="/teacher")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(parent_bp, url_prefix="/parent")
    
    return app 