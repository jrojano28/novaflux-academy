# init_db.py
# Script de utilidad para inicializar la base de datos SQLite y crear las tablas con datos demo.

from app import create_app
from app.models import db
from app.models.course import Course
from app.models.topic import Topic, Content

app = create_app()

with app.app_context():
    db.create_all()
    print("¡Base de datos SQLite y tablas (users, courses, topics, contents) creadas correctamente!")

    # Insertar curso de demostración si la tabla está vacía
    if Course.query.count() == 0:
        curso_demo = Course(
            title="Introducción a la Inteligencia Artificial",
            description="Explora los fundamentos de la inteligencia artificial, el aprendizaje automático y cómo los sistemas resuelven problemas complejos.",
            image_url="https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=800&q=80"
        )
        db.session.add(curso_demo)
        db.session.commit()

        tema1 = Topic(
            course_id=curso_demo.id,
            title="Conceptos Fundamentales",
            order=1
        )
        db.session.add(tema1)
        db.session.commit()

        contenido1 = Content(
            topic_id=tema1.id,
            title="¿Qué es la IA y el Aprendizaje Automático?",
            body="La Inteligencia Artificial (IA) es un área de la computación que busca construir sistemas capaces de simular procesos cognitivos humanos, como aprender, razonar y autocorregirse.",
            order=1
        )
        db.session.add(contenido1)
        db.session.commit()
        print("¡Curso demo insertado con éxito para pruebas!")
