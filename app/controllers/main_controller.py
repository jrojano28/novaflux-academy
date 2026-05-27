# app/controllers/main_controller.py
# Controlador para las rutas generales: Home, Dashboard (Alumno), Paneles de Roles.

from flask import Blueprint, render_template, redirect, url_for, session, request
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
    from app.models.user import ActivityLog
    from app.models.course import RoadmapEnrollment, RoadmapCourse

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

    # 1. Cursos recomendados (en los que aún no se ha inscrito)
    enrolled_course_ids = [e.course_id for e in enrollments]
    if enrolled_course_ids:
        recommended_courses = Course.query.filter(~Course.id.in_(enrolled_course_ids)).limit(3).all()
    else:
        recommended_courses = Course.query.limit(3).all()

    # 2. Trayectorias activas y su progreso
    roadmap_enrollments = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
    active_roadmaps = []

    for re in roadmap_enrollments:
        roadmap = re.roadmap
        # Obtener todos los cursos vinculados a esta trayectoria
        rc_list = RoadmapCourse.query.filter_by(roadmap_id=roadmap.id).all()
        total_rm_courses = len(rc_list)

        completed_rm_courses = 0
        if total_rm_courses > 0:
            course_ids = [rc.course_id for rc in rc_list]
            completed_rm_courses = Enrollment.query.filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id.in_(course_ids),
                Enrollment.progress >= 100
            ).count()
            rm_progress = (completed_rm_courses / total_rm_courses) * 100.0
        else:
            rm_progress = 0.0

        active_roadmaps.append({
            'roadmap': roadmap,
            'progress': round(rm_progress, 1),
            'completed_courses': completed_rm_courses,
            'total_courses': total_rm_courses
        })

    # 3. Historial de las últimas 5 actividades registradas
    activities = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        user=user,
        enrollments=enrollments,
        stats=stats,
        recommended_courses=recommended_courses,
        active_roadmaps=active_roadmaps,
        activities=activities
    )


@main_bp.route('/roadmaps')
def roadmaps():
    """Vista pública de trayectorias de competencia disponibles, con lógica de bloqueo."""
    from app.models.course import RoadmapCourse, RoadmapEnrollment

    all_roadmaps = Roadmap.query.all()
    user_id = session.get('user_id')

    # Obtener las trayectorias inscritas del usuario
    enrolled_roadmap_ids = []
    if user_id:
        enrolled_rms = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
        enrolled_roadmap_ids = [re.roadmap_id for re in enrolled_rms]

    roadmaps_data = []
    for rm in all_roadmaps:
        is_user_enrolled_in_rm = rm.id in enrolled_roadmap_ids

        courses_data = []
        for rc in rm.courses:
            course = rc.course
            unlocked = True
            lock_reason = ""
            course_progress = 0.0
            is_enrolled_in_course = False

            if user_id:
                # Comprobar si está inscrito en el curso específico y su porcentaje de progreso
                enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
                if enrollment:
                    course_progress = enrollment.progress
                    is_enrolled_in_course = True

                # Condición de bloqueo progresivo en la trayectoria
                if rc.order > 1:
                    prev_rc = RoadmapCourse.query.filter_by(roadmap_id=rm.id, order=rc.order - 1).first()
                    if prev_rc:
                        prev_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=prev_rc.course_id).first()
                        if not prev_enrollment or prev_enrollment.progress < 100.0:
                            # Se marca como bloqueado si el curso anterior no está completado al 100%
                            unlocked = False
                            lock_reason = f"Completa primero '{prev_rc.course.title}' para desbloquear este paso."
            else:
                # Si no está autenticado, todos los cursos excepto el primero se visualizan como bloqueados
                if rc.order > 1:
                    unlocked = False
                    lock_reason = "Inicia sesión para desbloquear esta ruta."

            courses_data.append({
                'course': course,
                'order': rc.order,
                'unlocked': unlocked,
                'lock_reason': lock_reason,
                'progress': course_progress,
                'is_enrolled': is_enrolled_in_course
            })

        roadmaps_data.append({
            'roadmap': rm,
            'is_enrolled': is_user_enrolled_in_rm,
            'courses': courses_data
        })

    return render_template('roadmaps.html', roadmaps=roadmaps_data)


@main_bp.route('/roadmaps/<int:roadmap_id>/enroll', methods=['POST'])
@login_required
def enroll_roadmap(roadmap_id):
    """Inscribe al usuario en una trayectoria y en su primer curso de forma secuencial."""
    from flask import flash
    from app.models.course import Roadmap, RoadmapCourse, RoadmapEnrollment
    from app.models.user import ActivityLog

    user_id = session['user_id']
    roadmap = Roadmap.query.get_or_404(roadmap_id)

    # Verificar si ya está inscrito
    existing = RoadmapEnrollment.query.filter_by(user_id=user_id, roadmap_id=roadmap_id).first()
    if existing:
        flash('Ya has iniciado esta trayectoria.', 'info')
        return redirect(url_for('main.roadmaps'))

    # Crear inscripción a trayectoria
    re = RoadmapEnrollment(user_id=user_id, roadmap_id=roadmap_id)
    db.session.add(re)

    # Registrar actividad
    log = ActivityLog(
        user_id=user_id,
        activity_type='enroll_roadmap',
        description=f"Comenzaste la trayectoria '{roadmap.title}'."
    )
    db.session.add(log)

    # Inscribir automáticamente al primer curso de la trayectoria
    first_rc = RoadmapCourse.query.filter_by(roadmap_id=roadmap_id, order=1).first()
    if first_rc:
        course_id = first_rc.course_id
        course_title = first_rc.course.title

        # Verificar si no está inscrito ya en el curso
        course_enroll = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if not course_enroll:
            new_enroll = Enrollment(user_id=user_id, course_id=course_id, progress=0.0)
            db.session.add(new_enroll)

            course_log = ActivityLog(
                user_id=user_id,
                activity_type='enroll_course',
                description=f"Te inscribiste en '{course_title}' (Paso 1 de '{roadmap.title}')."
            )
            db.session.add(course_log)

    db.session.commit()
    flash(f'¡Trayectoria "{roadmap.title}" iniciada con éxito! Has comenzado el paso 1.', 'success')
    return redirect(url_for('main.roadmaps'))


@main_bp.route('/admin')
@role_required('admin')
def admin_panel():
    """Panel de control del administrador del sistema."""
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

    my_courses = Course.query.filter_by(instructor_id=teacher_id).all()
    total_students = sum(
        Enrollment.query.filter_by(course_id=c.id).count()
        for c in my_courses
    )

    return render_template('teacher.html', teacher=teacher, my_courses=my_courses, total_students=total_students)
