import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class RestauranteApp(tk.Tk):
    """
    Interfaz gráfica del Sistema POS y Gestión de Pedidos.

    Célula 3 - Interfaz (GUI/CLI)

    Responsabilidades:
    - Presentar la interfaz gráfica.
    - Navegar entre los módulos del restaurante.
    - Capturar información ingresada por el usuario.
    - Preparar datos para su posterior envío a la capa services.

    La validación, reglas de negocio y persistencia pertenecen
    a las capas correspondientes del proyecto.
    """

    VERSION = "GUI v2.0"

    COLOR_MENU = "#211A35"
    COLOR_MENU_HOVER = "#34264F"
    COLOR_FONDO = "#F7F4FF"
    COLOR_TARJETA = "#FFFFFF"

    COLOR_PRINCIPAL = "#8B5CF6"
    COLOR_PRINCIPAL_HOVER = "#7C3AED"
    COLOR_PRINCIPAL_SUAVE = "#EDE9FE"

    COLOR_TEXTO = "#231F2D"
    COLOR_SECUNDARIO = "#6B7280"
    COLOR_BORDE = "#E4E0EB"

    COLOR_EXITO = "#16A34A"
    COLOR_ADVERTENCIA = "#D97706"
    COLOR_ERROR = "#DC2626"

    def __init__(
        self,
        on_mesa_capturada: Optional[Callable] = None,
        on_plato_capturado: Optional[Callable] = None,
        on_pedido_capturado: Optional[Callable] = None,
        on_cliente_capturado: Optional[Callable] = None,
    ):
        super().__init__()

        # Callbacks preparados para integración posterior con services.
        self.on_mesa_capturada = on_mesa_capturada
        self.on_plato_capturado = on_plato_capturado
        self.on_pedido_capturado = on_pedido_capturado
        self.on_cliente_capturado = on_cliente_capturado

        self.title(
            f"CSW Restaurante | Sistema POS y Gestión de Pedidos | {self.VERSION}"
        )

        self.geometry("1280x760")
        self.minsize(1050, 650)
        self.configure(bg=self.COLOR_FONDO)

        self._configurar_estilos()
        self._crear_estructura()

        self.mostrar_inicio()

    # =========================================================
    # ESTILOS
    # =========================================================

    def _configurar_estilos(self):
        estilo = ttk.Style(self)

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 22, "bold"),
            background=self.COLOR_FONDO,
            foreground=self.COLOR_TEXTO
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Segoe UI", 10),
            background=self.COLOR_FONDO,
            foreground=self.COLOR_SECUNDARIO
        )

        estilo.configure(
            "Seccion.TLabel",
            font=("Segoe UI", 15, "bold"),
            background=self.COLOR_TARJETA,
            foreground=self.COLOR_TEXTO
        )

        estilo.configure(
            "Campo.TLabel",
            font=("Segoe UI", 10),
            background=self.COLOR_TARJETA,
            foreground="#374151"
        )

        estilo.configure(
            "TEntry",
            font=("Segoe UI", 10),
            padding=8
        )

        estilo.configure(
            "TCombobox",
            font=("Segoe UI", 10),
            padding=7
        )

        estilo.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=32,
            background="white",
            fieldbackground="white"
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    # =========================================================
    # ESTRUCTURA GENERAL
    # =========================================================

    def _crear_estructura(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._crear_menu_lateral()
        self._crear_area_principal()

    def _crear_menu_lateral(self):
        self.menu_lateral = tk.Frame(
            self,
            bg=self.COLOR_MENU,
            width=245
        )

        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.menu_lateral.grid_propagate(False)

        cabecera = tk.Frame(
            self.menu_lateral,
            bg=self.COLOR_MENU
        )

        cabecera.pack(
            fill="x",
            padx=22,
            pady=(28, 24)
        )

        tk.Label(
            cabecera,
            text="CSW",
            font=("Segoe UI", 24, "bold"),
            fg=self.COLOR_PRINCIPAL,
            bg=self.COLOR_MENU
        ).pack(anchor="w")

        tk.Label(
            cabecera,
            text="Restaurante",
            font=("Segoe UI", 15, "bold"),
            fg="white",
            bg=self.COLOR_MENU
        ).pack(anchor="w")

        tk.Label(
            cabecera,
            text="Sistema POS y Gestión",
            font=("Segoe UI", 9),
            fg="#BEB5CF",
            bg=self.COLOR_MENU
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        self._crear_boton_menu(
            "⌂   Inicio",
            self.mostrar_inicio
        )

        self._crear_boton_menu(
            "▦   Mesas",
            self.mostrar_mesas
        )

        self._crear_boton_menu(
            "☕   Platillos",
            self.mostrar_platillos
        )

        self._crear_boton_menu(
            "▤   Pedidos",
            self.mostrar_pedidos
        )

        self._crear_boton_menu(
            "♙   Comensales",
            self.mostrar_comensales
        )

        self._crear_boton_menu(
            "◷   Preparación",
            self.mostrar_preparacion
        )

        self._crear_boton_menu(
            "$   Cuentas",
            self.mostrar_cuentas
        )

        pie = tk.Frame(
            self.menu_lateral,
            bg=self.COLOR_MENU
        )

        pie.pack(
            side="bottom",
            fill="x",
            padx=22,
            pady=20
        )

        tk.Label(
            pie,
            text="Construcción de Software",
            font=("Segoe UI", 8),
            fg="#9187A7",
            bg=self.COLOR_MENU
        ).pack(anchor="w")

        tk.Label(
            pie,
            text=self.VERSION,
            font=("Segoe UI", 8, "bold"),
            fg=self.COLOR_PRINCIPAL,
            bg=self.COLOR_MENU
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

    def _crear_boton_menu(self, texto, comando):
        boton = tk.Button(
            self.menu_lateral,
            text=texto,
            command=comando,
            font=("Segoe UI", 10),
            fg="#F3F4F6",
            bg=self.COLOR_MENU,
            activebackground=self.COLOR_MENU_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            padx=20,
            pady=12
        )

        boton.pack(
            fill="x",
            padx=10,
            pady=2
        )

    def _crear_area_principal(self):
        self.area_principal = tk.Frame(
            self,
            bg=self.COLOR_FONDO
        )

        self.area_principal.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.area_principal.columnconfigure(
            0,
            weight=1
        )

        self.area_principal.rowconfigure(
            1,
            weight=1
        )

        # Barra superior
        barra = tk.Frame(
            self.area_principal,
            bg="white",
            height=66
        )

        barra.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        barra.grid_propagate(False)

        tk.Label(
            barra,
            text="Sistema POS y Gestión de Pedidos",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.COLOR_TEXTO
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            barra,
            text=f"● Sistema activo   •   {self.VERSION}",
            font=("Segoe UI", 9),
            bg="white",
            fg=self.COLOR_EXITO
        ).pack(
            side="right",
            padx=30
        )

        # Área dinámica
        self.contenido = tk.Frame(
            self.area_principal,
            bg=self.COLOR_FONDO
        )

        self.contenido.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=22
        )

        # Barra inferior
        self.barra_estado = tk.Label(
            self.area_principal,
            text="Listo | Interfaz gráfica cargada correctamente",
            font=("Segoe UI", 9),
            bg="#EEE9F8",
            fg=self.COLOR_SECUNDARIO,
            anchor="w",
            padx=15,
            pady=6
        )

        self.barra_estado.grid(
            row=2,
            column=0,
            sticky="ew"
        )

    # =========================================================
    # FUNCIONES AUXILIARES
    # =========================================================

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_estado(self, mensaje):
        self.barra_estado.config(
            text=f"{self.VERSION} | {mensaje}"
        )

    def crear_titulo(self, titulo, descripcion):
        ttk.Label(
            self.contenido,
            text=titulo,
            style="Titulo.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            self.contenido,
            text=descripcion,
            style="Subtitulo.TLabel"
        ).pack(
            anchor="w",
            pady=(3, 20)
        )

    def crear_tarjeta(self, padre, titulo):
        tarjeta = tk.Frame(
            padre,
            bg=self.COLOR_TARJETA,
            highlightbackground=self.COLOR_BORDE,
            highlightthickness=1
        )

        ttk.Label(
            tarjeta,
            text=titulo,
            style="Seccion.TLabel"
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 14)
        )

        return tarjeta

    def crear_boton_principal(
        self,
        padre,
        texto,
        comando
    ):
        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=self.COLOR_PRINCIPAL,
            fg="white",
            activebackground=self.COLOR_PRINCIPAL_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=18,
            pady=9
        )

    # =========================================================
    # PANEL PRINCIPAL
    # =========================================================

    def mostrar_inicio(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Panel principal",
            "Administre las principales operaciones del restaurante."
        )

        self.actualizar_estado(
            "Panel principal cargado"
        )

        panel = tk.Frame(
            self.contenido,
            bg=self.COLOR_FONDO
        )

        panel.pack(
            fill="both",
            expand=True
        )

        modulos = [
            (
                "Mesas",
                "Registro, capacidad y ubicación de mesas.",
                self.mostrar_mesas
            ),
            (
                "Platillos",
                "Productos disponibles en el menú.",
                self.mostrar_platillos
            ),
            (
                "Pedidos",
                "Creación y captura de nuevos pedidos.",
                self.mostrar_pedidos
            ),
            (
                "Comensales",
                "Información de los clientes.",
                self.mostrar_comensales
            ),
            (
                "Preparación",
                "Seguimiento visual de pedidos en cocina.",
                self.mostrar_preparacion
            ),
            (
                "Cuentas",
                "Consulta del consumo por mesa.",
                self.mostrar_cuentas
            ),
        ]

        for indice, modulo in enumerate(modulos):
            titulo, descripcion, comando = modulo

            fila = indice // 2
            columna = indice % 2

            tarjeta = tk.Frame(
                panel,
                bg="white",
                highlightbackground=self.COLOR_BORDE,
                highlightthickness=1
            )

            tarjeta.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=8,
                pady=8
            )

            panel.columnconfigure(
                columna,
                weight=1
            )

            panel.rowconfigure(
                fila,
                weight=1
            )

            tk.Label(
                tarjeta,
                text=titulo,
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg=self.COLOR_TEXTO
            ).pack(
                anchor="w",
                padx=24,
                pady=(24, 6)
            )

            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Segoe UI", 10),
                bg="white",
                fg=self.COLOR_SECUNDARIO
            ).pack(
                anchor="w",
                padx=24
            )

            self.crear_boton_principal(
                tarjeta,
                "Abrir módulo",
                comando
            ).pack(
                anchor="w",
                padx=24,
                pady=22
            )

    # =========================================================
    # MESAS
    # =========================================================

    def mostrar_mesas(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de mesas",
            "Capture la información de las mesas del restaurante."
        )

        self.actualizar_estado(
            "Módulo Mesas"
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Registrar nueva mesa"
        )

        tarjeta.pack(fill="x")

        formulario = tk.Frame(
            tarjeta,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=22,
            pady=(0, 25)
        )

        ttk.Label(
            formulario,
            text="Número de mesa",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=6
        )

        self.mesa_numero = ttk.Entry(
            formulario
        )

        self.mesa_numero.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Capacidad",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            pady=6
        )

        self.mesa_capacidad = ttk.Entry(
            formulario
        )

        self.mesa_capacidad.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        ttk.Label(
            formulario,
            text="Ubicación",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(18, 6)
        )

        self.mesa_ubicacion = ttk.Combobox(
            formulario,
            values=[
                "Salón principal",
                "Terraza",
                "Segundo piso",
                "Zona privada"
            ],
            state="readonly"
        )

        self.mesa_ubicacion.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        formulario.columnconfigure(
            0,
            weight=1
        )

        formulario.columnconfigure(
            1,
            weight=1
        )

        self.crear_boton_principal(
            formulario,
            "Capturar mesa",
            self.capturar_mesa
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(24, 0)
        )

    def capturar_mesa(self):
        datos = {
            "numero": self.mesa_numero.get(),
            "capacidad": self.mesa_capacidad.get(),
            "ubicacion": self.mesa_ubicacion.get()
        }

        self.actualizar_estado(
            "Datos de mesa capturados"
        )

        if self.on_mesa_capturada:
            self.on_mesa_capturada(datos)

    # =========================================================
    # PLATILLOS
    # =========================================================

    def mostrar_platillos(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de platillos",
            "Capture los productos disponibles en el menú."
        )

        self.actualizar_estado(
            "Módulo Platillos"
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Registrar platillo"
        )

        tarjeta.pack(fill="x")

        formulario = tk.Frame(
            tarjeta,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=22,
            pady=(0, 25)
        )

        ttk.Label(
            formulario,
            text="Nombre del platillo",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=6
        )

        self.plato_nombre = ttk.Entry(
            formulario
        )

        self.plato_nombre.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Precio",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            pady=6
        )

        self.plato_precio = ttk.Entry(
            formulario
        )

        self.plato_precio.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        ttk.Label(
            formulario,
            text="Categoría",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(18, 6)
        )

        self.plato_categoria = ttk.Combobox(
            formulario,
            values=[
                "Entrada",
                "Plato principal",
                "Bebida",
                "Postre"
            ],
            state="readonly"
        )

        self.plato_categoria.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Disponibilidad",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(18, 6)
        )

        self.plato_estado = ttk.Combobox(
            formulario,
            values=[
                "Disponible",
                "No disponible"
            ],
            state="readonly"
        )

        self.plato_estado.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        formulario.columnconfigure(
            0,
            weight=1
        )

        formulario.columnconfigure(
            1,
            weight=1
        )

        self.crear_boton_principal(
            formulario,
            "Capturar platillo",
            self.capturar_platillo
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(24, 0)
        )

    def capturar_platillo(self):
        datos = {
            "nombre": self.plato_nombre.get(),
            "precio": self.plato_precio.get(),
            "categoria": self.plato_categoria.get(),
            "estado": self.plato_estado.get()
        }

        self.actualizar_estado(
            "Datos de platillo capturados"
        )

        if self.on_plato_capturado:
            self.on_plato_capturado(datos)

    # =========================================================
    # PEDIDOS
    # =========================================================

    def mostrar_pedidos(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de pedidos",
            "Capture los datos del pedido realizado por el comensal."
        )

        self.actualizar_estado(
            "Módulo Pedidos"
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Nuevo pedido"
        )

        tarjeta.pack(fill="x")

        formulario = tk.Frame(
            tarjeta,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=22,
            pady=(0, 25)
        )

        ttk.Label(
            formulario,
            text="Mesa",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.pedido_mesa = ttk.Entry(
            formulario
        )

        self.pedido_mesa.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Comensal",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.pedido_cliente = ttk.Entry(
            formulario
        )

        self.pedido_cliente.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        ttk.Label(
            formulario,
            text="Platillo",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(18, 6)
        )

        self.pedido_plato = ttk.Entry(
            formulario
        )

        self.pedido_plato.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Cantidad",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(18, 6)
        )

        self.pedido_cantidad = ttk.Entry(
            formulario
        )

        self.pedido_cantidad.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        ttk.Label(
            formulario,
            text="Observaciones",
            style="Campo.TLabel"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(18, 6)
        )

        self.pedido_observaciones = tk.Text(
            formulario,
            height=4,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.pedido_observaciones.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        formulario.columnconfigure(
            0,
            weight=1
        )

        formulario.columnconfigure(
            1,
            weight=1
        )

        self.crear_boton_principal(
            formulario,
            "Capturar pedido",
            self.capturar_pedido
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=(24, 0)
        )

    def capturar_pedido(self):
        datos = {
            "mesa": self.pedido_mesa.get(),
            "cliente": self.pedido_cliente.get(),
            "plato": self.pedido_plato.get(),
            "cantidad": self.pedido_cantidad.get(),
            "observaciones": self.pedido_observaciones.get(
                "1.0",
                "end-1c"
            )
        }

        self.actualizar_estado(
            "Datos del pedido capturados"
        )

        if self.on_pedido_capturado:
            self.on_pedido_capturado(datos)

    # =========================================================
    # COMENSALES
    # =========================================================

    def mostrar_comensales(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de comensales",
            "Capture los datos básicos del cliente."
        )

        self.actualizar_estado(
            "Módulo Comensales"
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Registrar comensal"
        )

        tarjeta.pack(fill="x")

        formulario = tk.Frame(
            tarjeta,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=22,
            pady=(0, 25)
        )

        ttk.Label(
            formulario,
            text="Nombre completo",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.cliente_nombre = ttk.Entry(
            formulario
        )

        self.cliente_nombre.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Documento",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.cliente_documento = ttk.Entry(
            formulario
        )

        self.cliente_documento.grid(
            row=1,
            column=1,
            sticky="ew"
        )

        ttk.Label(
            formulario,
            text="Teléfono",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(18, 6)
        )

        self.cliente_telefono = ttk.Entry(
            formulario
        )

        self.cliente_telefono.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Correo electrónico",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(18, 6)
        )

        self.cliente_correo = ttk.Entry(
            formulario
        )

        self.cliente_correo.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        formulario.columnconfigure(
            0,
            weight=1
        )

        formulario.columnconfigure(
            1,
            weight=1
        )

        self.crear_boton_principal(
            formulario,
            "Capturar comensal",
            self.capturar_comensal
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(24, 0)
        )

    def capturar_comensal(self):
        datos = {
            "nombre": self.cliente_nombre.get(),
            "documento": self.cliente_documento.get(),
            "telefono": self.cliente_telefono.get(),
            "correo": self.cliente_correo.get()
        }

        self.actualizar_estado(
            "Datos del comensal capturados"
        )

        if self.on_cliente_capturado:
            self.on_cliente_capturado(datos)

    # =========================================================
    # PREPARACIÓN
    # =========================================================

    def mostrar_preparacion(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Estado de preparación",
            "Seguimiento visual del estado de los pedidos."
        )

        self.actualizar_estado(
            "Módulo Preparación"
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Pedidos en cocina"
        )

        tarjeta.pack(
            fill="both",
            expand=True
        )

        contenedor = tk.Frame(
            tarjeta,
            bg="white"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 22)
        )

        columnas = (
            "pedido",
            "mesa",
            "platillo",
            "cantidad",
            "estado"
        )

        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=10
        )

        tabla.heading(
            "pedido",
            text="Pedido"
        )

        tabla.heading(
            "mesa",
            text="Mesa"
        )

        tabla.heading(
            "platillo",
            text="Platillo"
        )

        tabla.heading(
            "cantidad",
            text="Cantidad"
        )

        tabla.heading(
            "estado",
            text="Estado"
        )

        tabla.column(
            "pedido",
            width=90
        )

        tabla.column(
            "mesa",
            width=100
        )

        tabla.column(
            "platillo",
            width=230
        )

        tabla.column(
            "cantidad",
            width=100
        )

        tabla.column(
            "estado",
            width=150
        )

        # Datos visuales temporales.
        # Posteriormente se reemplazarán por información de services.
        pedidos_demo = [
            (
                "#001",
                "Mesa 03",
                "Lomo saltado",
                "2",
                "Pendiente"
            ),
            (
                "#002",
                "Mesa 07",
                "Ají de gallina",
                "1",
                "En preparación"
            ),
            (
                "#003",
                "Mesa 02",
                "Arroz con pollo",
                "3",
                "Listo"
            )
        ]

        for pedido in pedidos_demo:
            tabla.insert(
                "",
                "end",
                values=pedido
            )

        tabla.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CUENTAS
    # =========================================================

    def mostrar_cuentas(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Cálculo de cuentas",
            "Consulte el resumen de consumo correspondiente a una mesa."
        )

        self.actualizar_estado(
            "Módulo Cuentas"
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Resumen de cuenta"
        )

        tarjeta.pack(fill="x")

        formulario = tk.Frame(
            tarjeta,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=22,
            pady=(0, 25)
        )

        ttk.Label(
            formulario,
            text="Número de mesa",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.cuenta_mesa = ttk.Entry(
            formulario
        )

        self.cuenta_mesa.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        resumen = tk.Frame(
            formulario,
            bg=self.COLOR_PRINCIPAL_SUAVE
        )

        resumen.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(25, 15)
        )

        tk.Label(
            resumen,
            text="Subtotal",
            bg=self.COLOR_PRINCIPAL_SUAVE,
            fg=self.COLOR_TEXTO,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=8
        )

        self.lbl_subtotal = tk.Label(
            resumen,
            text="S/ 0.00",
            bg=self.COLOR_PRINCIPAL_SUAVE,
            fg=self.COLOR_PRINCIPAL_HOVER,
            font=("Segoe UI", 10, "bold")
        )

        self.lbl_subtotal.grid(
            row=0,
            column=1,
            sticky="e",
            padx=16
        )

        tk.Label(
            resumen,
            text="Servicio",
            bg=self.COLOR_PRINCIPAL_SUAVE,
            fg=self.COLOR_TEXTO,
            font=("Segoe UI", 10)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=16,
            pady=8
        )

        self.lbl_servicio = tk.Label(
            resumen,
            text="S/ 0.00",
            bg=self.COLOR_PRINCIPAL_SUAVE,
            fg=self.COLOR_PRINCIPAL_HOVER,
            font=("Segoe UI", 10, "bold")
        )

        self.lbl_servicio.grid(
            row=1,
            column=1,
            sticky="e",
            padx=16
        )

        tk.Label(
            resumen,
            text="Total",
            bg=self.COLOR_PRINCIPAL_SUAVE,
            fg=self.COLOR_TEXTO,
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=16,
            pady=10
        )

        self.lbl_total = tk.Label(
            resumen,
            text="S/ 0.00",
            bg=self.COLOR_PRINCIPAL_SUAVE,
            fg=self.COLOR_PRINCIPAL_HOVER,
            font=("Segoe UI", 14, "bold")
        )

        self.lbl_total.grid(
            row=2,
            column=1,
            sticky="e",
            padx=16
        )

        resumen.columnconfigure(
            0,
            weight=1
        )

        resumen.columnconfigure(
            1,
            weight=1
        )

        self.crear_boton_principal(
            formulario,
            "Consultar cuenta",
            self.capturar_consulta_cuenta
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(10, 0)
        )

        formulario.columnconfigure(
            0,
            weight=1
        )

        formulario.columnconfigure(
            1,
            weight=1
        )

    def capturar_consulta_cuenta(self):
        mesa = self.cuenta_mesa.get()

        self.actualizar_estado(
            f"Consulta de cuenta capturada para mesa: {mesa}"
        )


# =============================================================
# PUNTO DE ARRANQUE DE LA INTERFAZ
# =============================================================

def iniciar_interfaz():
    """
    Inicializa la interfaz gráfica principal.
    Puede ser llamada desde src/main.py.
    """

    app = RestauranteApp()
    app.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()