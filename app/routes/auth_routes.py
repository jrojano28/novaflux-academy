# app/routes/auth_routes.py
# Rutas de Autenticación: Define endpoints para registro, login y logout.

from flask import Blueprint
from app.controllers import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Vista e inicio de sesión."""
    return AuthController.login()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Vista y registro de nuevos usuarios."""
    return AuthController.register()

@auth_bp.route('/logout')
def logout():
    """Cierra la sesión del usuario actual."""
    return AuthController.logout()
