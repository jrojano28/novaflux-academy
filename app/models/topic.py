# app/models/topic.py
# Definición de los modelos de Tema (Topic) y Contenido (Content) para la base de datos.

from app.models import db
from datetime import datetime

class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=1)

    # Relación de uno a muchos: Un tema tiene muchos contenidos de estudio
    contents = db.relationship('Content', backref='topic', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Topic {self.title}>'


class Content(db.Model):
    __tablename__ = 'contents'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False) # Explicaciones, Markdown o código HTML
    order = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Content {self.title}>'


class UserLessonProgress(db.Model):
    """Guarda el progreso individual de las lecciones (contents) por cada estudiante."""
    __tablename__ = 'user_lesson_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Restricción única para evitar registros duplicados de la misma lección para el mismo usuario
    __table_args__ = (db.UniqueConstraint('user_id', 'content_id', name='_user_lesson_uc'),)

    # Relaciones
    user = db.relationship('User', backref=db.backref('lesson_progress', lazy=True, cascade="all, delete-orphan"))
    content = db.relationship('Content', backref=db.backref('user_progress', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<UserLessonProgress user={self.user_id} content={self.content_id}>'


class UserExerciseProgress(db.Model):
    __tablename__ = 'user_exercise_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    last_code = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'content_id', name='_user_exercise_uc'),)

    user = db.relationship('User', backref=db.backref('exercise_progress', lazy=True, cascade="all, delete-orphan"))
    content = db.relationship('Content', backref=db.backref('exercise_progress', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<UserExerciseProgress user={self.user_id} content={self.content_id} completed={self.completed}>'


class UserQuizProgress(db.Model):
    __tablename__ = 'user_quiz_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    passed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'content_id', name='_user_quiz_uc'),)

    user = db.relationship('User', backref=db.backref('quiz_progress', lazy=True, cascade="all, delete-orphan"))
    content = db.relationship('Content', backref=db.backref('quiz_progress', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<UserQuizProgress user={self.user_id} content={self.content_id} passed={self.passed}>'

