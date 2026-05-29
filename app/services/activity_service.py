from app.models import db
from app.models.user import ActivityLog


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
