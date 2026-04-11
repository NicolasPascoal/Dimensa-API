from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.ip_routes import ip_bp
    app.register_blueprint(ip_bp)

    return app