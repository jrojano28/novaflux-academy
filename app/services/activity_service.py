from app.models import db
from app.models.user import ActivityLog
from app.models.course import Enrollment


class ActivityService:
    @staticmethod
    def log_activity(user_id, activity_type, description):
        log = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            description=description
        )
        db.session.add(log)
        db.session.flush()
        return log

    @staticmethod
    def get_recent_activities(user_id, limit=5):
        return ActivityLog.query.filter_by(user_id=user_id)\
                              .order_by(ActivityLog.created_at.desc())\
                              .limit(limit)\
                              .all()

    @staticmethod
    def get_student_stats(user_id):
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        total_courses = len(enrollments)
        completed = sum(1 for e in enrollments if e.progress >= 100)
        in_progress = sum(1 for e in enrollments if 0 < e.progress < 100)
        avg_progress = (sum(e.progress for e in enrollments) / total_courses) if total_courses > 0 else 0

        return {
            'total_courses': total_courses,
            'completed': completed,
            'in_progress': in_progress,
            'avg_progress': round(avg_progress, 1)
        }
