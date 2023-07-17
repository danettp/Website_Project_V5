from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__) # Create a Flask application instance
    app.config['SECRET_KEY'] = "helloworld" # Secret key for session security
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # Initialize the SQLAlchemy database
    
    from .views import views # (Relative) import inside the python package
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/") # Register the views Blueprint with the application
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Post, Comment, Like
    
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Created Database!")
        
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # Redirects to Login page
    login_manager.init_app(app) # Initialize the LoginManager with the application
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app # Return the created application instance