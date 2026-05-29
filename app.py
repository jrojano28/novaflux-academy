# app.py
# Punto de entrada principal oficial de la aplicación AntiGravity (NovaFlux Academy).
# Optimizado para ejecución en servidores de desarrollo, producción (Gunicorn/UWSGI) y herramientas CLI de Flask.

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ejecución local de desarrollo
    app.run(host='127.0.0.1', port=5000, debug=True)
