# app/models/user.py
# Definición del modelo de Usuario (User) para la base de datos.

from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') # 'student', 'instructor', 'admin'

    def set_password(self, password):
        """Genera y almacena el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña ingresada contra el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class ActivityLog(db.Model):
    """Guarda el historial de actividades recientes de cada usuario en la plataforma."""
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'enroll_course', 'complete_lesson', 'complete_course', 'enroll_roadmap'
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('activities', lazy='dynamic', cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<ActivityLog user={self.user_id} type={self.activity_type}>'

