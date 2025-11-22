from flask import Flask
from flask_bootstrap import Bootstrap
from .routes import main
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    Bootstrap(app)
    
    # Initialize database
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(main)

    return app
