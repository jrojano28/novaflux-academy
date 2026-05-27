# app/models/topic.py
# Definición de los modelos de Tema (Topic) y Contenido (Content) para la base de datos.

from app.models import db

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
