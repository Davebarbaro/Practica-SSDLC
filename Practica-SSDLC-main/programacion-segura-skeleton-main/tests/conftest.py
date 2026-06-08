"""
Configuración de pytest para los tests.
Añade el directorio raíz al PYTHONPATH para que los imports funcionen.
"""
import sys
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))   # Se asegura que el directorio este al inicio del path
