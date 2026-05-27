# run.py
# Punto de entrada principal para ejecutar la aplicación Flask.

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
