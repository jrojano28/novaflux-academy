# app/controllers/course_controller.py
# Controlador para las rutas relacionadas con los cursos: Catálogo, Detalle e Inscripción.

from flask import Blueprint, render_template, abort, redirect, url_for, session, flash, jsonify
from app.models import db
from app.models.course import Course, Enrollment
from app.controllers.auth_controller import login_required

course_bp = Blueprint('course', __name__, url_prefix='/courses')


@course_bp.route('/')
def list_courses():
    """Vista pública del catálogo completo de cursos."""
    courses = Course.query.all()
    enrollments_dict = {}
    if 'user_id' in session:
        user_enrollments = Enrollment.query.filter_by(user_id=session['user_id']).all()
        enrollments_dict = {e.course_id: e for e in user_enrollments}
    return render_template('courses.html', courses=courses, enrollments_dict=enrollments_dict)


@course_bp.route('/<int:course_id>')
def course_detail(course_id):
    """Vista de detalle de un curso: temas, contenidos y botón de inscripción."""
    course = Course.query.get_or_404(course_id)

    # Verificar si el usuario autenticado está inscrito en este curso
    is_enrolled = False
    enrollment = None
    completed_lesson_ids = []
    is_locked = False
    lock_reason = None

    if 'user_id' in session:
        user_id = session['user_id']
        enrollment = Enrollment.query.filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()
        is_enrolled = enrollment is not None

        # Obtener IDs de lecciones completadas
        from app.models.topic import UserLessonProgress
        completed = UserLessonProgress.query.filter_by(user_id=user_id).all()
        completed_lesson_ids = [c.content_id for c in completed]

        # Verificar si el curso está bloqueado en alguna trayectoria en la que esté inscrito el estudiante
        from app.models.course import RoadmapCourse, RoadmapEnrollment
        user_roadmaps = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
        for ur in user_roadmaps:
            # Buscar la posición de este curso en esta trayectoria
            rc = RoadmapCourse.query.filter_by(roadmap_id=ur.roadmap_id, course_id=course_id).first()
            if rc and rc.order > 1:
                # Buscar el curso previo en la misma trayectoria (order = current - 1)
                prev_rc = RoadmapCourse.query.filter_by(roadmap_id=ur.roadmap_id, order=rc.order - 1).first()
                if prev_rc:
                    # Verificar si completó el previo
                    prev_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=prev_rc.course_id).first()
                    if not prev_enrollment or prev_enrollment.progress < 100:
                        is_locked = True
                        lock_reason = f"Este curso está BLOQUEADO. Debes completar primero '{prev_rc.course.title}' de la trayectoria '{ur.roadmap.title}'."
                        break

    # Calcular lecciones desbloqueadas secuencialmente
    all_course_contents = []
    for t in sorted(course.topics, key=lambda x: x.order):
        for c in sorted(t.contents, key=lambda x: x.order):
            all_course_contents.append(c)

    unlocked_lesson_ids = []
    for i, c in enumerate(all_course_contents):
        if i == 0:
            unlocked_lesson_ids.append(c.id)
        else:
            prev_c = all_course_contents[i-1]
            if prev_c.id in completed_lesson_ids:
                unlocked_lesson_ids.append(c.id)

    return render_template(
        'detail.html',
        course=course,
        is_enrolled=is_enrolled,
        enrollment=enrollment,
        completed_lesson_ids=completed_lesson_ids,
        unlocked_lesson_ids=unlocked_lesson_ids,
        is_locked=is_locked,
        lock_reason=lock_reason
    )



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

    # Registrar actividad
    from app.models.user import ActivityLog
    log = ActivityLog(
        user_id=user_id,
        activity_type='enroll_course',
        description=f"Te inscribiste en el curso '{course.title}'."
    )
    db.session.add(log)

    db.session.commit()
    flash(f'¡Inscripción exitosa! Bienvenido al curso "{course.title}".', 'success')
    return redirect(url_for('course.course_detail', course_id=course_id))


@course_bp.route('/lessons/<int:content_id>/toggle-complete', methods=['POST'])
@login_required
def toggle_complete_lesson(content_id):
    """Alterna el estado de finalización de una lección para el usuario actual y recalcula el progreso del curso."""
    from app.services.course_service import CourseService
    user_id = session['user_id']
    success, result = CourseService.toggle_lesson_completion(user_id, content_id)
    if success:
        return jsonify(result)
    else:
        return jsonify(result), 400


@course_bp.route('/run-code', methods=['POST'])
def run_code():
    """Ejecuta código Python básico enviado desde el Playground (AJAX)."""
    from app.services.course_service import CourseService
    from flask import request
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            'success': False,
            'output': '💡 Debes iniciar sesión e inscribirte en el curso para ejecutar código en tiempo real.'
        }), 200

    data = request.get_json() or {}
    code = data.get('code', '')

    output = CourseService.execute_playground_code(code)
    return jsonify({'success': True, 'output': output})


