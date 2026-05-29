from app.models import db
from app.models.topic import UserExerciseProgress
from datetime import datetime


class ExerciseService:
    @staticmethod
    def has_practice_in_body(body):
        return 'interactive-practice' in body

    @staticmethod
    def has_quiz_in_body(body):
        return 'interactive-quiz' in body

    @staticmethod
    def has_simulator_in_body(body):
        return 'interactive-simulator' in body

    @staticmethod
    def get_practice_status(user_id, content_id):
        record = UserExerciseProgress.query.filter_by(
            user_id=user_id, content_id=content_id
        ).first()
        return record

    @staticmethod
    def save_practice_attempt(user_id, content_id, code, completed):
        record = UserExerciseProgress.query.filter_by(
            user_id=user_id, content_id=content_id
        ).first()

        if record:
            record.attempts += 1
            record.last_code = code
            if completed:
                record.completed = True
                record.completed_at = datetime.utcnow()
        else:
            record = UserExerciseProgress(
                user_id=user_id,
                content_id=content_id,
                completed=completed,
                attempts=1,
                last_code=code,
                completed_at=datetime.utcnow() if completed else None
            )
            db.session.add(record)

        db.session.flush()
        return record

    @staticmethod
    def is_practice_completed(user_id, content_id):
        record = UserExerciseProgress.query.filter_by(
            user_id=user_id, content_id=content_id, completed=True
        ).first()
        return record is not None

    @staticmethod
    def reset_practice(content_id, user_id):
        UserExerciseProgress.query.filter_by(
            user_id=user_id, content_id=content_id
        ).delete()
        db.session.flush()
