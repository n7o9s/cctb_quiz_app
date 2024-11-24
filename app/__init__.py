from flask import Flask
from flask_cors import CORS
from app.config import DevelopmentConfig
from .db.mongo import init_db, disconnect

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    # Allow CORS for all domains on all routes.
    cors = CORS(app)

    # Load configuration from the provided class
    app.config.from_object(config_class)

    # Initialize the database
    init_db(app)

    # Register the disconnect function on app teardown
    @app.teardown_appcontext
    def close_db(exception):
        disconnect()

    # Import routes and register them
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app