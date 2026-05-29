from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, request
from app.models import db
from app.models.course import Course, Enrollment
from app.models.topic import Content
from app.controllers.auth_controller import login_required
from app.services.course_service import CourseService
from app.services.exercise_service import ExerciseService
from app.services.quiz_service import QuizService
from app.services.activity_service import ActivityService

course_bp = Blueprint('course', __name__, url_prefix='/courses')


def _ensure_enrolled_for_content(user_id, content):
    course_id = content.topic.course_id
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enrollment:
        return False
    return True


@course_bp.route('/')
def list_courses():
    courses = Course.query.all()
    enrollments_dict = {}
    if 'user_id' in session:
        user_enrollments = Enrollment.query.filter_by(user_id=session['user_id']).all()
        enrollments_dict = {e.course_id: e for e in user_enrollments}
    return render_template('courses.html', courses=courses, enrollments_dict=enrollments_dict)


@course_bp.route('/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)

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

        from app.models.topic import UserLessonProgress
        completed = UserLessonProgress.query.filter_by(user_id=user_id).all()
        completed_lesson_ids = [c.content_id for c in completed]

        from app.models.course import RoadmapCourse, RoadmapEnrollment
        user_roadmaps = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
        for ur in user_roadmaps:
            rc = RoadmapCourse.query.filter_by(roadmap_id=ur.roadmap_id, course_id=course_id).first()
            if rc and rc.order > 1:
                prev_rc = RoadmapCourse.query.filter_by(roadmap_id=ur.roadmap_id, order=rc.order - 1).first()
                if prev_rc:
                    prev_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=prev_rc.course_id).first()
                    if not prev_enrollment or prev_enrollment.progress < 100:
                        is_locked = True
                        lock_reason = f"Este curso está BLOQUEADO. Debes completar primero '{prev_rc.course.title}' de la trayectoria '{ur.roadmap.title}'."
                        break

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
    course = Course.query.get_or_404(course_id)
    user_id = session['user_id']

    existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        flash('Ya estás inscrito en este curso.', 'info')
        return redirect(url_for('course.course_detail', course_id=course_id))

    enrollment = Enrollment(user_id=user_id, course_id=course_id, progress=0.0)
    db.session.add(enrollment)

    ActivityService.log_activity(
        user_id=user_id,
        activity_type='enroll_course',
        description=f"Te inscribiste en el curso '{course.title}'."
    )

    db.session.commit()
    flash(f'¡Inscripción exitosa! Bienvenido al curso "{course.title}".', 'success')
    return redirect(url_for('course.course_detail', course_id=course_id))


@course_bp.route('/lessons/<int:content_id>/toggle-complete', methods=['POST'])
@login_required
def toggle_complete_lesson(content_id):
    user_id = session['user_id']
    success, result = CourseService.toggle_lesson_completion(user_id, content_id)
    if success:
        return jsonify(result)
    else:
        return jsonify(result), 400


@course_bp.route('/run-code', methods=['POST'])
def run_code():
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


@course_bp.route('/lessons/<int:content_id>/validate-practice', methods=['POST'])
@login_required
def validate_practice(content_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    code = data.get('code', '')
    expected_code = data.get('expected_code', '')
    expected_output = data.get('expected_output', '')

    content = Content.query.get(content_id)
    if not content:
        return jsonify({'success': False, 'valid': False, 'message': 'Contenido no encontrado.'}), 404
    if not _ensure_enrolled_for_content(user_id, content):
        return jsonify({'success': False, 'valid': False, 'message': 'No estás inscrito en este curso.'}), 403

    output = CourseService.execute_playground_code(code)

    is_valid = True
    error_details = ''

    if expected_code and expected_code.lower() not in code.lower():
        is_valid = False
        error_details = f"Debes incluir la instrucción o palabra clave '{expected_code}'."

    if expected_output and expected_output.lower() not in output.lower():
        is_valid = False
        error_details = f"La consola no contiene la salida esperada '{expected_output}'."

    if is_valid:
        ExerciseService.save_practice_attempt(user_id, content_id, code, True)
        db.session.commit()
        return jsonify({
            'success': True,
            'valid': True,
            'output': output,
            'message': '🎉 ¡Ejercicio completado!'
        })
    else:
        ExerciseService.save_practice_attempt(user_id, content_id, code, False)
        db.session.commit()
        return jsonify({
            'success': True,
            'valid': False,
            'output': output,
            'message': f'❌ {error_details}'
        })


@course_bp.route('/lessons/<int:content_id>/validate-quiz', methods=['POST'])
@login_required
def validate_quiz(content_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    selected_is_correct = data.get('correct', False)
    explanation = data.get('explanation', '')

    content = Content.query.get(content_id)
    if not content:
        return jsonify({'success': False, 'correct': False, 'message': 'Contenido no encontrado.'}), 404
    if not _ensure_enrolled_for_content(user_id, content):
        return jsonify({'success': False, 'correct': False, 'message': 'No estás inscrito en este curso.'}), 403

    if selected_is_correct:
        QuizService.save_quiz_attempt(user_id, content_id, True)
        db.session.commit()
        return jsonify({
            'success': True,
            'correct': True,
            'message': '🎉 ¡Correcto! Excelente respuesta.'
        })
    else:
        QuizService.save_quiz_attempt(user_id, content_id, False)
        db.session.commit()
        return jsonify({
            'success': True,
            'correct': False,
            'message': '❌ Incorrecto. ¡Inténtalo de nuevo!',
            'explanation': explanation
        })


@course_bp.route('/lessons/<int:content_id>/requirements', methods=['GET'])
@login_required
def get_lesson_requirements(content_id):
    user_id = session['user_id']
    content = Content.query.get(content_id)
    if not content:
        return jsonify({'success': False, 'message': 'Contenido no encontrado.'}), 404
    if not _ensure_enrolled_for_content(user_id, content):
        return jsonify({'success': False, 'message': 'No estás inscrito en este curso.'}), 403

    body = content.body or ''
    reqs = {
        'has_practice': ExerciseService.has_practice_in_body(body),
        'has_quiz': QuizService.has_quiz_in_body(body),
        'has_simulator': ExerciseService.has_simulator_in_body(body),
        'practice_completed': ExerciseService.is_practice_completed(user_id, content_id),
        'quiz_passed': QuizService.is_quiz_passed(user_id, content_id),
        'simulator_completed': ExerciseService.is_practice_completed(user_id, content_id),
    }
    return jsonify({'success': True, 'requirements': reqs})


@course_bp.route('/lessons/<int:content_id>/mark-simulator-done', methods=['POST'])
@login_required
def mark_simulator_done(content_id):
    user_id = session['user_id']
    content = Content.query.get(content_id)
    if not content:
        return jsonify({'success': False, 'message': 'Contenido no encontrado.'}), 404
    if not _ensure_enrolled_for_content(user_id, content):
        return jsonify({'success': False, 'message': 'No estás inscrito en este curso.'}), 403
    ExerciseService.save_practice_attempt(user_id, content_id, '# simulator', True)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Simulador completado.'})
