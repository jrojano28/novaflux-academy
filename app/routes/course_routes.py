# app/routes/course_routes.py
# Rutas de Cursos: Endpoints para catálogo, detalle de curso, inscripción y progreso AJAX.

from flask import Blueprint
from app.controllers import CourseController

course_bp = Blueprint('course', __name__, url_prefix='/courses')

@course_bp.route('/')
def list_courses():
    """Catálogo público de todos los cursos."""
    return CourseController.list_courses()

@course_bp.route('/<int:course_id>')
def course_detail(course_id):
    """Detalle de un curso, syllabus y lecciones SPA."""
    return CourseController.course_detail(course_id)

@course_bp.route('/<int:course_id>/enroll', methods=['POST'])
def enroll(course_id):
    """Inscribe al usuario en el curso."""
    return CourseController.enroll(course_id)

@course_bp.route('/lessons/<int:content_id>/toggle-complete', methods=['POST'])
def toggle_complete_lesson(content_id):
    """Marca o desmarca lección completada vía AJAX."""
    return CourseController.toggle_complete_lesson(content_id)

@course_bp.route('/run-code', methods=['POST'])
def run_code():
    """Ejecuta código Python enviado desde el Playground."""
    return CourseController.run_code()
