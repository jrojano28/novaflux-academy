# app/controllers/__init__.py
# Exportación de las clases controladoras y decoradores del sistema.

from app.controllers.auth_controller import AuthController, login_required, role_required
from app.controllers.main_controller import MainController
