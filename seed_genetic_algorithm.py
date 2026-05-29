# seed_genetic_algorithm.py
# Script para cargar el curso de Algoritmos Genéticos (9 módulos), usuarios demo y trayectoria de competencia.

from app import create_app
from app.models import db
from app.models.user import User, ActivityLog
from app.models.course import Course, Enrollment, Roadmap, RoadmapCourse, RoadmapEnrollment
from app.models.topic import Topic, Content

app = create_app()

def seed_data():
    with app.app_context():
        print("[INFO] Recreando base de datos con el nuevo esquema...")
        # Limpiar y recrear las tablas para incorporar los nuevos modelos
        db.drop_all()
        db.create_all()
        print("[OK] Base de datos y tablas creadas correctamente.")

        # ─── USUARIOS DEMO ──────────────────────────────────────────────────
        print("[INFO] Creando usuarios demo...")
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
            db.session.flush()
            created_users[u['role']] = user
        db.session.commit()
        print(f"[OK] {len(users)} usuarios demo creados.")

        teacher = created_users['teacher']
        student = created_users['student']

        # ─── CURSO DEMO (Intro IA) ──────────────────────────────────────────
        print("[INFO] Sembrando curso 'Introducción a la Inteligencia Artificial'...")
        curso_intro = Course(
            title="Introducción a la Inteligencia Artificial",
            description="Explora los fundamentos de la inteligencia artificial, el aprendizaje automático y cómo los sistemas resuelven problemas complejos en el mundo real.",
            image_gradient="linear-gradient(135deg, #1a1a4e 0%, #4f46e5 50%, #00f2fe 100%)",
            image_url="https://images.unsplash.com/photo-1677442136019-21780efad99a?auto=format&fit=crop&w=800&q=80",
            level="Básico",
            duration_hours=8,
            price=19.99,
            instructor_id=teacher.id
        )
        db.session.add(curso_intro)
        db.session.commit()

        t_intro_1 = Topic(course_id=curso_intro.id, title="1. Conceptos Fundamentales de IA", order=1)
        db.session.add(t_intro_1)
        db.session.commit()

        c_intro_1 = Content(
            topic_id=t_intro_1.id,
            title="1.1 Qué es la Inteligencia Artificial y Ramas Principales",
            order=1,
            video_url="https://www.youtube.com/embed/2ePf9rue1Ao",
            body="""
<p>La <strong>Inteligencia Artificial (IA)</strong> es una de las áreas más fascinantes de la computación moderna. Su objetivo primordial es diseñar sistemas informáticos capaces de realizar tareas que, ejecutadas por seres humanos, requerirían procesos cognitivos complejos, tales como razonar, generalizar, aprender de la experiencia o percibir patrones.</p>

<h3>Ramas Principales de la IA</h3>
<ul>
    <li><strong>Sistemas Expertos:</strong> Sistemas basados en reglas lógicas programadas por humanos para tomar decisiones en nichos ultraespecializados.</li>
    <li><strong>Aprendizaje Automático (Machine Learning):</strong> Algoritmos que detectan patrones y refinan su desempeño directamente a partir de conjuntos de datos en lugar de seguir instrucciones rígidas.</li>
    <li><strong>Optimización Heurística y Evolutiva:</strong> Métodos de búsqueda estocástica inspirados en la naturaleza para hallar soluciones de calidad a problemas NP-completos donde los métodos exactos fallan por explosión combinatoria.</li>
</ul>

<div class="note-box cyan" style="background:rgba(0, 242, 254, 0.08); border-left:4px solid var(--neon-cyan); padding:1rem; margin:1.5rem 0; border-radius:4px;">
    <strong>💡 Nota Clave:</strong> A diferencia de un algoritmo tradicional secuencial que sigue pasos preestablecidos, un sistema inteligente modela el conocimiento de forma heurística o aprende dinámicamente ajustando sus coeficientes matemáticos.
</div>
"""
        )
        db.session.add(c_intro_1)
        db.session.commit()
        print(f"[OK] Curso 'Intro IA' configurado con éxito (ID: {curso_intro.id}).")


        # ─── CURSO DE ALGORITMOS GENÉTICOS (9 MÓDULOS) ──────────────────────
        print("[INFO] Sembrando curso extendido 'Algoritmos Genéticos en Python'...")
        curso_ga = Course(
            title="Algoritmos Genéticos en Python",
            description="Aprende a diseñar, optimizar e implementar algoritmos evolutivos en Python desde cero. Resuelve problemas de optimización combinatoria y numérica compleja de manera profesional.",
            image_gradient="linear-gradient(135deg, #0d2137 0%, #10b981 50%, #00f2fe 100%)",
            image_url="https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=800&q=80",
            level="Avanzado",
            duration_hours=20,
            price=49.99,
            instructor_id=teacher.id
        )
        db.session.add(curso_ga)
        db.session.commit()

        # MÓDULO 1
        m1 = Topic(course_id=curso_ga.id, title="1. Introducción a la Inteligencia Artificial", order=1)
        db.session.add(m1)
        db.session.commit()
        db.session.add(Content(
            topic_id=m1.id,
            title="1.1 Relación entre IA y los Algoritmos de Optimización",
            order=1,
            video_url="https://www.youtube.com/embed/MacV1T1eN0w",
            body="""
<p>La Inteligencia Artificial no solo comprende el análisis de datos masivos o el entrenamiento de redes neuronales profundas. Una gran parte de los problemas más complejos de la IA consiste en la <strong>optimización heurística</strong>.</p>

<p>Cuando nos enfrentamos a problemas de la vida real (como planificar rutas logísticas óptimas, programar horarios escolares o diseñar microchips), el espacio de búsqueda de soluciones es tan absurdamente gigantesco que calcular todas las combinaciones posibles demoraría billones de años. Este tipo de problemas se denominan <strong>NP-Hard</strong>.</p>

<h3>¿Por qué Optimizar?</h3>
<p>En lugar de una búsqueda a ciegas por fuerza bruta, requerimos algoritmos metaheurísticos guiados que exploren inteligentemente el espacio de búsqueda. Los <strong>Algoritmos Genéticos</strong> son, precisamente, una de las técnicas más robustas e inteligentes dentro de este ecosistema, permitiendo encontrar excelentes soluciones en un tiempo de cómputo razonable.</p>

<div class="note-box" style="background:rgba(139, 92, 246, 0.08); border-left:4px solid var(--neon-purple); padding:1rem; margin:1.5rem 0; border-radius:4px;">
    <strong>Definición Técnica:</strong> Optimizar significa hallar el conjunto de parámetros o variables de entrada $(x_1, x_2, ..., x_n)$ que maximizan o minimizan una función matemática objetivo $f(X)$, respetando ciertas restricciones físicas o lógicas.
</div>
"""
        ))

        # MÓDULO 2
        m2 = Topic(course_id=curso_ga.id, title="2. Introducción a los Algoritmos Genéticos", order=2)
        db.session.add(m2)
        db.session.commit()
        db.session.add(Content(
            topic_id=m2.id,
            title="2.1 Historia y Flujo Básico de la Evolución Artificial",
            order=1,
            video_url="https://www.youtube.com/embed/uQ2t9sJ7gB0",
            body="""
<p>Los <strong>Algoritmos Genéticos (AG)</strong> fueron concebidos originalmente en los años 70 por el científico de la computación <strong>John Holland</strong> en la Universidad de Michigan. Holland buscaba emular la flexibilidad y resiliencia de la selección natural y la evolución darwiniana directamente en sistemas de software.</p>

<h3>Analogía Biológica Básica</h3>
<table>
    <thead>
        <tr>
            <th>Concepto Biológico</th>
            <th>Equivalente Computacional</th>
            <th>Descripción</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Cromosoma / Individuo</td>
            <td>Vector / Cadena</td>
            <td>Una solución candidata para el problema.</td>
        </tr>
        <tr>
            <td>Gen</td>
            <td>Elemento / Bit</td>
            <td>Una variable individual de la solución.</td>
        </tr>
        <tr>
            <td>Aptitud (Fitness)</td>
            <td>Función de Costo / Rendimiento</td>
            <td>Qué tan buena es la solución actual.</td>
        </tr>
        <tr>
            <td>Población</td>
            <td>Matriz / Lista de soluciones</td>
            <td>Conjunto de soluciones explorando el espacio simultáneamente.</td>
        </tr>
    </tbody>
</table>

<h3>Flujo de Trabajo del Algoritmo Genético</h3>
<pre><code>[Inicio] Generar Población Inicial de manera aleatoria
   │
   ├─► [Evaluación] Calcular el 'Fitness' de cada individuo
   │
   ├─► [Condición de Término] ¿Se alcanzó la solución ideal o número de generaciones límite?
   │      🗲 Sí: Terminar y retornar el mejor individuo
   │      🗲 No: Continuar
   │
   ├─► [Selección] Seleccionar padres basados en su Fitness (sobreviven los mejores)
   │
   ├─► [Cruce (Crossover)] Combinar el material genético de los padres elegidos
   │
   ├─► [Mutación] Alterar aleatoriamente algunos genes con una tasa de mutación baja
   │
   └─► Reemplazar la población vieja con los nuevos descendientes e iniciar nuevo ciclo</code></pre>
"""
        ))

        # MÓDULO 3
        m3 = Topic(course_id=curso_ga.id, title="3. Individuos y Población", order=3)
        db.session.add(m3)
        db.session.commit()
        db.session.add(Content(
            topic_id=m3.id,
            title="3.1 Representaciones y Genotipos frente a Fenotipos",
            order=1,
            body="""
<p>Para implementar un algoritmo genético de manera efectiva, debemos separar conceptualmente dos mundos:</p>
<ol>
    <li><strong>El Genotipo:</strong> La representación interna cifrada del cromosoma (la codificación computacional, por ejemplo, una cadena de bits <code>010011</code> o un vector numérico).</li>
    <li><strong>El Fenotipo:</strong> La manifestación física o decodificada del individuo (la solución real en el dominio del problema, por ejemplo, una configuración geométrica o un horario de trabajo estructurado).</li>
</ol>

<h3>Tipos de Codificación de Cromosomas</h3>
<ul>
    <li><strong>Codificación Binaria:</strong> Los cromosomas son arreglos de bits (<code>0</code> y <code>1</code>). Es muy simple y fácil de operar matemáticamente.</li>
    <li><strong>Codificación de Valores Reales:</strong> Los cromosomas son vectores de números decimales (floats). Ideal para optimizar funciones matemáticas continuas o pesos de redes neuronales.</li>
    <li><strong>Codificación Permutada:</strong> Los genes representan una secuencia o ruta ordenada (e.g. <code>[3, 1, 4, 2]</code>). Fundamental para resolver el Problema del Viajante (TSP) donde no se permiten elementos repetidos.</li>
</ul>

<h3>Inicialización de la Población</h3>
<p>Por lo general, la población inicial se compone de $N$ individuos generados de manera aleatoria a través del espacio de búsqueda para garantizar una amplia <strong>diversidad genética</strong> desde el primer instante.</p>
"""
        ))

        # MÓDULO 4
        m4 = Topic(course_id=curso_ga.id, title="4. Función Fitness", order=4)
        db.session.add(m4)
        db.session.commit()
        db.session.add(Content(
            topic_id=m4.id,
            title="4.1 Diseño de Funciones de Aptitud y Penalizaciones",
            order=1,
            body="""
<p>La <strong>Función Fitness</strong> (o función de aptitud) es el corazón de la evolución. Es el único mecanismo mediante el cual el algoritmo distingue entre una solución pésima, una promedio y una extraordinaria.</p>

<p>Recibe como parámetro un individuo y devuelve un número real que cuantifica su calidad.</p>

<h3>Buenas Prácticas en el Diseño de Fitness</h3>
<ul>
    <li><strong>Gradiente Claro:</strong> Debe ser continua y guiar suavemente la búsqueda. Si la función retorna simplemente <code>1</code> (correcto) o <code>0</code> (incorrecto), el algoritmo no tendrá un gradiente que le guíe y la evolución colapsará en una búsqueda ciega.</li>
    <li><strong>Control de Restricciones (Penalización):</strong> Si una solución viola las restricciones del problema (por ejemplo, cargar en la mochila más peso del permitido), se le aplica una función de penalización proporcional para reducir drásticamente su aptitud:
    <pre><code>Fitness(Individuo) = Valor_Original - Penalización(Gravedad_Infracción)</code></pre>
    </li>
</ul>

<div class="note-box cyan" style="background:rgba(0, 242, 254, 0.08); border-left:4px solid var(--neon-cyan); padding:1rem; margin:1.5rem 0; border-radius:4px;">
    <strong>Ejemplo Práctico:</strong> Si optimizamos el consumo energético de un edificio, el fitness podría modelarse como la inversa del consumo de watts ($1 / E$). Así, menor consumo se traduce en mayor fitness (aptitud).
</div>
"""
        ))

        # MÓDULO 5
        m5 = Topic(course_id=curso_ga.id, title="5. Selección Natural", order=5)
        db.session.add(m5)
        db.session.commit()
        db.session.add(Content(
            topic_id=m5.id,
            title="5.1 Selección por Ruleta, Torneo y Ranking",
            order=1,
            body="""
<p>El operador de **Selección** decide cuáles individuos de la población actual sobrevivirán y tendrán la oportunidad de reproducirse. Imita la regla de "supervivencia del más apto". Un buen método equilibra la **presión selectiva** para no perder diversidad genética prematuramente.</p>

<h3>1. Selección por Ruleta (Proporcional al Fitness)</h3>
<p>La probabilidad $P_i$ de elegir al individuo $i$ es directamente proporcional a su aptitud individual dividida por la aptitud de toda la población:</p>
<div style="text-align:center; margin:1rem 0; font-size:1.25rem;">
    $$P_i = \\frac{Fitness_i}{\\sum_{j=1}^{N} Fitness_j}$$
</div>
<p>Se asemeja a girar una ruleta donde los sectores son proporcionales al tamaño del fitness. El problema es que si un individuo es excepcionalmente bueno, acaparará toda la ruleta rápidamente provocando convergencia prematura.</p>

<h3>2. Selección por Torneo</h3>
<p>Elegimos aleatoriamente un número $K$ de individuos de la población y realizamos un "enfrentamiento", seleccionando al que tenga el fitness más elevado. 
$K$ se denomina el tamaño del torneo. A mayor $K$, mayor es la presión selectiva.</p>

<pre><code class="language-python">import random

def tournament_selection(population, k=3):
    # Elegir k contendientes al azar
    contenders = random.sample(population, k)
    # El de mayor fitness gana el torneo
    return max(contenders, key=lambda ind: ind['fitness'])
</code></pre>
"""
        ))

        # MÓDULO 6
        m6 = Topic(course_id=curso_ga.id, title="6. Crossover o Cruce", order=6)
        db.session.add(m6)
        db.session.commit()
        db.session.add(Content(
            topic_id=m6.id,
            title="6.1 Operadores de Recombinación Genética",
            order=1,
            body="""
<p>El <strong>Cruce (Crossover)</strong> es el operador principal de exploración del algoritmo genético. Permite intercambiar y combinar las mejores características de dos padres seleccionados con la esperanza de generar descendientes aún mejores.</p>

<p>Habitualmente se define una probabilidad de cruce $P_c$ (normalmente entre $0.6$ y $0.9$). Si no se realiza el cruce, los hijos son clones idénticos de los padres.</p>

<h3>Técnicas Comunes de Cruce</h3>

<h4>Cruce de Un Punto</h4>
<p>Se selecciona un punto de corte aleatorio en la cadena cromosómica. La primera sección del Padre 1 se junta con la segunda sección del Padre 2 para formar el descendiente.</p>
<pre><code>Padre 1:  [A B C D] │ [E F G H]
Padre 2:  [1 2 3 4] │ [5 6 7 8]
                    ▼ Punto de corte en índice 4
Hijo 1:   [A B C D] ┼ [5 6 7 8]  -> [A B C D 5 6 7 8]
Hijo 2:   [1 2 3 4] ┼ [E F G H]  -> [1 2 3 4 E F G H]</code></pre>

<h4>Cruce Uniforme</h4>
<p>Para cada gen de los hijos, se lanza una moneda al aire (probabilidad 50%) para decidir si hereda el gen del Padre 1 o del Padre 2.</p>
"""
        ))

        # MÓDULO 7
        m7 = Topic(course_id=curso_ga.id, title="7. Mutación", order=7)
        db.session.add(m7)
        db.session.commit()
        db.session.add(Content(
            topic_id=m7.id,
            title="7.1 Tasa de Mutación y Prevención de Óptimos Locales",
            order=1,
            body="""
<p>Mientras que el cruce combina soluciones existentes, la <strong>Mutación</strong> inyecta material genético completamente nuevo y fresco en la población. Actúa como el motor de exploración en áreas inexploradas del espacio de búsqueda.</p>

<p>Sin mutación, si todos los cromosomas de la población convergen a tener un <code>0</code> en cierta posición, el cruce jamás podrá generar un descendiente con un <code>1</code> en esa misma posición. La población quedaría estancada permanentemente en un <strong>óptimo local</strong>.</p>

<h3>La Tasa de Mutación ($P_m$)</h3>
<p>La probabilidad de mutar un gen individual debe ser extremadamente baja (habitualmente entre $0.001$ y $0.05$). Una tasa demasiado alta degradaría el algoritmo genético transformándolo en una búsqueda puramente caótica al azar.</p>

<h3>Tipos de Operadores de Mutación</h3>
<ul>
    <li><strong>Mutación Flip-Bit:</strong> Para codificaciones binarias, consiste simplemente en negar el bit (cambiar <code>0</code> por <code>1</code> y viceversa).</li>
    <li><strong>Mutación de Intercambio (Swap Mutation):</strong> Para permutaciones (como el TSP), se eligen dos genes aleatorios del vector y se intercambian sus posiciones físicas de manera recíproca.</li>
</ul>

<div class="note-box" style="background:rgba(243, 85, 218, 0.08); border-left:4px solid var(--neon-magenta); padding:1rem; margin:1.5rem 0; border-radius:4px;">
    <strong>🧠 Evita la Convergencia Prematura:</strong> La mutación garantiza la diversidad de la población, actuando como una red de seguridad biológica contra el estancamiento evolutivo.
</div>
"""
        ))

        # MÓDULO 8
        m8 = Topic(course_id=curso_ga.id, title="8. Ejemplos prácticos en Python", order=8)
        db.session.add(m8)
        db.session.commit()
        db.session.add(Content(
            topic_id=m8.id,
            title="8.1 Solución del problema clásico One-Max desde Cero",
            order=1,
            body="""
<p>El problema <strong>One-Max</strong> es el 'Hello World' de la computación evolutiva. Consiste en encontrar una cadena binaria llena completamente de unos (<code>1</code>).</p>

<p>A continuación tienes una implementación modular, documentada e interactiva lista para ejecutarse directamente en Python.</p>

<pre><code class="language-python">import random

# CONFIGURACIÓN DE PARÁMETROS
CROMOSOMA_SIZE = 50
POBLACION_SIZE = 100
GENERACIONES_MAX = 100
TASA_CRUCE = 0.8
TASA_MUTACION = 0.02  # 2% por gen

def crear_individuo():
    # Genera un vector aleatorio de 0s y 1s
    return [random.choice([0, 1]) for _ in range(CROMOSOMA_SIZE)]

def calcular_fitness(individuo):
    # En el problema One-Max, el fitness es la suma de los unos
    return sum(individuo)

def seleccion_torneo(poblacion, k=3):
    torneo = random.sample(poblacion, k)
    return max(torneo, key=lambda ind: ind['fitness'])

def cruce_un_punto(padre1, padre2):
    if random.random() < TASA_CRUCE:
        punto = random.randint(1, CROMOSOMA_SIZE - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2
    return padre1.copy(), padre2.copy()

def mutar(cromosoma):
    for i in range(len(cromosoma)):
        if random.random() < TASA_MUTACION:
            # Niega el bit (flip-bit)
            cromosoma[i] = 1 - cromosoma[i]

# BUCLE EVOLUTIVO PRINCIPAL
def ejecutar_algoritmo():
    # 1. Población Inicial
    poblacion = [{'cromosoma': crear_individuo(), 'fitness': 0} for _ in range(POBLACION_SIZE)]
    
    for generacion in range(GENERACIONES_MAX):
        # 2. Evaluación
        for ind in poblacion:
            ind['fitness'] = calcular_fitness(ind['cromosoma'])
        
        # Ordenar población para encontrar al mejor líder
        poblacion.sort(key=lambda x: x['fitness'], reverse=True)
        mejor = poblacion[0]
        
        print(f"Gen {generacion}: Mejor Fitness = {mejor['fitness']}/{CROMOSOMA_SIZE}")
        
        if mejor['fitness'] == CROMOSOMA_SIZE:
            print("¡Solución óptima perfecta encontrada!")
            break
            
        # Generar la nueva descendencia
        nueva_poblacion = [mejor] # Preservamos al mejor líder (Elitismo)
        
        while len(nueva_poblacion) < POBLACION_SIZE:
            # 3. Selección de Padres
            p1 = seleccion_torneo(poblacion)
            p2 = seleccion_torneo(poblacion)
            
            # 4. Cruce
            h1_crom, h2_crom = cruce_un_punto(p1['cromosoma'], p2['cromosoma'])
            
            # 5. Mutación
            mutar(h1_crom)
            mutar(h2_crom)
            
            nueva_poblacion.append({'cromosoma': h1_crom, 'fitness': 0})
            if len(nueva_poblacion) < POBLACION_SIZE:
                nueva_poblacion.append({'cromosoma': h2_crom, 'fitness': 0})
                
        poblacion = nueva_poblacion

if __name__ == '__main__':
    ejecutar_algoritmo()
</code></pre>
"""
        ))

        # MÓDULO 9
        m9 = Topic(course_id=curso_ga.id, title="9. Aplicaciones reales", order=9)
        db.session.add(m9)
        db.session.commit()
        db.session.add(Content(
            topic_id=m9.id,
            title="9.1 TSP, Problema de la Mochila y Diseño Industrial",
            order=1,
            body="""
<p>Los Algoritmos Genéticos no son simples ejercicios académicos teóricos. Son utilizados diariamente en la industria tecnológica para optimizar infraestructuras de millones de dólares.</p>

<h3>Aplicaciones Prácticas Destacadas</h3>
<ul>
    <li><strong>El Problema de la Mochila (Knapsack Problem):</strong> Optimizar de forma óptima el espacio de almacenamiento o la selección de inversiones en portafolios financieros bajo un presupuesto estricto.</li>
    <li><strong>El Problema del Viajante (TSP - Traveling Salesperson Problem):</strong> Diseño de rutas de reparto logístico (utilizado por gigantes como DHL, UPS y Amazon) para ahorrar combustible y tiempo al visitar múltiples ciudades en una sola pasada.</li>
    <li><strong>Diseño Aeroespacial e Ingeniería:</strong> La NASA utilizó algoritmos genéticos evolutivos para modelar la antena ST5 de una de sus misiones satelitales. El diseño evolucionado arrojó una geometría orgánica no intuitiva que superaba con creces el rendimiento de cualquier diseño hecho por ingenieros expertos.</li>
    <li><strong>Optimización de Pesos en Redes Neuronales (Neuroevolución):</strong> Una alternativa potente al algoritmo de Backpropagation tradicional para entrenar arquitecturas complejas de redes neuronales artificiales cuando no hay derivadas disponibles.</li>
</ul>

<p>Felicidades, has concluido el temario de estudio de los algoritmos genéticos evolutivos. ¡Ahora estás listo para aplicar la evolución artificial y resolver los problemas más desafiantes del mundo real!</p>
"""
        ))
        db.session.commit()
        print(f"[OK] Curso 'Algoritmos Genéticos' configurado con éxito con 9 módulos completos.")

        # ─── TRAYECTORIA DE COMPETENCIA (Roadmaps) ──────────────────────────
        print("[INFO] Sembrando trayectorias de competencia...")
        rm = Roadmap(
            title="Ingeniero en Algoritmos Inteligentes",
            description="Domina los fundamentos de la inteligencia artificial moderna y los algoritmos evolutivos para especializarte en problemas complejos de optimización y sistemas computacionales avanzados.",
            icon="🧠",
            color_start="#00f2fe",
            color_end="#8b5cf6"
        )
        db.session.add(rm)
        db.session.commit()

        # Asociar cursos en orden
        rm_courses = [
            (curso_intro.id, 1),
            (curso_ga.id, 2)
        ]
        for course_id, order in rm_courses:
            db.session.add(RoadmapCourse(roadmap_id=rm.id, course_id=course_id, order=order))
        db.session.commit()
        print(f"[OK] Trayectoria '{rm.title}' creada con sus enlaces a cursos correspondientes.")

        # ─── SEMBRAR INSCRIPCIÓN Y BITÁCORA DEMO PARA ESTUDIANTE 1 ──────────
        print("[INFO] Sembrando inscripciones demo e historial para 'estudiante1'...")
        # Inscribir estudiante 1 al curso 1 (Intro IA) con 0%
        db.session.add(Enrollment(user_id=student.id, course_id=curso_intro.id, progress=0.0))
        
        # Historial de actividades iniciales
        logs = [
            ActivityLog(user_id=student.id, activity_type='enroll_course', description="Te inscribiste en el curso 'Introducción a la Inteligencia Artificial'."),
        ]
        for log in logs:
            db.session.add(log)
        
        db.session.commit()
        print("[SUCCESS] Siembra completa de NovaFlux Academy exitosa con todas las tablas e historial.")

if __name__ == '__main__':
    seed_data()
