# app/controllers/course_controller.py
# Controlador para las rutas relacionadas con los cursos: Catálogo, Detalle e Inscripción.

from flask import Blueprint, render_template, abort, redirect, url_for, session, flash
from app.models import db
from app.models.course import Course, Enrollment
from app.controllers.auth_controller import login_required

course_bp = Blueprint('course', __name__, url_prefix='/courses')


@course_bp.route('/')
def list_courses():
    """Vista pública del catálogo completo de cursos."""
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


@course_bp.route('/<int:course_id>')
def course_detail(course_id):
    """Vista de detalle de un curso: temas, contenidos y botón de inscripción."""
    course = Course.query.get_or_404(course_id)

    # Verificar si el usuario autenticado está inscrito en este curso
    is_enrolled = False
    enrollment = None
    if 'user_id' in session:
        enrollment = Enrollment.query.filter_by(
            user_id=session['user_id'],
            course_id=course_id
        ).first()
        is_enrolled = enrollment is not None

    return render_template('detail.html', course=course, is_enrolled=is_enrolled, enrollment=enrollment)


@course_bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    """Inscribe al usuario autenticado en el curso especificado."""
    course = Course.query.get_or_404(course_id)
    user_id = session['user_id']

    # Verificar que no esté ya inscrito
    existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        flash('Ya estás inscrito en este curso.', 'info')
        return redirect(url_for('course.course_detail', course_id=course_id))

    # Crear nueva inscripción
    enrollment = Enrollment(user_id=user_id, course_id=course_id, progress=0.0)
    db.session.add(enrollment)
    db.session.commit()
    flash(f'¡Inscripción exitosa! Bienvenido al curso "{course.title}".', 'success')
    return redirect(url_for('course.course_detail', course_id=course_id))
