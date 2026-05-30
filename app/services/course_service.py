from app.models import db
from app.models.course import Course, Enrollment
from app.models.topic import Topic, Content, UserLessonProgress
from app.services.activity_service import ActivityService
from app.services.exercise_service import ExerciseService
from app.services.quiz_service import QuizService


class CourseService:
    @staticmethod
    def get_all_courses():
        return Course.query.all()

    @staticmethod
    def get_user_enrollments_dict(user_id):
        if not user_id:
            return {}
        user_enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        return {e.course_id: e for e in user_enrollments}

    @staticmethod
    def get_course_or_404(course_id):
        return Course.query.get_or_404(course_id)

    @staticmethod
    def get_completed_lessons_ids(user_id):
        if not user_id:
            return []
        completed = UserLessonProgress.query.filter_by(user_id=user_id).all()
        return [c.content_id for c in completed]

    @staticmethod
    def get_lesson_requirements(content_id):
        content = Content.query.get(content_id)
        if not content:
            return {'has_practice': False, 'has_quiz': False, 'has_simulator': False}
        body = content.body or ''
        return {
            'has_practice': ExerciseService.has_practice_in_body(body),
            'has_quiz': QuizService.has_quiz_in_body(body),
            'has_simulator': ExerciseService.has_simulator_in_body(body),
        }

    @staticmethod
    def are_lesson_requirements_met(user_id, content_id):
        content = Content.query.get(content_id)
        if not content:
            return False
        body = content.body or ''

        reqs_met = True

        if ExerciseService.has_practice_in_body(body):
            if not ExerciseService.is_practice_completed(user_id, content_id):
                reqs_met = False

        if QuizService.has_quiz_in_body(body):
            if not QuizService.is_quiz_passed(user_id, content_id):
                reqs_met = False

        if ExerciseService.has_simulator_in_body(body):
            if not ExerciseService.is_practice_completed(user_id, content_id):
                sim_record = UserLessonProgress.query.filter_by(
                    user_id=user_id, content_id=content_id
                ).first()
                if not sim_record:
                    reqs_met = False

        return reqs_met

    @staticmethod
    def enroll_in_course(user_id, course_id):
        course = Course.query.get(course_id)
        if not course:
            return False, "El curso no existe."

        existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if existing:
            return False, "Ya estás inscrito en este curso."

        try:
            enrollment = Enrollment(user_id=user_id, course_id=course_id, progress=0.0)
            db.session.add(enrollment)

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
        content = Content.query.get(content_id)
        if not content:
            return False, {"message": "Contenido no encontrado."}

        course_id = content.topic.course_id
        course_title = content.topic.course.title

        progress_record = UserLessonProgress.query.filter_by(user_id=user_id, content_id=content_id).first()
        course_newly_completed = False

        try:
            if progress_record:
                db.session.delete(progress_record)
                action_msg = "Lección desmarcada como completada"
                activity_desc = f"Desmarcaste la lección '{content.title}' del curso '{course_title}'."
                activity_type = "uncomplete_lesson"
                is_completed = False
            else:
                reqs_ok = CourseService.are_lesson_requirements_met(user_id, content_id)
                body = content.body or ''
                has_any_interactive = (
                    ExerciseService.has_practice_in_body(body) or
                    QuizService.has_quiz_in_body(body) or
                    ExerciseService.has_simulator_in_body(body)
                )
                if has_any_interactive and not reqs_ok:
                    return False, {
                        "message": "Completa todos los ejercicios, quizzes y prácticas antes de marcar esta lección como completada.",
                        "requirements_not_met": True
                    }

                new_progress = UserLessonProgress(user_id=user_id, content_id=content_id)
                db.session.add(new_progress)
                action_msg = "Lección marcada como completada"
                activity_desc = f"Completaste la lección '{content.title}' del curso '{course_title}'."
                activity_type = "complete_lesson"
                is_completed = True

            db.session.flush()

            ActivityService.log_activity(user_id=user_id, activity_type=activity_type, description=activity_desc)

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

            enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

            if enrollment:
                old_progress = enrollment.progress
                enrollment.progress = progress_percentage

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

    @staticmethod
    def execute_playground_code(code):
        import sys
        import io

        if not code or not code.strip():
            return "Consola vacía."

        if len(code) > 2000:
            return "Error: El código es demasiado largo para el Playground educativo."

        dangerous_keywords = ["import", "open", "eval", "exec", "os", "sys", "subprocess", "write", "read", "builtins", "__", "globals", "locals"]
        for word in dangerous_keywords:
            if word in code:
                return f"Seguridad: No se permite usar '{word}' en el Playground educativo."

        stdout_capture = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout_capture

        try:
            safe_globals = {
                "print": print,
                "range": range,
                "len": len,
                "sum": sum,
                "list": list,
                "dict": dict,
                "int": int,
                "float": float,
                "str": str,
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
            }
            exec(code, safe_globals, {})
            output = stdout_capture.getvalue()
            if not output:
                output = "[Ejecución exitosa, sin salida print]"
        except Exception as e:
            output = f"Error de ejecución:\n{str(e)}"
        finally:
            sys.stdout = old_stdout

        return output
