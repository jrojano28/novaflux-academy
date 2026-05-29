# app/controllers/main_controller.py
# Controlador General: Gestiona páginas públicas, el dashboard del alumno y los paneles de control.

from flask import render_template, redirect, url_for, session, flash
from app.models.course import Course, Enrollment
from app.models.user import User
from app.services.course_service import CourseService
from app.services.roadmap_service import RoadmapService
from app.services.activity_service import ActivityService

class MainController:
    @staticmethod
    def home():
        """Muestra la página de inicio pública con los cursos y trayectorias más recientes."""
        courses = Course.query.order_by(Course.created_at.desc()).limit(6).all()
        roadmaps = RoadmapService.get_all_roadmaps()[:3]
        return render_template('home.html', courses=courses, roadmaps=roadmaps)

    @staticmethod
    def dashboard():
        """Panel de control personal del estudiante."""
        user_id = session['user_id']
        user = User.query.get_or_404(user_id)

        # 1. Obtener estadísticas del alumno
        stats = ActivityService.get_student_stats(user_id)
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()

        # 2. Cursos recomendados (en los que aún no se ha inscrito)
        enrolled_course_ids = [e.course_id for e in enrollments]
        if enrolled_course_ids:
            recommended_courses = Course.query.filter(~Course.id.in_(enrolled_course_ids)).limit(3).all()
        else:
            recommended_courses = Course.query.limit(3).all()

        # 3. Trayectorias activas y su progreso
        active_roadmaps = RoadmapService.get_active_roadmaps_with_progress(user_id)

        # 4. Historial de las últimas 5 actividades registradas
        activities = ActivityService.get_recent_activities(user_id, limit=5)

        return render_template(
            'dashboard.html',
            user=user,
            enrollments=enrollments,
            stats=stats,
            recommended_courses=recommended_courses,
            active_roadmaps=active_roadmaps,
            activities=activities
        )

    @staticmethod
    def roadmaps():
        """Muestra la vista pública de las trayectorias de aprendizaje."""
        user_id = session.get('user_id')
        roadmaps_data = RoadmapService.get_roadmap_details_for_user(user_id)
        return render_template('roadmaps.html', roadmaps=roadmaps_data)

    @staticmethod
    def enroll_roadmap(roadmap_id):
        """Inscribe al usuario en una trayectoria y en su primer curso."""
        user_id = session['user_id']
        success, message = RoadmapService.enroll_in_roadmap(user_id, roadmap_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'info')

        return redirect(url_for('main.roadmaps'))

    @staticmethod
    def admin_panel():
        """Panel de administración del sistema."""
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

        return render_template(
            'admin.html',
            stats=stats,
            recent_users=recent_users,
            courses=courses
        )

    @staticmethod
    def teacher_panel():
        """Panel de control del profesor."""
        teacher_id = session['user_id']
        teacher = User.query.get_or_404(teacher_id)

        my_courses = Course.query.filter_by(instructor_id=teacher_id).all()
        total_students = sum(
            Enrollment.query.filter_by(course_id=c.id).count()
            for c in my_courses
        )

        return render_template(
            'teacher.html',
            teacher=teacher,
            my_courses=my_courses,
            total_students=total_students
        )
