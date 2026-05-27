# app/config.py
# Configuración del entorno de la aplicación Flask y base de datos SQLite.

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_anti_gravity_2026'
    # Base de datos SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///plataforma.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
