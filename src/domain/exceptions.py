"""
Módulo de excepciones personalizadas para el dominio del restaurante.
Define la jerarquía de errores de negocio para validaciones y operaciones.
"""

from typing import Optional, Any


class RestauranteError(Exception):
    """
    Excepción base para todos los errores de dominio del sistema de restaurante.
    """

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje: str = mensaje

    def __str__(self) -> str:
        return self.mensaje


# Alias para compatibilidad de nomenclatura
DomainError = RestauranteError
RestauranteException = RestauranteError


# ==========================================
# Excepciones de Mesas
# ==========================================

class MesaError(RestauranteError):
    """Excepción base para errores relacionados con mesas."""

    def __init__(self, mensaje: str, numero_mesa: Optional[int] = None):
        super().__init__(mensaje)
        self.numero_mesa: Optional[int] = numero_mesa


MesaException = MesaError


class MesaOcupadaError(MesaError):
    """
    Lanzada cuando se intenta asignar u operar en una mesa que ya está ocupada.
    """

    def __init__(self, mensaje: Optional[str] = None, numero_mesa: Optional[int] = None):
        if mensaje is None and numero_mesa is not None:
            mensaje = f"La mesa #{numero_mesa} ya se encuentra ocupada."
        elif mensaje is None:
            mensaje = "La mesa seleccionada ya se encuentra ocupada."
        super().__init__(mensaje, numero_mesa=numero_mesa)


MesaYaOcupadaException = MesaOcupadaError
MesaNoDisponibleException = MesaOcupadaError


class MesaNoEncontradaError(MesaError):
    """
    Lanzada cuando no existe una mesa con el número solicitado.
    """

    def __init__(self, mensaje: Optional[str] = None, numero_mesa: Optional[int] = None):
        if mensaje is None and numero_mesa is not None:
            mensaje = f"No se encontró ninguna mesa con el número {numero_mesa}."
        elif mensaje is None:
            mensaje = "La mesa solicitada no existe."
        super().__init__(mensaje, numero_mesa=numero_mesa)


MesaNoEncontradaException = MesaNoEncontradaError


# ==========================================
# Excepciones de Platillos / Menú
# ==========================================

class PlatilloError(RestauranteError):
    """Excepción base para errores relacionados con platillos."""

    def __init__(self, mensaje: str, platillo_id: Optional[int] = None):
        super().__init__(mensaje)
        self.platillo_id: Optional[int] = platillo_id


PlatilloException = PlatilloError


class PlatilloNoDisponibleError(PlatilloError):
    """
    Lanzada cuando se intenta ordenar un platillo no disponible o inexistente en la carta.
    """

    def __init__(self, mensaje: Optional[str] = None, platillo_id: Optional[int] = None):
        if mensaje is None and platillo_id is not None:
            mensaje = f"El platillo con ID {platillo_id} no está disponible o no existe en el menú."
        elif mensaje is None:
            mensaje = "El platillo solicitado no se encuentra disponible en la carta."
        super().__init__(mensaje, platillo_id=platillo_id)


PlatilloNoEncontradoException = PlatilloNoDisponibleError


class PlatilloInvalidoError(PlatilloError):
    """
    Lanzada cuando los datos de un platillo son inválidos (precio <= 0, nombre vacío, etc.).
    """

    def __init__(self, mensaje: str, platillo_id: Optional[int] = None):
        super().__init__(mensaje, platillo_id=platillo_id)


PlatilloInvalidoException = PlatilloInvalidoError


# ==========================================
# Excepciones de Pedidos
# ==========================================

class PedidoError(RestauranteError):
    """Excepción base para errores relacionados con pedidos."""

    def __init__(self, mensaje: str, pedido_id: Optional[int] = None):
        super().__init__(mensaje)
        self.pedido_id: Optional[int] = pedido_id


PedidoException = PedidoError


class PedidoInvalidoError(PedidoError):
    """
    Lanzada cuando la estructura o datos de un pedido no cumplen las reglas de negocio.
    """

    def __init__(self, mensaje: str, pedido_id: Optional[int] = None):
        super().__init__(mensaje, pedido_id=pedido_id)


PedidoInvalidoException = PedidoInvalidoError


class PedidoNoEncontradoError(PedidoError):
    """
    Lanzada cuando no se encuentra un pedido con el identificador solicitado.
    """

    def __init__(self, mensaje: Optional[str] = None, pedido_id: Optional[int] = None):
        if mensaje is None and pedido_id is not None:
            mensaje = f"No se encontró ningún pedido con el ID #{pedido_id}."
        elif mensaje is None:
            mensaje = "El pedido solicitado no fue encontrado."
        super().__init__(mensaje, pedido_id=pedido_id)


PedidoNoEncontradoException = PedidoNoEncontradoError


class EstadoPedidoInvalidoError(PedidoError):
    """
    Lanzada cuando se intenta una transición de estado no permitida para un pedido.
    """

    def __init__(
        self,
        mensaje: str,
        pedido_id: Optional[int] = None,
        estado_actual: Optional[Any] = None,
        estado_destino: Optional[Any] = None,
    ):
        super().__init__(mensaje, pedido_id=pedido_id)
        self.estado_actual = estado_actual
        self.estado_destino = estado_destino


EstadoPedidoInvalidoException = EstadoPedidoInvalidoError


# ==========================================
# Excepciones de Cuentas y Facturación
# ==========================================

class CuentaError(RestauranteError):
    """Excepción base para errores en el cálculo o cobro de cuentas."""
    pass


CuentaException = CuentaError


class CuentaInvalidaError(CuentaError):
    """
    Lanzada cuando los parámetros de facturación (propina negativa, pedido sin ítems) son inválidos.
    """
    pass


CuentaInvalidaException = CuentaInvalidaError


# ==========================================
# Excepciones de Persistencia
# ==========================================

class PersistenciaError(RestauranteError):
    """
    Lanzada cuando ocurre un error al leer o escribir datos en el medio de almacenamiento.
    """
    pass


PersistenciaException = PersistenciaError
