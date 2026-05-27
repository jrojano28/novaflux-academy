# app/controllers/main_controller.py
# Controlador para las rutas generales: Home, Dashboard (Alumno), Paneles de Roles.

from flask import Blueprint, render_template, redirect, url_for, session
from app.models.course import Course, Enrollment, Roadmap
from app.models.user import User
from app.models import db
from app.controllers.auth_controller import login_required, role_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Página de inicio pública con los cursos más recientes."""
    courses = Course.query.order_by(Course.created_at.desc()).limit(6).all()
    roadmaps = Roadmap.query.limit(3).all()
    return render_template('home.html', courses=courses, roadmaps=roadmaps)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Panel de control personal del estudiante. Solo accesible con sesión activa."""
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    # Obtener inscripciones del usuario con sus cursos
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()

    # Calcular estadísticas generales del alumno
    total_courses = len(enrollments)
    completed = sum(1 for e in enrollments if e.progress >= 100)
    in_progress = sum(1 for e in enrollments if 0 < e.progress < 100)
    avg_progress = (sum(e.progress for e in enrollments) / total_courses) if total_courses > 0 else 0

    stats = {
        'total_courses': total_courses,
        'completed': completed,
        'in_progress': in_progress,
        'avg_progress': round(avg_progress, 1)
    }

    return render_template('dashboard.html', user=user, enrollments=enrollments, stats=stats)


@main_bp.route('/roadmaps')
def roadmaps():
    """Vista pública de trayectorias de competencia disponibles."""
    all_roadmaps = Roadmap.query.all()
    return render_template('roadmaps.html', roadmaps=all_roadmaps)


@main_bp.route('/admin')
@role_required('admin')
def admin_panel():
    """Panel de control del administrador del sistema."""
    # Estadísticas globales del sistema
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_teachers = User.query.filter_by(role='teacher').count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()

    recent_users = User.query.order_by(User.id.desc()).limit(10).all()
    courses = Course.query.all()

    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments
    }

    return render_template('admin.html', stats=stats, recent_users=recent_users, courses=courses)


@main_bp.route('/teacher')
@role_required('teacher', 'admin')
def teacher_panel():
    """Panel de control del profesor: estadísticas de sus cursos."""
    teacher_id = session['user_id']
    teacher = User.query.get_or_404(teacher_id)

    # Cursos que el profesor dicta
    my_courses = Course.query.filter_by(instructor_id=teacher_id).all()

    # Total de estudiantes en sus cursos
    total_students = sum(
        Enrollment.query.filter_by(course_id=c.id).count()
        for c in my_courses
    )

    return render_template('teacher.html', teacher=teacher, my_courses=my_courses, total_students=total_students)
