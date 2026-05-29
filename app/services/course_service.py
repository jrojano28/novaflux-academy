# app/services/course_service.py
# Servicio de Cursos: Catálogo, lecciones, inscripciones y cálculo de progreso.

from app.models import db
from app.models.course import Course, Enrollment
from app.models.topic import Topic, Content, UserLessonProgress
from app.services.activity_service import ActivityService

class CourseService:
    @staticmethod
    def get_all_courses():
        """
        Retorna la lista de todos los cursos disponibles.
        """
        return Course.query.all()

    @staticmethod
    def get_user_enrollments_dict(user_id):
        """
        Retorna un diccionario de {course_id: enrollment} para un usuario dado.
        """
        if not user_id:
            return {}
        user_enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        return {e.course_id: e for e in user_enrollments}

    @staticmethod
    def get_course_or_404(course_id):
        """
        Obtiene un curso por su ID o levanta error 404.
        """
        return Course.query.get_or_404(course_id)

    @staticmethod
    def get_completed_lessons_ids(user_id):
        """
        Retorna la lista de IDs de lecciones completadas por el usuario.
        """
        if not user_id:
            return []
        completed = UserLessonProgress.query.filter_by(user_id=user_id).all()
        return [c.content_id for c in completed]

    @staticmethod
    def enroll_in_course(user_id, course_id):
        """
        Inscribe al usuario en un curso específico.
        Retorna (exito, mensaje)
        """
        course = Course.query.get(course_id)
        if not course:
            return False, "El curso no existe."

        existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if existing:
            return False, "Ya estás inscrito en este curso."

        try:
            # Crear nueva inscripción
            enrollment = Enrollment(user_id=user_id, course_id=course_id, progress=0.0)
            db.session.add(enrollment)
            
            # Registrar actividad
            ActivityService.log_activity(
                user_id=user_id,
                activity_type='enroll_course',
                description=f"Te inscribiste en el curso '{course.title}'."
            )
            
            db.session.commit()
            return True, f'¡Inscripción exitosa! Bienvenido al curso "{course.title}".'
        except Exception as e:
            db.session.rollback()
            return False, f"Error al inscribirse en el curso: {str(e)}"

    @staticmethod
    def toggle_lesson_completion(user_id, content_id):
        """
        Alterna el estado de finalización de una lección para el usuario.
        Recalcula el progreso general del curso.
        Retorna (exito, data_resultado)
        """
        content = Content.query.get(content_id)
        if not content:
            return False, {"message": "Contenido no encontrado."}

        course_id = content.topic.course_id
        course_title = content.topic.course.title

        # Buscar si ya está completada
        progress_record = UserLessonProgress.query.filter_by(user_id=user_id, content_id=content_id).first()
        course_newly_completed = False

        try:
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

            db.session.flush()

            # Guardar en bitácora de actividad
            log = ActivityService.log_activity(user_id=user_id, activity_type=activity_type, description=activity_desc)

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

            progress_percentage = round(progress_percentage, 1)

            # Actualizar tabla de inscripciones (Enrollment)
            enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

            if enrollment:
                old_progress = enrollment.progress
                enrollment.progress = progress_percentage

                # Si antes no estaba completo y ahora sí
                if enrollment.progress >= 100.0 and old_progress < 100.0:
                    course_newly_completed = True
                    ActivityService.log_activity(
                        user_id=user_id,
                        activity_type='complete_course',
                        description=f"¡Has completado con éxito el curso '{course_title}'!"
                    )

            db.session.commit()

            return True, {
                'success': True,
                'message': action_msg,
                'completed': is_completed,
                'progress': enrollment.progress if enrollment else progress_percentage,
                'course_completed': (enrollment.progress >= 100.0) if enrollment else (progress_percentage >= 100.0),
                'course_newly_completed': course_newly_completed
            }
        except Exception as e:
            db.session.rollback()
            return False, {"message": f"Error al procesar el progreso: {str(e)}"}
