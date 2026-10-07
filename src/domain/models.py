from datetime import datetime


class Platillo:
    """Representa un platillo o bebida del menú."""
    def __init__(self, id_platillo: int, nombre: str, precio: float, categoria: str):
        if precio <= 0:
            raise ValueError("El precio del platillo debe ser mayor a 0.")
        if not nombre.strip():
            raise ValueError("El nombre del platillo no puede estar vacío.")

        self.__id_platillo = id_platillo
        self.__nombre = nombre.strip()
        self.__precio = float(precio)
        self.__categoria = categoria.strip()

    @property
    def id_platillo(self) -> int:
        return self.__id_platillo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def precio(self) -> float:
        return self.__precio

    @property
    def categoria(self) -> str:
        return self.__categoria

    def to_dict(self) -> dict:
        return {
            "id_platillo": self.__id_platillo,
            "nombre": self.__nombre,
            "precio": self.__precio,
            "categoria": self.__categoria,
        }


class Mesa:
    """Representa una mesa del restaurante."""
    def __init__(self, numero: int, capacidad: int):
        if numero <= 0:
            raise ValueError("El número de mesa debe ser un entero positivo.")
        if capacidad <= 0:
            raise ValueError("La capacidad de la mesa debe ser mayor a 0.")

        self.__numero = numero
        self.__capacidad = capacidad
        self.__ocupada = False

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @property
    def ocupada(self) -> bool:
        return self.__ocupada

    def ocupar(self):
        if self.__ocupada:
            raise ValueError(f"La mesa {self.__numero} ya se encuentra ocupada.")
        self.__ocupada = True

    def liberar(self):
        self.__ocupada = False

    def to_dict(self) -> dict:
        return {
            "numero": self.__numero,
            "capacidad": self.__capacidad,
            "ocupada": self.__ocupada,
        }


class Pedido:
    """Gestiona el pedido de una mesa, comensales, platillos y estados."""
    ESTADOS = ["PENDIENTE", "EN_PREPARACION", "SERVIDO", "PAGADO"]

    def __init__(self, id_pedido: int, mesa: Mesa, comensales: int):
        if comensales <= 0:
            raise ValueError("El número de comensales debe ser al menos 1.")
        if comensales > mesa.capacidad:
            raise ValueError(f"El número de comensales excede la capacidad de la mesa ({mesa.capacidad}).")

        self.__id_pedido = id_pedido
        self.__mesa = mesa
        self.__comensales = comensales
        self.__platillos = []
        self.__estado = "PENDIENTE"
        self.__fecha_creacion = datetime.now()

        # Ocupa la mesa automáticamente al crear el pedido
        self.__mesa.ocupar()

    @property
    def id_pedido(self) -> int:
        return self.__id_pedido

    @property
    def mesa(self) -> Mesa:
        return self.__mesa

    @property
    def comensales(self) -> int:
        return self.__comensales

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def platillos(self) -> list:
        return list(self.__platillos)

    def agregar_platillo(self, platillo: Platillo):
        if self.__estado == "PAGADO":
            raise ValueError("No se pueden agregar platillos a un pedido que ya fue pagado.")
        self.__platillos.append(platillo)

    def cambiar_estado(self, nuevo_estado: str):
        nuevo_estado_upper = nuevo_estado.upper()
        if nuevo_estado_upper not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Estados permitidos: {self.ESTADOS}")
        self.__estado = nuevo_estado_upper

        if self.__estado == "PAGADO":
            self.__mesa.liberar()

    def calcular_total(self) -> float:
        """Cálculo de cuenta total del pedido."""
        return sum(p.precio for p in self.__platillos)

    def to_dict(self) -> dict:
        return {
            "id_pedido": self.__id_pedido,
            "numero_mesa": self.__mesa.numero,
            "comensales": self.__comensales,
            "estado": self.__estado,
            "platillos": [p.to_dict() for p in self.__platillos],
            "total": self.calcular_total(),
        }