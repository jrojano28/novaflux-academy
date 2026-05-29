# app/services/auth_service.py
# Servicio de Autenticación: Lógica de registro, inicio de sesión y gestión de usuarios.

from app.models import db
from app.models.user import User

class AuthService:
    @staticmethod
    def register_user(username, email, password, confirm_password):
        """
        Registra un nuevo usuario en el sistema.
        Retorna (exito, mensaje, usuario_creado)
        """
        username = username.strip()
        email = email.strip().lower()

        if not all([username, email, password, confirm_password]):
            return False, "Por favor, completa todos los campos.", None

        if password != confirm_password:
            return False, "Las contraseñas no coinciden.", None

        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres.", None

        # Verificar si el correo ya está registrado
        if User.query.filter_by(email=email).first():
            return False, "Este correo electrónico ya está registrado.", None

        # Verificar si el nombre de usuario ya está en uso
        if User.query.filter_by(username=username).first():
            return False, "Este nombre de usuario ya está en uso.", None

        # Crear el nuevo usuario con rol de estudiante por defecto
        try:
            new_user = User(username=username, email=email, role='student')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return True, "¡Cuenta creada con éxito! Ya puedes iniciar sesión.", new_user
        except Exception as e:
            db.session.rollback()
            return False, f"Error al crear el usuario en la base de datos: {str(e)}", None

    @staticmethod
    def authenticate_user(email, password):
        """
        Valida las credenciales de un usuario.
        Retorna (exito, mensaje, usuario)
        """
        email = email.strip().lower()
        if not email or not password:
            return False, "Por favor, completa ambos campos.", None

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return True, f"¡Bienvenido de vuelta, {user.username}!", user
        else:
            return False, "Correo o contraseña incorrectos. Verifica tus datos.", None
