import os
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_mongo(app):
    """Initialize MongoDB connection with app context."""
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/webhook_db')
    app.config['MONGO_URI'] = mongo_uri
    mongo.init_app(app)
    return mongo
