from flask import Flask
from flask_cors import CORS
from .mongo import mongo

def create_app(config_class=None):
    # Create the Flask app
    app = Flask(__name__)

    # Apply configuration from the given class
    if config_class:
        app.config.from_object(config_class)

    # Initialize MongoDB
    mongo.init_app(app)

    # Enable CORS for React app
    CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5173", "http://localhost:5173"]}})

    # Register blueprints/routes
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app