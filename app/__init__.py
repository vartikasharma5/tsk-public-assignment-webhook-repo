from flask import Flask, render_template
from flask_cors import CORS

from app.extensions import init_mongo
from app.webhook.routes import webhook, api


def create_app():
    """Application factory for Flask app."""
    app = Flask(__name__)
    
    CORS(app)
    
    init_mongo(app)
    
    app.register_blueprint(webhook)
    app.register_blueprint(api)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
