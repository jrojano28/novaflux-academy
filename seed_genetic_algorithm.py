# seed_genetic_algorithm.py
# Script para cargar el curso de Algoritmos Genéticos (9 módulos), usuarios demo, trayectorias de competencia e interacciones.

from app import create_app
from app.models import db
from app.models.user import User, ActivityLog
from app.models.course import Course, Enrollment, Roadmap, RoadmapCourse, RoadmapEnrollment
from app.models.topic import Topic, Content

app = create_app()

def seed_data():
    with app.app_context():
        print("[INFO] Recreando base de datos con el nuevo esquema...")
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
            level="Básico",
            duration_hours=8,
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
            body="""
<p>La <strong>Inteligencia Artificial (IA)</strong> es una de las áreas más fascinantes de la computación moderna. Su objetivo primordial es diseñar sistemas informáticos capaces de realizar tareas que, ejecutadas por seres humanos, requerirían procesos cognitivos complejos, tales como razonar, generalizar, aprender de la experiencia o percibir patrones.</p>

<h3>Ramas Principales de la IA</h3>
<ul>
    <li><strong>Sistemas Expertos:</strong> Sistemas basados en reglas lógicas programadas por humanos para tomar decisiones en nichos ultraespecializados.</li>
    <li><strong>Aprendizaje Automático (Machine Learning):</strong> Algoritmos que detectan patrones y refinan su desempeño directamente a partir de conjuntos de datos.</li>
    <li><strong>Optimización Heurística y Evolutiva:</strong> Métodos de búsqueda inspirados en la naturaleza para hallar excelentes soluciones a problemas complejos de forma rápida.</li>
</ul>

<div class="note-box cyan">
    <div class="note-box-title">💡 Nota Clave</div>
    A diferencia de un programa secuencial tradicional rígido, un sistema inteligente de optimización busca dinámicamente y se adapta usando heurísticas guiadas.
</div>

<!-- PLAYGROUND DE PYTHON 1 -->
<div class="interactive-playground">
    <div class="playground-header">
        <h4>💻 Laboratorio Práctico: Variables y Salidas en Python</h4>
        <span class="playground-badge">Python Básico</span>
    </div>
    <div class="playground-editor-container">
        <textarea class="playground-editor"># Crea una variable para tu puntuación inteligente
score = 100
print("Mi puntuación en AntiGravity es:", score)</textarea>
    </div>
    <div class="playground-actions">
        <button class="btn-primary btn-playground-run">Ejecutar Código →</button>
    </div>
    <div class="playground-console-card">
        <div class="playground-console-header">🐚 Consola de Salida:</div>
        <pre class="playground-console-output">Haz clic en 'Ejecutar Código' para ver la salida aquí...</pre>
    </div>
</div>

<!-- QUIZ 1 -->
<div class="interactive-quiz">
    <div class="quiz-header">📝 Mini Reto: Comprueba lo aprendido</div>
    <div class="quiz-question">¿Cuál es el objetivo primordial de la Inteligencia Artificial (IA)?</div>
    <div class="quiz-options">
        <div class="quiz-option" data-correct="false">
            <input type="radio" name="quiz-ia-opt" id="opt-ia-1">
            <span class="quiz-option-label">A) Crear procesadores de texto más rápidos</span>
        </div>
        <div class="quiz-option" data-correct="true">
            <input type="radio" name="quiz-ia-opt" id="opt-ia-2">
            <span class="quiz-option-label">B) Construir sistemas capaces de realizar tareas complejas imitando procesos cognitivos humanos ✅</span>
        </div>
        <div class="quiz-option" data-correct="false">
            <input type="radio" name="quiz-ia-opt" id="opt-ia-3">
            <span class="quiz-option-label">C) Aumentar la velocidad de almacenamiento en disco</span>
        </div>
    </div>
    <div class="quiz-footer">
        <button class="btn-secondary btn-quiz-verify">Verificar Respuesta</button>
        <div class="quiz-feedback"></div>
    </div>
</div>
"""
        )
        db.session.add(c_intro_1)
        db.session.commit()
        print(f"[OK] Curso 'Intro IA' configurado con éxito.")


        # ─── CURSO DE ALGORITMOS GENÉTICOS (9 MÓDULOS) ──────────────────────
        print("[INFO] Sembrando curso extendido 'Algoritmos Genéticos en Python'...")
        curso_ga = Course(
            title="Algoritmos Genéticos en Python",
            description="Aprende a diseñar, optimizar e implementar algoritmos evolutivos en Python desde cero. Resuelve problemas de optimización combinatoria y numérica compleja de manera profesional.",
            image_gradient="linear-gradient(135deg, #0d2137 0%, #10b981 50%, #00f2fe 100%)",
            level="Avanzado",
            duration_hours=20,
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
            body="""
<p>La Inteligencia Artificial no solo comprende el análisis de datos masivos o redes neuronales. Una gran parte de los problemas de la vida real consiste en la <strong>optimización heurística</strong>.</p>

<p>Cuando nos enfrentamos a problemas del mundo real (como planificar rutas logísticas óptimas, programar horarios escolares o diseñar componentes), el espacio de búsqueda de soluciones es tan gigantesco que calcular todas las combinaciones demoraría millones de años.</p>

<h3>¿Por qué Optimizar?</h3>
<p>En lugar de una búsqueda por fuerza bruta a ciegas, requerimos algoritmos metaheurísticos guiados que exploren inteligentemente el espacio de búsqueda. Los <strong>Algoritmos Genéticos</strong> son, precisamente, una de las técnicas más robustas e inteligentes dentro de este ecosistema.</p>

<!-- PLAYGROUND DE PYTHON 2 -->
<div class="interactive-playground">
    <div class="playground-header">
        <h4>💻 Laboratorio Práctico: Iteraciones en Python</h4>
        <span class="playground-badge">Bucles Simples</span>
    </div>
    <div class="playground-editor-container">
        <textarea class="playground-editor"># Un bucle simple que simula 5 iteraciones evolutivas
for gen in range(1, 6):
    print("Evaluando Generación:", gen)</textarea>
    </div>
    <div class="playground-actions">
        <button class="btn-primary btn-playground-run">Ejecutar Código →</button>
    </div>
    <div class="playground-console-card">
        <div class="playground-console-header">🐚 Consola de Salida:</div>
        <pre class="playground-console-output">Haz clic en 'Ejecutar Código' para ver la salida aquí...</pre>
    </div>
</div>

<!-- QUIZ 2 -->
<div class="interactive-quiz">
    <div class="quiz-header">📝 Mini Reto: Optimización</div>
    <div class="quiz-question">¿Por qué no usamos la fuerza bruta para resolver problemas de optimización complejos de la vida real?</div>
    <div class="quiz-options">
        <div class="quiz-option" data-correct="true">
            <input type="radio" name="quiz-opt-2" id="opt-2-1">
            <span class="quiz-option-label">A) Porque el espacio de búsqueda es tan gigantesco que tardaría demasiado tiempo calcular todas las opciones. ✅</span>
        </div>
        <div class="quiz-option" data-correct="false">
            <input type="radio" name="quiz-opt-2" id="opt-2-2">
            <span class="quiz-option-label">B) Porque la fuerza bruta solo sirve para números decimales.</span>
        </div>
    </div>
    <div class="quiz-footer">
        <button class="btn-secondary btn-quiz-verify">Verificar Respuesta</button>
        <div class="quiz-feedback"></div>
    </div>
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
            body="""
<p>Los <strong>Algoritmos Genéticos (AG)</strong> emulan la flexibilidad y resiliencia de la selección natural y la evolución darwiniana directamente en sistemas de software.</p>

<h3>Analogía Biológica Básica</h3>
<ul>
    <li><strong>Individuo:</strong> Una solución candidata para el problema.</li>
    <li><strong>Gen:</strong> Una variable individual de la solución.</li>
    <li><strong>Aptitud (Fitness):</strong> Qué tan buena es la solución actual.</li>
    <li><strong>Población:</strong> Conjunto de soluciones explorando el espacio simultáneamente.</li>
</ul>

<div class="note-box purple">
    <div class="note-box-title">🧬 Evolución Digital</div>
    La población inicial se compone de individuos generados al azar. Mediante Selección (picks), Cruce (combinación) y Mutación (cambios aleatorios), la población evoluciona hacia la solución óptima.
</div>

<!-- SIMULACIÓN VISUAL EVOLUCIÓN DE ADN -->
<div class="interactive-simulator">
    <div class="simulator-header">
        <h4>🧬 Simulación Visual: Evolución de Cromosomas</h4>
        <span class="simulator-badge">Darwinismo Digital</span>
    </div>
    <div class="simulator-body">
        <div class="simulator-controls">
            <button class="btn-primary btn-simulator-action" id="btn-evolve-dna">Evolucionar Generación ⚡</button>
        </div>
        <div class="simulator-display">
            <div class="chromosome-list" id="evolve-dna-list">
                <div class="chromosome-card-visual">
                    <span class="chromosome-index">Indiv. 1</span>
                    <span class="chromosome-dna">🧬 <span class="dna-char">A</span><span class="dna-char">A</span><span class="dna-char">B</span><span class="dna-char">B</span></span>
                    <span class="chromosome-fitness-val">Aptitud: 2/4</span>
                </div>
                <div class="chromosome-card-visual">
                    <span class="chromosome-index">Indiv. 2</span>
                    <span class="chromosome-dna">🧬 <span class="dna-char">A</span><span class="dna-char">B</span><span class="dna-char">A</span><span class="dna-char">B</span></span>
                    <span class="chromosome-fitness-val">Aptitud: 2/4</span>
                </div>
                <div class="chromosome-card-visual">
                    <span class="chromosome-index">Indiv. 3</span>
                    <span class="chromosome-dna">🧬 <span class="dna-char">B</span><span class="dna-char">B</span><span class="dna-char">A</span><span class="dna-char">A</span></span>
                    <span class="chromosome-fitness-val">Aptitud: 2/4</span>
                </div>
                <div class="chromosome-card-visual">
                    <span class="chromosome-index">Indiv. 4</span>
                    <span class="chromosome-dna">🧬 <span class="dna-char">A</span><span class="dna-char">A</span><span class="dna-char">A</span><span class="dna-char">A</span></span>
                    <span class="chromosome-fitness-val">Aptitud: 0/4</span>
                </div>
            </div>
            <div class="simulator-stats-row">
                <span>Generación: <strong id="evolve-dna-gen">1</strong></span>
                <span>Aptitud Máxima: <strong id="evolve-dna-max-fitness">2</strong>/4</span>
            </div>
        </div>
    </div>
</div>
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
    <li><strong>El Genotipo:</strong> La representación interna cifrada del cromosoma (por ejemplo, una cadena de bits <code>010011</code> o un vector numérico).</li>
    <li><strong>El Fenotipo:</strong> La manifestación real o decodificada del individuo en el problema (por ejemplo, una configuración de horarios).</li>
</ol>

<h3>Tipos de Codificación de Cromosomas</h3>
<ul>
    <li><strong>Codificación Binaria:</strong> Los cromosomas son arreglos de bits (<code>0</code> y <code>1</code>). Es muy simple y fácil de operar.</li>
    <li><strong>Codificación de Valores Reales:</strong> Los cromosomas son vectores de números decimales. Ideal para problemas numéricos continuos.</li>
    <li><strong>Codificación Permutada:</strong> Secuencias ordenadas de elementos (e.g. rutas lógicas).</li>
</ul>
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
<p>La <strong>Función Fitness</strong> (o función de aptitud) es el corazón de la evolución. Es el único mecanismo mediante el cual el algoritmo distingue entre soluciones pésimas y extraordinarias.</p>

<p>Recibe un individuo y devuelve un número real que cuantifica su calidad.</p>

<div class="note-box cyan">
    <div class="note-box-title">⚙️ Diseño de Fitness</div>
    Debe guiar suavemente la búsqueda. Si la función retorna simplemente 1 (correcto) o 0 (incorrecto), el algoritmo no tendrá un gradiente que guiar y se asemejará a buscar a ciegas.
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
<p>El operador de **Selección** decide cuáles individuos de la población actual sobrevivirán y tendrán la oportunidad de reproducirse, imitando la supervivencia del más apto.</p>

<h3>Selección por Torneo</h3>
<p>Elegimos aleatoriamente un número $K$ de individuos de la población y realizamos un "enfrentamiento", seleccionando al que tenga el fitness más elevado. El ganador se convertirá en un padre para la próxima generación.</p>

<!-- SIMULADOR DE SELECCIÓN POR TORNEO -->
<div class="interactive-simulator">
    <div class="simulator-header">
        <h4>👑 Simulador de Selección por Torneo</h4>
        <span class="simulator-badge">Presión Selectiva</span>
    </div>
    <div class="simulator-body">
        <div class="simulator-controls">
            <div class="simulator-field">
                <label for="tournament-size-input">Tamaño del Torneo (K):</label>
                <input type="number" id="tournament-size-input" value="3" min="2" max="6">
            </div>
            <button class="btn-primary btn-simulator-action" id="btn-run-tournament">Correr Torneo ⚔️</button>
        </div>
        <div class="simulator-display">
            <div class="chromosome-list" id="tournament-dna-list">
                <p style="color:var(--text-muted); font-size:0.9rem; text-align:center; padding:1.5rem 0; margin:0;">
                    Haz clic en 'Correr Torneo' para enfrentar K cromosomas al azar y seleccionar al más apto.
                </p>
            </div>
        </div>
    </div>
</div>
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
<p>El <strong>Cruce (Crossover)</strong> es el operador principal de exploración. Permite intercambiar y combinar las mejores características de dos padres seleccionados con la esperanza de generar descendientes aún mejores.</p>

<h3>Cruce de Un Punto</h3>
<p>Se selecciona un punto de corte aleatorio en la cadena cromosómica. La primera sección del Padre 1 se junta con la segunda sección del Padre 2 para formar el descendiente.</p>
<pre><code>Padre 1:  [A B C D] │ [E F G H]
Padre 2:  [1 2 3 4] │ [5 6 7 8]
                    ▼ Punto de corte
Hijo 1:   [A B C D] ┼ [5 6 7 8]  -> [A B C D 5 6 7 8]</code></pre>
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
<p>Mientras que el cruce combina soluciones existentes, la <strong>Mutación</strong> inyecta material genético completamente nuevo y fresco en la población, garantizando la diversidad y evitando estancarse en óptimos locales.</p>

<h3>La Tasa de Mutación ($P_m$)</h3>
<p>La probabilidad de mutar un gen individual debe ser baja (entre $0.01$ y $0.2$). Una tasa demasiado alta degradaría el algoritmo transformándolo en una búsqueda caótica aleatoria.</p>

<!-- SIMULADOR DE MUTACIÓN -->
<div class="interactive-simulator">
    <div class="simulator-header">
        <h4>⚡ Simulador de Mutación Flip-Bit</h4>
        <span class="simulator-badge">Exploración Genética</span>
    </div>
    <div class="simulator-body">
        <div class="simulator-controls">
            <div class="simulator-field">
                <label for="mutation-input-dna">Cromosoma Binario:</label>
                <input type="text" id="mutation-input-dna" value="10101010" maxlength="12">
            </div>
            <div class="simulator-field">
                <label for="mutation-rate-input">Tasa de Mutación (Pm):</label>
                <input type="number" id="mutation-rate-input" value="0.20" step="0.05" min="0.01" max="0.90">
            </div>
            <button class="btn-primary btn-simulator-action" id="btn-run-mutation">Mutar ADN ⚡</button>
        </div>
        <div class="simulator-display">
            <div class="chromosome-list" id="mutation-dna-list">
                <p style="color:var(--text-muted); font-size:0.9rem; text-align:center; padding:1.5rem 0; margin:0;">
                    Haz clic en 'Mutar ADN' para ver cómo la probabilidad Pm altera bits específicos.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- QUIZ 3 -->
<div class="interactive-quiz">
    <div class="quiz-header">📝 Mini Reto: Mutación</div>
    <div class="quiz-question">¿Cuál es el rol principal de la mutación en un Algoritmo Genético?</div>
    <div class="quiz-options">
        <div class="quiz-option" data-correct="false">
            <input type="radio" name="quiz-opt-3" id="opt-3-1">
            <span class="quiz-option-label">A) Clonar exactamente a los mejores padres.</span>
        </div>
        <div class="quiz-option" data-correct="true">
            <input type="radio" name="quiz-opt-3" id="opt-3-2">
            <span class="quiz-option-label">B) Inyectar material genético nuevo para mantener la diversidad y evitar óptimos locales. ✅</span>
        </div>
        <div class="quiz-option" data-correct="false">
            <input type="radio" name="quiz-opt-3" id="opt-3-3">
            <span class="quiz-option-label">C) Reducir el fitness de toda la población.</span>
        </div>
    </div>
    <div class="quiz-footer">
        <button class="btn-secondary btn-quiz-verify">Verificar Respuesta</button>
        <div class="quiz-feedback"></div>
    </div>
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
<p>El problema <strong>One-Max</strong> consiste en encontrar una cadena binaria llena completamente de unos (<code>1</code>).</p>

<p>A continuación tienes un laboratorio práctico donde puedes experimentar directamente evaluando el fitness del problema One-Max de forma sencilla.</p>

<!-- PLAYGROUND DE PYTHON 3 -->
<div class="interactive-playground">
    <div class="playground-header">
        <h4>💻 Laboratorio Práctico: Evaluando el Fitness de One-Max</h4>
        <span class="playground-badge">Función Fitness</span>
    </div>
    <div class="playground-editor-container">
        <textarea class="playground-editor">def fitness_onemax(cromosoma):
    # En el problema One-Max, el fitness es la suma de los unos
    return sum(cromosoma)

# Probemos un cromosoma binario
mi_adn = [1, 0, 1, 1, 0, 1, 1, 1]
print("Fitness de mi cromosoma binario:", fitness_onemax(mi_adn))</textarea>
    </div>
    <div class="playground-actions">
        <button class="btn-primary btn-playground-run">Ejecutar Código →</button>
    </div>
    <div class="playground-console-card">
        <div class="playground-console-header">🐚 Consola de Salida:</div>
        <pre class="playground-console-output">Haz clic en 'Ejecutar Código' para ver la salida aquí...</pre>
    </div>
</div>
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
<p>Los Algoritmos Genéticos se utilizan diariamente en la industria tecnológica para optimizar infraestructuras de millones de dólares.</p>

<h3>Aplicaciones Prácticas Destacadas</h3>
<ul>
    <li><strong>El Problema de la Mochila:</strong> Optimizar la selección de inversiones o almacenamiento bajo presupuesto estricto.</li>
    <li><strong>El Problema del Viajante (TSP):</strong> Diseño de rutas de reparto logístico (DHL, Amazon) para ahorrar combustible.</li>
    <li><strong>Diseño de Antenas evolutivas:</strong> La NASA utilizó algoritmos genéticos evolutivos para modelar antenas óptimas con geometrías no intuitivas.</li>
</ul>

<p>Felicidades, has concluido el temario de estudio de los algoritmos genéticos evolutivos. ¡Ahora estás listo para aplicar la evolución artificial y resolver los problemas más desafiantes del mundo real!</p>
"""
        ))
        db.session.commit()
        print(f"[OK] Curso 'Algoritmos Genéticos' configurado con éxito.")

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

        rm_courses = [
            (curso_intro.id, 1),
            (curso_ga.id, 2)
        ]
        for course_id, order in rm_courses:
            db.session.add(RoadmapCourse(roadmap_id=rm.id, course_id=course_id, order=order))
        db.session.commit()
        print(f"[OK] Trayectoria '{rm.title}' creada.")

        # ─── SEMBRAR INSCRIPCIÓN Y BITÁCORA DEMO PARA ESTUDIANTE 1 ──────────
        print("[INFO] Sembrando inscripciones demo e historial para 'estudiante1'...")
        db.session.add(Enrollment(user_id=student.id, course_id=curso_intro.id, progress=0.0))
        
        logs = [
            ActivityLog(user_id=student.id, activity_type='enroll_course', description="Te inscribiste en el curso 'Introducción a la Inteligencia Artificial'."),
        ]
        for log in logs:
            db.session.add(log)
        
        db.session.commit()
        print("[SUCCESS] Siembra completa de AntiGravity exitosa.")

if __name__ == '__main__':
    seed_data()
