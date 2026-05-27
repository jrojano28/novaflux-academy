# tests/test_routes.py
# Pruebas automatizadas básicas para verificar que las rutas principales respondan correctamente.

import sys
import os

# Agregar la raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

def test_routes():
    app = create_app()
    client = app.test_client()

    print("Iniciando pruebas de rutas...")

    # Probar ruta inicio
    res_home = client.get('/')
    assert res_home.status_code == 200, f"Error en Inicio: {res_home.status_code}"
    print("[OK] Ruta de Inicio ('/') responde con 200.")

    # Probar lista de cursos
    res_courses = client.get('/courses/')
    assert res_courses.status_code == 200, f"Error en Lista de Cursos: {res_courses.status_code}"
    print("[OK] Ruta de Cursos ('/courses/') responde con 200.")

    # Probar detalle de curso 1 (Demo)
    res_detail = client.get('/courses/1')
    assert res_detail.status_code == 200, f"Error en Detalle de Curso 1: {res_detail.status_code}"
    print("[OK] Ruta de Detalle ('/courses/1') responde con 200.")

    # Probar detalle de curso 2 (Algoritmos Genéticos)
    res_detail2 = client.get('/courses/2')
    assert res_detail2.status_code == 200, f"Error en Detalle de Curso 2: {res_detail2.status_code}"
    print("[OK] Ruta de Detalle ('/courses/2') responde con 200.")

    print("\n¡Todas las pruebas pasaron con éxito!")

if __name__ == '__main__':
    test_routes()
