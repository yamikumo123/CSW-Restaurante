"""
Módulo de Servicios de Aplicación (Lógica de Negocio POS Restaurante)
=====================================================================

Célula 2: Servicios y Persistencia - Integrante 4
Módulo encargado de coordinar los casos de uso principales del sistema POS:
gestión de estados de mesas, adición de consumos, aplicación de reglas fiscales
(IGV) y procesamiento financiero de liquidaciones y comprobantes.
"""

from typing import Dict, List, Any, Optional
from domain.exceptions import *  # Importa las excepciones personalizadas del dominio


class AppService:
    """
    Coordinador de Lógica de Negocio y Casos de Uso del POS.

    Actúa como capa intermedia (Application Layer) entre los controladores
    de interfaz de usuario (UI) y la capa de persistencia de datos (DataManager).
    """

    # Constantes del dominio
    TASA_IGV: float = 0.18
    ESTADO_OCUPADA: str = "OCUPADA"
    ESTADO_DISPONIBLE: str = "DISPONIBLE"
    ESTADO_PAGADO: str = "PAGADO"

    def __init__(self, data_manager: Any) -> None:
        """
        Inicializa el servicio inyectando la dependencia de persistencia.

        Args:
            data_manager (Any): Instancia de la clase DataManager encargada
                                de las operaciones de I/O de almacenamiento.
        """
        self.data_manager = data_manager

    def asignar_mesa(self, numero_mesa: int, cantidad_comensales: int) -> Dict[str, Any]:
        """
        Registra la ocupación de una mesa y valida su disponibilidad previa.

        Args:
            numero_mesa (int): Número identificador de la mesa.
            cantidad_comensales (int): Número de personas asociadas a la reserva.

        Returns:
            Dict[str, Any]: Objeto estructurado de la mesa asignada.

        Raises:
            ValueError: Si el número de comensales es menor o igual a cero,
                        o si la mesa ya se encuentra ocupada.
        """
        if cantidad_comensales <= 0:
            raise ValueError("La cantidad de comensales debe ser un entero positivo.")

        mesa_existente: Optional[Dict[str, Any]] = self.data_manager.obtener_mesa_por_numero(numero_mesa)
        if mesa_existente and mesa_existente.get("estado") == self.ESTADO_OCUPADA:
            raise ValueError(f"La mesa N° {numero_mesa} ya se encuentra registrada como OCUPADA.")

        mesa: Dict[str, Any] = {
            "numero_mesa": numero_mesa,
            "comensales": cantidad_comensales,
            "estado": self.ESTADO_OCUPADA,
            "pedidos": []
        }

        self.data_manager.guardar_mesa(mesa)
        return mesa

    def agregar_pedido_a_mesa(
        self, 
        numero_mesa: int, 
        nombre_platillo: str, 
        precio: float, 
        cantidad: int = 1
    ) -> Dict[str, Any]:
        """
        Agrega un consumo o platillo a la comanda activa de una mesa ocupada.

        Args:
            numero_mesa (int): Identificador de la mesa.
            nombre_platillo (str): Descripción o nombre del ítem.
            precio (float): Precio unitario en moneda local.
            cantidad (int, optional): Unidades solicitadas. Por defecto es 1.

        Returns:
            Dict[str, Any]: Estructura actualizada de la mesa con la comanda.

        Raises:
            ValueError: Si los valores numéricos son inválidos o la mesa no está activa.
        """
        if precio <= 0 or cantidad <= 0:
            raise ValueError("El precio unitario y la cantidad deben ser valores estrictamente positivos.")

        mesa: Optional[Dict[str, Any]] = self.data_manager.obtener_mesa_por_numero(numero_mesa)
        if not mesa or mesa.get("estado") != self.ESTADO_OCUPADA:
            raise ValueError(f"No existe una cuenta activa u ocupada para la mesa N° {numero_mesa}.")

        item_pedido: Dict[str, Any] = {
            "platillo": nombre_platillo.strip(),
            "precio_unitario": round(precio, 2),
            "cantidad": cantidad,
            "subtotal_item": round(precio * cantidad, 2)
        }
        
        mesa["pedidos"].append(item_pedido)
        self.data_manager.actualizar_mesa(numero_mesa, mesa)
        return mesa

    def calcular_total_y_cobrar(
        self, 
        numero_mesa: int, 
        porcentaje_propina: float = 0.10, 
        metodo_pago: str = "EFECTIVO",
        monto_recibido: float = 0.0
    ) -> Dict[str, Any]:
        """
        Procesa la liquidación financiera, aplica impuestos (IGV 18%), valida la 
        transacción según el medio de pago y libera la mesa.

        Args:
            numero_mesa (int): Identificador de la mesa a liquidar.
            porcentaje_propina (float, optional): Ratio de propina voluntaria. Por defecto 0.10 (10%).
            metodo_pago (str, optional): Forma de pago ('EFECTIVO', 'TARJETA', 'YAPE/PLIN'). Por defecto 'EFECTIVO'.
            monto_recibido (float, optional): Importe entregado por el cliente. Requerido para efectivo.

        Returns:
            Dict[str, Any]: Comprobante/factura detallada del cobro finalizado.

        Raises:
            ValueError: Si la mesa no existe, no tiene pedidos o el pago es insuficiente.
        """
        mesa: Optional[Dict[str, Any]] = self.data_manager.obtener_mesa_por_numero(numero_mesa)
        if not mesa or mesa.get("estado") != self.ESTADO_OCUPADA:
            raise ValueError(f"No se puede facturar: La mesa N° {numero_mesa} no registra cuenta activa.")

        pedidos: List[Dict[str, Any]] = mesa.get("pedidos", [])
        if not pedidos:
            raise ValueError(f"Imposible cerrar cuenta: La mesa N° {numero_mesa} no registra consumos.")

        # Cálculos Financieros
        subtotal_consumo: float = sum(
            item.get("subtotal_item", item.get("precio", 0.0) * item.get("cantidad", 1))
            for item in pedidos
        )
        monto_igv: float = subtotal_consumo * self.TASA_IGV
        monto_propina: float = subtotal_consumo * porcentaje_propina
        total_liquidacion: float = subtotal_consumo + monto_igv + monto_propina

        # Validación del Flujo de Pago
        metodo_pago_norm: str = metodo_pago.strip().upper()
        vuelto: float = 0.0

        if metodo_pago_norm == "EFECTIVO":
            if monto_recibido < total_liquidacion:
                falta: float = round(total_liquidacion - monto_recibido, 2)
                raise ValueError(f"Pago insuficiente en efectivo. Faltan S/. {falta:.2f} para completar el cobro.")
            vuelto = round(monto_recibido - total_liquidacion, 2)

        # Generación del Comprobante
        comprobante: Dict[str, Any] = {
            "numero_mesa": numero_mesa,
            "resumen_pedidos": pedidos,
            "subtotal": round(subtotal_consumo, 2),
            "igv": round(monto_igv, 2),
            "propina": round(monto_propina, 2),
            "total_pagar": round(total_liquidacion, 2),
            "metodo_pago": metodo_pago_norm,
            "monto_recibido": round(monto_recibido, 2) if metodo_pago_norm == "EFECTIVO" else round(total_liquidacion, 2),
            "vuelto": vuelto,
            "estado": self.ESTADO_PAGADO
        }

        # Actualización de estados e historización
        mesa["estado"] = self.ESTADO_DISPONIBLE
        mesa["pedidos"] = []
        
        self.data_manager.actualizar_mesa(numero_mesa, mesa)
        self.data_manager.guardar_venta(comprobante)

        return comprobante