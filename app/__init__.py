# app/__init__.py
# Inicialización de la aplicación Flask, base de datos y registro de controladores.

from flask import Flask
from app.config import Config
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)

    # Inicializar Base de Datos SQLAlchemy
    db.init_app(app)

    # Registro de Blueprints de Enrutamiento
    from app.routes import main_bp, auth_bp, course_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)

    return app
