import json
import os
from typing import List, Dict, Any


class DataManager:
    """Clase encargada del almacenamiento y persistencia de datos en formato JSON."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()

    def _ensure_data_directory(self) -> None:
        """Crea la carpeta de datos si aún no existe."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_file_path(self, filename: str) -> str:
        """Retorna la ruta completa de un archivo dentro del directorio de datos."""
        return os.path.join(self.data_dir, filename)

    def save_data(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """Guarda una lista de diccionarios en un archivo JSON."""
        file_path = self._get_file_path(filename)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"[ERROR] No se pudo guardar en {filename}: {e}")
            return False

    def load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Carga y retorna los datos desde un archivo JSON."""
        file_path = self._get_file_path(filename)
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            print(f"[ERROR] Error al leer {filename}: {e}")
            return []


# Instancia global reutilizable para la Célula 2
data_manager = DataManager()