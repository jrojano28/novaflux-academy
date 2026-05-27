# seed_genetic_algorithm.py
# Script para cargar el curso de Algoritmos Genéticos, usuarios demo y trayectoria de competencia.

from app import create_app
from app.models import db
from app.models.user import User
from app.models.course import Course, Enrollment, Roadmap, RoadmapCourse
from app.models.topic import Topic, Content

app = create_app()

def seed_data():
    with app.app_context():

        # ─── USUARIOS DEMO ──────────────────────────────────────────────────
        if User.query.count() == 0:
            users = [
                {'username': 'admin_nova',  'email': 'admin@demo.com',   'role': 'admin'},
                {'username': 'prof_carlos', 'email': 'teacher@demo.com', 'role': 'teacher'},
                {'username': 'estudiante1', 'email': 'student@demo.com', 'role': 'student'},
            ]
            created_users = {}
            for u in users:
                user = User(username=u['username'], email=u['email'], role=u['role'])
                user.set_password('novaflux2026')
                db.session.add(user)
                db.session.flush()  # Para obtener el id antes del commit
                created_users[u['role']] = user
            db.session.commit()
            print(f"[OK] {len(users)} usuarios demo creados.")
        else:
            created_users = {
                'teacher': User.query.filter_by(role='teacher').first(),
                'student': User.query.filter_by(role='student').first(),
            }

        teacher = created_users.get('teacher') or User.query.filter_by(role='teacher').first()
        student = created_users.get('student') or User.query.filter_by(role='student').first()

        # ─── CURSO DEMO (Intro IA) ──────────────────────────────────────────
        if Course.query.count() == 0:
            curso_intro = Course(
                title="Introducción a la Inteligencia Artificial",
                description="Explora los fundamentos de la IA, el aprendizaje automático y cómo los sistemas resuelven problemas complejos en el mundo real.",
                image_gradient="linear-gradient(135deg, #1a1a4e 0%, #4f46e5 50%, #00f2fe 100%)",
                level="Básico",
                duration_hours=8,
                instructor_id=teacher.id if teacher else None
            )
            db.session.add(curso_intro)
            db.session.commit()

            t = Topic(course_id=curso_intro.id, title="Conceptos Fundamentales", order=1)
            db.session.add(t)
            db.session.commit()

            c = Content(topic_id=t.id, title="¿Qué es la Inteligencia Artificial?", order=1,
                        body="<p>La <strong>Inteligencia Artificial (IA)</strong> es una rama de la computación que busca construir sistemas capaces de simular procesos cognitivos humanos como aprender, razonar y autocorregirse.</p>")
            db.session.add(c)
            db.session.commit()
            print(f"[OK] Curso 'Intro IA' creado con ID {curso_intro.id}")

        # ─── CURSO DE ALGORITMOS GENÉTICOS ─────────────────────────────────
        if Course.query.filter_by(title="Algoritmos Genéticos en Python").count() == 0:
            curso_ga = Course(
                title="Algoritmos Genéticos en Python",
                description="Aprende a diseñar, optimizar e implementar algoritmos evolutivos en Python desde cero. Resuelve problemas de optimización combinatoria y numérica compleja.",
                image_gradient="linear-gradient(135deg, #0d2137 0%, #10b981 50%, #00f2fe 100%)",
                level="Avanzado",
                duration_hours=20,
                instructor_id=teacher.id if teacher else None
            )
            db.session.add(curso_ga)
            db.session.commit()

            t1 = Topic(course_id=curso_ga.id, title="1. Introducción a la Computación Evolutiva", order=1)
            db.session.add(t1)
            db.session.commit()

            Content(topic_id=t1.id, title="1.1 Fundamentos de los Algoritmos Genéticos", order=1, body="""
<p>Los <strong>Algoritmos Genéticos (AG)</strong> son métodos adaptativos y de optimización global inspirados en los procesos evolutivos de la naturaleza, propuestos por <strong>John Holland</strong> en los años 70.</p>
<h3>Inspiración Biológica</h3>
<ul>
    <li><strong>Individuo / Cromosoma:</strong> Una solución potencial al problema.</li>
    <li><strong>Población:</strong> Conjunto de soluciones potenciales.</li>
    <li><strong>Aptitud (Fitness):</strong> Medida de la calidad de la solución.</li>
    <li><strong>Selección:</strong> Elegir las mejores soluciones para reproducirse.</li>
    <li><strong>Operadores Genéticos:</strong> Cruzamiento y Mutación para crear nuevas soluciones.</li>
</ul>
<h3>Ciclo Evolutivo</h3>
<pre><code>Población Inicial -> Evaluación -> Selección -> Reproducción -> Nueva Población -> ¿Convergencia?</code></pre>
""").save() if False else db.session.add(Content(topic_id=t1.id, title="1.1 Fundamentos de los Algoritmos Genéticos", order=1, body="""
<p>Los <strong>Algoritmos Genéticos (AG)</strong> son métodos adaptativos y de optimización global inspirados en los procesos evolutivos de la naturaleza, propuestos por <strong>John Holland</strong> en los años 70.</p>
<h3>Inspiración Biológica</h3>
<ul>
    <li><strong>Individuo / Cromosoma:</strong> Una solución potencial al problema.</li>
    <li><strong>Población:</strong> Conjunto de soluciones potenciales.</li>
    <li><strong>Aptitud (Fitness):</strong> Medida de la calidad de la solución.</li>
</ul>
<pre><code>Población Inicial -> Evaluación -> Selección -> Reproducción -> Nueva Población</code></pre>
"""))

            t2 = Topic(course_id=curso_ga.id, title="2. Operadores Genéticos", order=2)
            db.session.add(t2)
            db.session.commit()

            db.session.add(Content(topic_id=t2.id, title="2.1 Selección por Torneo", order=1, body="""
<p>La <strong>selección por torneo</strong> elige al azar <code>k</code> individuos y retorna el de mayor aptitud.</p>
<pre><code>import random

def tournament_selection(population, k=3):
    tournament = random.sample(population, k)
    return max(tournament, key=lambda ind: ind['fitness'])
</code></pre>
"""))

            db.session.add(Content(topic_id=t2.id, title="2.2 Cruzamiento y Mutación", order=2, body="""
<h3>Cruzamiento de Un Punto</h3>
<pre><code>def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
</code></pre>
<h3>Mutación Flip-Bit</h3>
<pre><code>def mutate(chromosome, rate=0.01):
    return [1 - gen if random.random() < rate else gen for gen in chromosome]
</code></pre>
"""))

            t3 = Topic(course_id=curso_ga.id, title="3. Proyecto: Problema One-Max", order=3)
            db.session.add(t3)
            db.session.commit()

            db.session.add(Content(topic_id=t3.id, title="3.1 Implementación Completa en Python", order=1, body="""
<p>Implementación completa del Algoritmo Genético para resolver el problema <strong>One-Max</strong>.</p>
<pre><code>import random

CHROMOSOME_SIZE = 20
POPULATION_SIZE = 100
GENERATIONS = 50

def create_individual():
    return [random.choice([0, 1]) for _ in range(CHROMOSOME_SIZE)]

def get_fitness(individual):
    return sum(individual)

population = [{'chromosome': create_individual(), 'fitness': 0} for _ in range(POPULATION_SIZE)]

for gen in range(GENERATIONS):
    for ind in population:
        ind['fitness'] = get_fitness(ind['chromosome'])
    population.sort(key=lambda i: i['fitness'], reverse=True)
    best = population[0]
    print(f"Gen {gen}: Mejor Fitness = {best['fitness']}")
    if best['fitness'] == CHROMOSOME_SIZE:
        print("¡Solución óptima!")
        break
</code></pre>
"""))
            db.session.commit()
            print(f"[OK] Curso 'Algoritmos Genéticos' creado con ID {curso_ga.id}")

        # ─── INSCRIPCIÓN DEMO ───────────────────────────────────────────────
        curso_ga_obj = Course.query.filter_by(title="Algoritmos Genéticos en Python").first()
        if student and curso_ga_obj:
            existing = Enrollment.query.filter_by(user_id=student.id, course_id=curso_ga_obj.id).first()
            if not existing:
                db.session.add(Enrollment(user_id=student.id, course_id=curso_ga_obj.id, progress=35.0))
                db.session.commit()
                print(f"[OK] Inscripción demo: {student.username} -> {curso_ga_obj.title} (35%)")

        # ─── TRAYECTORIA DE COMPETENCIA ─────────────────────────────────────
        if Roadmap.query.count() == 0:
            rm = Roadmap(
                title="Ingeniero en Algoritmos Inteligentes",
                description="Domina los fundamentos de la IA y los algoritmos evolutivos para convertirte en un especialista en optimización y sistemas inteligentes.",
                icon="🧠",
                color_start="#00f2fe",
                color_end="#8b5cf6"
            )
            db.session.add(rm)
            db.session.commit()

            for order, course_title in enumerate([
                "Introducción a la Inteligencia Artificial",
                "Algoritmos Genéticos en Python"
            ], start=1):
                course_obj = Course.query.filter_by(title=course_title).first()
                if course_obj:
                    db.session.add(RoadmapCourse(roadmap_id=rm.id, course_id=course_obj.id, order=order))
            db.session.commit()
            print(f"[OK] Trayectoria '{rm.title}' creada con {len(rm.courses)} cursos.")

        print("\n[SUCCESS] Siembra completa de NovaFlux Academy exitosa!")


if __name__ == '__main__':
    seed_data()
