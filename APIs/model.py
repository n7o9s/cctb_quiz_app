from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

# Helper function to convert BSON ObjectId to string
def object_id_to_str(document):
    document['_id'] = str(document['_id'])
    return document