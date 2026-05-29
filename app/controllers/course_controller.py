# app/controllers/course_controller.py
# Controlador de Cursos: Gestiona el catálogo, lecciones e inscripciones de estudiantes.

from flask import render_template, redirect, url_for, session, flash, jsonify
from app.services.course_service import CourseService
from app.services.roadmap_service import RoadmapService

class CourseController:
    @staticmethod
    def list_courses():
        """Muestra el catálogo completo de cursos."""
        courses = CourseService.get_all_courses()
        user_id = session.get('user_id')
        enrollments_dict = CourseService.get_user_enrollments_dict(user_id)
        
        return render_template(
            'courses.html',
            courses=courses,
            enrollments_dict=enrollments_dict
        )

    @staticmethod
    def course_detail(course_id):
        """Muestra la vista detallada de un curso con su syllabus y lecciones SPA."""
        course = CourseService.get_course_or_404(course_id)
        user_id = session.get('user_id')
        
        # Valores por defecto
        is_enrolled = False
        enrollment = None
        completed_lesson_ids = []
        is_locked = False
        lock_reason = None

        if user_id:
            enrollments_dict = CourseService.get_user_enrollments_dict(user_id)
            enrollment = enrollments_dict.get(course_id)
            is_enrolled = enrollment is not None

            # Obtener lecciones completadas
            completed_lesson_ids = CourseService.get_completed_lessons_ids(user_id)

            # Verificar si está bloqueado por trayectorias
            is_locked, lock_reason = RoadmapService.check_course_lock_for_user(user_id, course_id)

        return render_template(
            'detail.html',
            course=course,
            is_enrolled=is_enrolled,
            enrollment=enrollment,
            completed_lesson_ids=completed_lesson_ids,
            is_locked=is_locked,
            lock_reason=lock_reason
        )

    @staticmethod
    def enroll(course_id):
        """Inscribe al usuario actual en el curso especificado."""
        user_id = session.get('user_id')
        if not user_id:
            flash("Inicia sesión para poder inscribirte en un curso.", "warning")
            return redirect(url_for('auth.login'))

        success, message = CourseService.enroll_in_course(user_id, course_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'info')

        return redirect(url_for('course.course_detail', course_id=course_id))

    @staticmethod
    def toggle_complete_lesson(content_id):
        """Alterna el estado completado de una lección (AJAX)."""
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Debes iniciar sesión.'}), 401

        success, result = CourseService.toggle_lesson_completion(user_id, content_id)
        if success:
            return jsonify(result)
        else:
            return jsonify(result), 400
