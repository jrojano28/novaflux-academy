# AntiGravity Academy - Plataforma Web de Cursos Online (MVC)

¡Bienvenido a **AntiGravity Academy**! Esta es una plataforma web de educación en línea diseñada paso a paso utilizando Python y la arquitectura de diseño **Modelo-Vista-Controlador (MVC)**. El proyecto ha sido desarrollado de forma colaborativa para un equipo de 3 personas.

---

## 🚀 Características Principales

*   **Arquitectura MVC Limpia:** Separación estricta entre Modelos (datos), Controladores (rutas y lógica) y Vistas (HTML, CSS y JS).
*   **Base de Datos Relacional:** Configurada con **SQLite** y gestionada mediante **SQLAlchemy** (ORM).
*   **Interfaz de Usuario Premium:** Tema oscuro ("SaaS Developer Theme") moderno, responsivo y dinámico, construido con Vanilla CSS y diseñado para asombrar a primera vista.
*   **Lector Interactiva de Cursos (SPA-like):** Permite cambiar de lecciones en tiempo real mediante JavaScript sin recargar la página completa.
*   **Tests de Integración:** Incluye pruebas automatizadas para garantizar la estabilidad de las rutas principales del sistema.
*   **Curso Incluido:** Contenido completo y detallado sobre **Algoritmos Genéticos en Python** con explicaciones teóricas y código fuente funcional.

---

## 🛠️ Stack Tecnológico

*   **Lenguaje:** Python 3.x
*   **Backend:** Flask (con Flask-SQLAlchemy)
*   **Base de Datos:** SQLite (para desarrollo local)
*   **Frontend:** HTML5 semántico + CSS3 (Variables avanzadas, Glassmorphism, animaciones) + JavaScript ES6
*   **Pruebas:** Unittest incorporado de Flask
*   **Control de Versiones:** Git & GitHub

---

## 📂 Estructura de Carpetas

```
taller-ia/
├── app/
│   ├── __init__.py           # Inicialización de Flask y conexión BD/Controladores
│   ├── config.py             # Parámetros y claves de configuración
│   ├── models/               # [MODELOS] Esquemas de base de datos SQL
│   │   ├── __init__.py
│   │   ├── user.py           # Tabla de Usuarios y hashes de seguridad
│   │   ├── course.py         # Tabla de Cursos y relaciones
│   │   └── topic.py          # Tablas de Temas y Contenidos de lección
│   ├── controllers/          # [CONTROLADORES] Lógica de rutas
│   │   ├── __init__.py
│   │   ├── main_controller.py   # Enrutamiento de landing page
│   │   └── course_controller.py # Enrutamiento de catálogo y visor
│   └── views/                # [VISTAS] Presentación visual
│       ├── templates/        # Plantillas HTML con Jinja2
│       │   ├── base.html
│       │   ├── home.html
│       │   ├── courses.html
│       │   └── detail.html
│       └── static/           # Archivos estáticos
│           ├── css/
│           │   └── style.css # Estilos globales premium
│           └── js/
│               └── main.js   # Interactividad del sidebar lector
├── instance/                 # Almacén de base de datos SQLite (local)
├── tests/                    # Pruebas automatizadas de enrutamiento
│   └── test_routes.py
├── init_db.py                # Script de creación física de tablas de BD
├── seed_genetic_algorithm.py # Script de carga académica del curso AG
├── requirements.txt          # Dependencias del proyecto
└── run.py                    # Punto de entrada de la aplicación
```

---

## 💻 Instrucciones de Instalación y Uso

Sigue estos sencillos pasos para clonar, instalar y arrancar la plataforma en tu entorno de desarrollo local.

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd taller-ia
```

### 2. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
En macOS o Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos SQL
Este script creará las tablas necesarias en la base de datos local SQLite:
```bash
python init_db.py
```

### 5. Cargar el contenido del curso de Algoritmos Genéticos
Este script poblará la base de datos con el temario y lecciones completas del curso de Algoritmos Genéticos:
```bash
python seed_genetic_algorithm.py
```

### 6. Ejecutar la aplicación
Arranca el servidor local en modo desarrollo:
```bash
python run.py
```
Abre tu navegador e ingresa a: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 7. Ejecutar pruebas automatizadas
Para comprobar que el enrutamiento y la renderización funcionan correctamente:
```bash
python tests/test_routes.py
```

---

## 👥 Colaboración y Trabajo en Grupo (3 Integrantes)

Para mantener un flujo de trabajo limpio y sin conflictos en Git, se aconseja seguir el estándar **Git Flow**:
1. Crear ramas descriptivas para cada tarea: `git checkout -b feature/nombre-de-la-rama`
2. Realizar Commits atómicos y descriptivos.
3. Subir la rama a GitHub y abrir un **Pull Request (PR)** para revisión de los compañeros antes de integrar a la rama principal (`main`).
