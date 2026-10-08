import sys
from pathlib import Path

# Agrega la carpeta src al path para asegurar
# que los módulos internos puedan importarse correctamente.
SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ui.cli_interface import iniciar_interfaz


def main():
    """Punto de entrada principal del sistema."""
    iniciar_interfaz()


if __name__ == "__main__":
    main()