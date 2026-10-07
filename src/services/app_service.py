"""
Módulo de Servicios de Aplicación (Lógica POS de Restaurante)
Célula 2: Servicios y Persistencia - Integrante 4
"""

from domain.exceptions import *  # Importa las excepciones personalizadas de la Célula 1


class AppService:
    """
    Gestor de la lógica de negocio para pedidos, asignación de mesas y cobros.
    """

    def __init__(self, data_manager):
        """
        Recibe la instancia de DataManager (controlada por el Integrante 5).
        """
        self.data_manager = data_manager

    def asignar_mesa(self, numero_mesa: int, cantidad_comensales: int) -> dict:
        """
        Regla de negocio: Asigna una mesa para un número de comensales.
        """
        if cantidad_comensales <= 0:
            raise ValueError("La cantidad de comensales debe ser mayor a 0.")

        mesa = {
            "numero_mesa": numero_mesa,
            "comensales": cantidad_comensales,
            "estado": "OCUPADA",
            "pedidos": []
        }
        
        # Se guarda el estado inicial de la mesa mediante el DataManager
        self.data_manager.guardar_mesa(mesa)
        return mesa

    def agregar_pedido_a_mesa(self, numero_mesa: int, nombre_platillo: str, precio: float) -> dict:
        """
        Regla de negocio: Registra un nuevo platillo a la cuenta de una mesa.
        """
        if precio <= 0:
            raise ValueError("El precio del platillo debe ser positivo.")

        mesa = self.data_manager.obtener_mesa_por_numero(numero_mesa)
        if not mesa or mesa.get("estado") != "OCUPADA":
            raise ValueError(f"La mesa {numero_mesa} no está ocupada o no existe.")

        item = {"platillo": nombre_platillo, "precio": precio}
        mesa["pedidos"].append(item)
        
        self.data_manager.actualizar_mesa(numero_mesa, mesa)
        return mesa

    def calcular_total_y_cobrar(self, numero_mesa: int, porcentaje_propina: float = 0.10) -> dict:
        """
        Regla de negocio: Calcula subtotal, propina, total y cierra la cuenta de la mesa.
        """
        mesa = self.data_manager.obtener_mesa_por_numero(numero_mesa)
        if not mesa or mesa.get("estado") != "OCUPADA":
            raise ValueError(f"No hay una cuenta activa para la mesa {numero_mesa}.")

        pedidos = mesa.get("pedidos", [])
        if not pedidos:
            raise ValueError("No se pueden cobrar mesas sin pedidos registrados.")

        subtotal = sum(item["precio"] for item in pedidos)
        propina = subtotal * porcentaje_propina
        total = subtotal + propina

        factura = {
            "numero_mesa": numero_mesa,
            "subtotal": round(subtotal, 2),
            "propina": round(propina, 2),
            "total": round(total, 2),
            "estado": "PAGADO"
        }

        # Liberar mesa y registrar venta final
        mesa["estado"] = "DISPONIBLE"
        mesa["pedidos"] = []
        self.data_manager.actualizar_mesa(numero_mesa, mesa)
        self.data_manager.guardar_venta(factura)

        return factura