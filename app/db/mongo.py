# Handle your connection, queries, and other database functions.

from flask_pymongo import PyMongo

# Initialize the PyMongo extension
mongo = PyMongo()

def init_db(app):
    """Initialize the database with the Flask app."""
    mongo.init_app(app)

    # Access the specific database using the database name from config
    db_name = app.config['MONGO_DATABASE']
    mongo.db = mongo.cx[db_name]  # Explicitly set the database
    
    print("Connected from MongoDB.")

def disconnect():
    """Disconnect from the MongoDB database."""
    try:
        # Close the connection if it exists
        if hasattr(mongo, 'client'):
            mongo.client.close()
            print("Disconnected from MongoDB.")
    except Exception as e:
        print(f"Error while disconnecting from MongoDB: {e}")

# Helper function to convert BSON ObjectId to string
def object_id_to_str(document):
    document['_id'] = str(document['_id'])
    return document