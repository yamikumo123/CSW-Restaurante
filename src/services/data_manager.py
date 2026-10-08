import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class DataManagerError(Exception):
    """Excepción base para errores en el módulo de gestión de datos."""
    pass


class FileSaveError(DataManagerError):
    """Lanzada cuando ocurre un error al intentar guardar un archivo."""
    pass


class FileLoadError(DataManagerError):
    """Lanzada cuando ocurre un error al intentar leer o parsear un archivo."""
    pass


class DataManager:
    """Clase encargada de la persistencia de datos (JSON/CSV) para la Célula 2.
    
    Proporciona lectura y escritura segura mediante archivos temporales
    y manejo explícito de excepciones de persistencia.
    """

    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self._ensure_data_directory()

    def _ensure_data_directory(self) -> None:
        """Garantiza la existencia del directorio de persistencia."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise DataManagerError(f"No se pudo crear el directorio de datos: {e}")

    def _get_file_path(self, filename: str) -> Path:
        """Retorna la ruta absoluta formateada dentro del directorio de datos."""
        return self.data_dir / filename

    def save_json(self, filename: str, data: List[Dict[str, Any]]) -> None:
        """Guarda una lista de objetos/diccionarios en un archivo JSON de forma atómica.
        
        Args:
            filename: Nombre del archivo de destino (ej. 'mesas.json').
            data: Lista de diccionarios con la información a almacenar.

        Raises:
            FileSaveError: Si no se puede escribir o reemplazar el archivo.
        """
        file_path = self._get_file_path(filename)
        temp_path = file_path.with_suffix(".tmp")

        try:
            # Escritura en archivo temporal para evitar corrupción
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            
            # Reemplazo atómico
            temp_path.replace(file_path)
        except (IOError, TypeError) as e:
            if temp_path.exists():
                temp_path.unlink()
            raise FileSaveError(f"Error al guardar datos en {filename}: {e}")

    def load_json(self, filename: str) -> List[Dict[str, Any]]:
        """Carga y retorna los datos desde un archivo JSON.
        
        Args:
            filename: Nombre del archivo a leer (ej. 'pedidos.json').

        Returns:
            List[Dict[str, Any]]: Lista de elementos recuperados del archivo.

        Raises:
            FileLoadError: Si el archivo existe pero su contenido está corrupto o ilegible.
        """
        file_path = self._get_file_path(filename)
        
        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            raise FileLoadError(f"Error al leer o procesar {filename}: {e}")

    def export_csv(self, filename: str, data: List[Dict[str, Any]], fieldnames: List[str]) -> None:
        """Exporta una lista de diccionarios a un archivo CSV.
        
        Args:
            filename: Nombre del archivo CSV a generar (ej. 'reporte_ventas.csv').
            data: Estructura de datos a exportar.
            fieldnames: Lista con los nombres de las columnas/cabeceras.

        Raises:
            FileSaveError: Si falla la generación del archivo CSV.
        """
        file_path = self._get_file_path(filename)
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except (IOError, ValueError) as e:
            raise FileSaveError(f"Error al exportar reporte CSV {filename}: {e}")


# Instancia global lista para ser consumida por los servicios del proyecto
data_manager = DataManager()