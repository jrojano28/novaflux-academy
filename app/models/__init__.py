# app/models/__init__.py
# Inicialización de Flask-SQLAlchemy y exportación de todos los modelos del sistema.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar los modelos para que SQLAlchemy los detecte al inicializar la BD
from app.models.user import User
from app.models.course import Course, Enrollment, Roadmap, RoadmapCourse
from app.models.topic import Topic, Content
