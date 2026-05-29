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

    return render_template(
        'detail.html',
        course=course,
        is_enrolled=is_enrolled,
        enrollment=enrollment,
        completed_lesson_ids=completed_lesson_ids,
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

<<<<<<< Updated upstream
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
    from app.models.topic import Topic, Content, UserLessonProgress
    from app.models.user import ActivityLog

    user_id = session['user_id']
    content = Content.query.get_or_404(content_id)
    course_id = content.topic.course_id
    course_title = content.topic.course.title

    # Buscar si ya está completada
    progress_record = UserLessonProgress.query.filter_by(user_id=user_id, content_id=content_id).first()

    if progress_record:
        # Desmarcar completado
        db.session.delete(progress_record)
        action_msg = "Lección desmarcada como completada"
        activity_desc = f"Desmarcaste la lección '{content.title}' del curso '{course_title}'."
        activity_type = "uncomplete_lesson"
        is_completed = False
    else:
        # Marcar completado
        new_progress = UserLessonProgress(user_id=user_id, content_id=content_id)
        db.session.add(new_progress)
        action_msg = "Lección marcada como completada"
        activity_desc = f"Completaste la lección '{content.title}' del curso '{course_title}'."
        activity_type = "complete_lesson"
        is_completed = True

    db.session.commit()

    # Guardar en bitácora de actividad
    log = ActivityLog(user_id=user_id, activity_type=activity_type, description=activity_desc)
    db.session.add(log)

    # Recalcular progreso general del curso
    course_lessons = Content.query.join(Topic).filter(Topic.course_id == course_id).all()
    total_lessons = len(course_lessons)

    if total_lessons > 0:
        lesson_ids = [l.id for l in course_lessons]
        completed_count = UserLessonProgress.query.filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.content_id.in_(lesson_ids)
        ).count()
        progress_percentage = (completed_count / total_lessons) * 100.0
    else:
        progress_percentage = 0.0

    # Actualizar tabla de inscripciones (Enrollment)
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    course_newly_completed = False

    if enrollment:
        old_progress = enrollment.progress
        enrollment.progress = round(progress_percentage, 1)

        # Si antes no estaba completo y ahora sí
        if enrollment.progress >= 100.0 and old_progress < 100.0:
            course_newly_completed = True
            course_log = ActivityLog(
                user_id=user_id,
                activity_type='complete_course',
                description=f"¡Has completado con éxito el curso '{course_title}'!"
            )
            db.session.add(course_log)

        db.session.commit()

    return jsonify({
        'success': True,
        'message': action_msg,
        'completed': is_completed,
        'progress': enrollment.progress if enrollment else round(progress_percentage, 1),
        'course_completed': (enrollment.progress >= 100.0) if enrollment else (progress_percentage >= 100.0),
        'course_newly_completed': course_newly_completed
    })
=======
        success, result = CourseService.toggle_lesson_completion(user_id, content_id)
        if success:
            return jsonify(result)
        else:
            return jsonify(result), 400

    @staticmethod
    def run_code():
        """Ejecuta código Python básico enviado desde el Playground (AJAX)."""
        from flask import request
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'output': 'Debes iniciar sesión para ejecutar código.'}), 401

        data = request.get_json() or {}
        code = data.get('code', '')

        output = CourseService.execute_playground_code(code)
        return jsonify({'success': True, 'output': output})
>>>>>>> Stashed changes
