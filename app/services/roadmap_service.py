# app/services/roadmap_service.py
# Servicio de Trayectorias (Roadmaps): Gestión de rutas de aprendizaje y lógica de bloqueos.

from app.models import db
from app.models.course import Roadmap, RoadmapCourse, RoadmapEnrollment, Enrollment
from app.services.activity_service import ActivityService

class RoadmapService:
    @staticmethod
    def get_all_roadmaps():
        """
        Retorna todas las trayectorias de competencia.
        """
        return Roadmap.query.all()

    @staticmethod
    def get_user_enrolled_roadmap_ids(user_id):
        """
        Retorna la lista de IDs de trayectorias en las que está inscrito el usuario.
        """
        if not user_id:
            return []
        enrolled_rms = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
        return [re.roadmap_id for re in enrolled_rms]

    @staticmethod
    def get_active_roadmaps_with_progress(user_id):
        """
        Calcula el progreso de las trayectorias activas del estudiante.
        """
        if not user_id:
            return []

        roadmap_enrollments = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
        active_roadmaps = []

        for re in roadmap_enrollments:
            roadmap = re.roadmap
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

        return active_roadmaps

    @staticmethod
    def get_roadmap_details_for_user(user_id):
        """
        Retorna información detallada de todas las trayectorias y sus cursos con lógica de bloqueo.
        """
        all_roadmaps = RoadmapService.get_all_roadmaps()
        enrolled_roadmap_ids = RoadmapService.get_user_enrolled_roadmap_ids(user_id)

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

        return roadmaps_data

    @staticmethod
    def check_course_lock_for_user(user_id, course_id):
        """
        Verifica si un curso está bloqueado en alguna trayectoria en la que esté inscrito el estudiante.
        Retorna (is_locked, lock_reason)
        """
        if not user_id:
            return False, None

        user_roadmaps = RoadmapEnrollment.query.filter_by(user_id=user_id).all()
        for ur in user_roadmaps:
            rc = RoadmapCourse.query.filter_by(roadmap_id=ur.roadmap_id, course_id=course_id).first()
            if rc and rc.order > 1:
                prev_rc = RoadmapCourse.query.filter_by(roadmap_id=ur.roadmap_id, order=rc.order - 1).first()
                if prev_rc:
                    prev_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=prev_rc.course_id).first()
                    if not prev_enrollment or prev_enrollment.progress < 100:
                        return True, f"Este curso está BLOQUEADO. Debes completar primero '{prev_rc.course.title}' de la trayectoria '{ur.roadmap.title}'."
        return False, None

    @staticmethod
    def enroll_in_roadmap(user_id, roadmap_id):
        """
        Inscribe al usuario en una trayectoria y en su primer curso de manera secuencial.
        Retorna (exito, mensaje)
        """
        roadmap = Roadmap.query.get(roadmap_id)
        if not roadmap:
            return False, "La trayectoria no existe."

        # Verificar si ya está inscrito
        existing = RoadmapEnrollment.query.filter_by(user_id=user_id, roadmap_id=roadmap_id).first()
        if existing:
            return False, "Ya has iniciado esta trayectoria."

        try:
            # Crear inscripción a trayectoria
            re = RoadmapEnrollment(user_id=user_id, roadmap_id=roadmap_id)
            db.session.add(re)

            # Registrar actividad
            ActivityService.log_activity(
                user_id=user_id,
                activity_type='enroll_roadmap',
                description=f"Comenzaste la trayectoria '{roadmap.title}'."
            )

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

                    ActivityService.log_activity(
                        user_id=user_id,
                        activity_type='enroll_course',
                        description=f"Te inscribiste en '{course_title}' (Paso 1 de '{roadmap.title}')."
                    )

            db.session.commit()
            return True, f'¡Trayectoria "{roadmap.title}" iniciada con éxito! Has comenzado el paso 1.'
        except Exception as e:
            db.session.rollback()
            return False, f"Error al inscribirse en la trayectoria: {str(e)}"
