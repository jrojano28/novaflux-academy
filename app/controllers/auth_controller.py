# app/controllers/auth_controller.py
# Controlador de Autenticación: Maneja las peticiones HTTP y delega al AuthService.

from functools import wraps
from flask import render_template, request, redirect, url_for, session, flash
from app.services.auth_service import AuthService

# ─── DECORADORES DE ACCESO POR ROLES ──────────────────────────────────────────

def login_required(f):
    """Decorador: Requiere que el usuario tenga sesión activa."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """Decorador: Requiere que el usuario tenga uno de los roles especificados."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión para acceder.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('user_role') not in roles:
                flash('No tienes permiso para acceder a esta sección.', 'danger')
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated
    return decorator


# ─── CLASE CONTROLADORA PRINCIPAL ─────────────────────────────────────────────

class AuthController:
    @staticmethod
    def login():
        """Maneja el inicio de sesión del usuario."""
        if 'user_id' in session:
            return redirect(url_for('main.dashboard'))

        if request.method == 'POST':
            email = request.form.get('email', '')
            password = request.form.get('password', '')

            success, message, user = AuthService.authenticate_user(email, password)

            if success:
                # Crear sesión del usuario
                session['user_id'] = user.id
                session['user_name'] = user.username
                session['user_role'] = user.role
                flash(message, 'success')

                # Redirigir según el rol del usuario
                if user.role == 'admin':
                    return redirect(url_for('main.admin_panel'))
                elif user.role == 'teacher':
                    return redirect(url_for('main.teacher_panel'))
                else:
                    return redirect(url_for('main.dashboard'))
            else:
                flash(message, 'danger')

        return render_template('login.html')

    @staticmethod
    def register():
        """Maneja el registro de nuevos usuarios en el sistema."""
        if 'user_id' in session:
            return redirect(url_for('main.dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '')
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            confirm = request.form.get('confirm_password', '')

            success, message, new_user = AuthService.register_user(username, email, password, confirm)

            if success:
                flash(message, 'success')
                return redirect(url_for('auth.login'))
            else:
                flash(message, 'danger')

        return render_template('register.html')

    @staticmethod
    def logout():
        """Cierra la sesión activa del usuario."""
        session.clear()
        flash('Has cerrado sesión correctamente.', 'info')
        return redirect(url_for('main.home'))
