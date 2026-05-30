import sys
import os

# Agregar el directorio del proyecto al path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from main import app as application
