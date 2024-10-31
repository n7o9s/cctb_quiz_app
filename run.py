import os
from app import create_app
from app.config import DevelopmentConfig
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Choose the appropriate configuration class
app = create_app(config_class=DevelopmentConfig)

if __name__ == "__main__":
    # Get port and host from environment variables, with defaults if not set
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 3000))

    # Run the Flask app on the specified host and port
    app.run(host=host, port=port)