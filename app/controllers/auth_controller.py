# app/controllers/auth_controller.py
# Controlador de autenticación: Registro, Login, Logout y decoradores de acceso por roles.

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ─── DECORADORES DE ROLES ─────────────────────────────────────────────────────

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


# ─── RUTAS DE AUTENTICACIÓN ───────────────────────────────────────────────────

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Vista de inicio de sesión."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Crear sesión del usuario
            session['user_id'] = user.id
            session['user_name'] = user.username
            session['user_role'] = user.role
            flash(f'¡Bienvenido de vuelta, {user.username}!', 'success')

            # Redirigir según el rol del usuario
            if user.role == 'admin':
                return redirect(url_for('main.admin_panel'))
            elif user.role == 'teacher':
                return redirect(url_for('main.teacher_panel'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Correo o contraseña incorrectos. Verifica tus datos.', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Vista de registro de nuevos usuarios."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Validaciones básicas
        if not all([username, email, password, confirm]):
            flash('Por favor, completa todos los campos.', 'warning')
        elif password != confirm:
            flash('Las contraseñas no coinciden.', 'danger')
        elif len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'warning')
        elif User.query.filter_by(email=email).first():
            flash('Este correo electrónico ya está registrado.', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Este nombre de usuario ya está en uso.', 'danger')
        else:
            # Crear el nuevo usuario con rol de estudiante por defecto
            new_user = User(username=username, email=email, role='student')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('¡Cuenta creada con éxito! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Cerrar sesión del usuario actual."""
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.home'))
