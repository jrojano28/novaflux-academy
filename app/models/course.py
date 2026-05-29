# app/models/course.py
# Modelos de Curso, Inscripción, Trayectoria y su relación con cursos.

from app.models import db
from datetime import datetime


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_gradient = db.Column(db.String(200), nullable=True)  # CSS gradient string para la portada
    image_url = db.Column(db.String(255), nullable=True)
    level = db.Column(db.String(30), nullable=False, default='Básico')  # Básico / Intermedio / Avanzado
    duration_hours = db.Column(db.Integer, nullable=False, default=10)
    price = db.Column(db.Float, nullable=False, default=29.99)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    topics = db.relationship('Topic', backref='course', lazy=True, cascade="all, delete-orphan")
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.title}>'


class Enrollment(db.Model):
    """Tabla de inscripciones: relaciona estudiantes con cursos y registra su progreso."""
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    progress = db.Column(db.Float, nullable=False, default=0.0)  # Porcentaje de 0.0 a 100.0
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Enrollment user={self.user_id} course={self.course_id} progress={self.progress}%>'


class Roadmap(db.Model):
    """Trayectoria de competencia: agrupa cursos en un orden lógico para lograr una habilidad."""
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)  # Nombre del icono SVG
    color_start = db.Column(db.String(20), nullable=True, default='#00f2fe')
    color_end = db.Column(db.String(20), nullable=True, default='#8b5cf6')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    courses = db.relationship('RoadmapCourse', backref='roadmap', lazy=True,
                               cascade="all, delete-orphan",
                               order_by='RoadmapCourse.order')

    def __repr__(self):
        return f'<Roadmap {self.title}>'


class RoadmapCourse(db.Model):
    """Tabla intermedia que relaciona una trayectoria con sus cursos en orden."""
    __tablename__ = 'roadmap_courses'

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=1)

    # Relación con el curso
    course = db.relationship('Course')

    def __repr__(self):
        return f'<RoadmapCourse roadmap={self.roadmap_id} course={self.course_id}>'


class RoadmapEnrollment(db.Model):
    """Tabla de inscripciones a trayectorias: relaciona alumnos con trayectorias de aprendizaje."""
    __tablename__ = 'roadmap_enrollments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user = db.relationship('User', backref=db.backref('roadmap_enrollments', lazy=True, cascade="all, delete-orphan"))
    roadmap = db.relationship('Roadmap', backref=db.backref('enrollments', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<RoadmapEnrollment user={self.user_id} roadmap={self.roadmap_id}>'

