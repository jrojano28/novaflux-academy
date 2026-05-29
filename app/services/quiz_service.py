from app.models import db
from app.models.topic import UserQuizProgress
from datetime import datetime


class QuizService:
    @staticmethod
    def has_quiz_in_body(body):
        return 'interactive-quiz' in body

    @staticmethod
    def get_quiz_status(user_id, content_id):
        record = UserQuizProgress.query.filter_by(
            user_id=user_id, content_id=content_id
        ).first()
        return record

    @staticmethod
    def save_quiz_attempt(user_id, content_id, passed):
        record = UserQuizProgress.query.filter_by(
            user_id=user_id, content_id=content_id
        ).first()

        if record:
            record.attempts += 1
            if passed:
                record.passed = True
                record.completed_at = datetime.utcnow()
        else:
            record = UserQuizProgress(
                user_id=user_id,
                content_id=content_id,
                passed=passed,
                attempts=1,
                completed_at=datetime.utcnow() if passed else None
            )
            db.session.add(record)

        db.session.flush()
        return record

    @staticmethod
    def is_quiz_passed(user_id, content_id):
        record = UserQuizProgress.query.filter_by(
            user_id=user_id, content_id=content_id, passed=True
        ).first()
        return record is not None

    @staticmethod
    def reset_quiz(content_id, user_id):
        UserQuizProgress.query.filter_by(
            user_id=user_id, content_id=content_id
        ).delete()
        db.session.flush()
