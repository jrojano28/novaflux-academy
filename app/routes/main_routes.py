# app/routes/main_routes.py
# Rutas Generales: Página de inicio, dashboard de alumno, trayectorias y paneles de roles.

from flask import Blueprint
from app.controllers import MainController, login_required, role_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Página de inicio pública."""
    return MainController.home()

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Panel de control interactivo del estudiante."""
    return MainController.dashboard()

@main_bp.route('/roadmaps')
def roadmaps():
    """Vista de trayectorias de competencia con lógica de bloqueo."""
    return MainController.roadmaps()

@main_bp.route('/roadmaps/<int:roadmap_id>/enroll', methods=['POST'])
@login_required
def enroll_roadmap(roadmap_id):
    """Inscribe al estudiante en la trayectoria."""
    return MainController.enroll_roadmap(roadmap_id)

@main_bp.route('/admin')
@role_required('admin')
def admin_panel():
    """Panel de administración del sistema."""
    return MainController.admin_panel()

@main_bp.route('/teacher')
@role_required('teacher', 'admin')
def teacher_panel():
    """Panel de control para profesores."""
    return MainController.teacher_panel()
