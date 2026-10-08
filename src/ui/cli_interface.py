import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class RestauranteApp(tk.Tk):
    """
    Interfaz gráfica principal del Sistema POS y Gestión de Pedidos.

    Responsabilidades:
    - Mostrar la interfaz gráfica.
    - Permitir navegación entre módulos.
    - Capturar datos ingresados por el usuario.
    - Preparar la interfaz para conectarse con servicios y validaciones.

    La lógica de negocio y persistencia pertenecen a src/services/.
    Las entidades y reglas de dominio pertenecen a src/domain/.
    """

    COLOR_FONDO = "#F7F5FF"
    COLOR_MENU = "#211A35"
    COLOR_MENU_HOVER = "#35294F"
    COLOR_PRINCIPAL = "#8B5CF6"
    COLOR_PRINCIPAL_OSCURO = "#7C3AED"
    COLOR_TEXTO = "#241F31"
    COLOR_TEXTO_SECUNDARIO = "#6B7280"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_BORDE = "#E5E7EB"
    COLOR_EXITO = "#16A34A"

    def __init__(
        self,
        on_mesa_capturada: Optional[Callable] = None,
        on_plato_capturado: Optional[Callable] = None,
        on_pedido_capturado: Optional[Callable] = None,
        on_cliente_capturado: Optional[Callable] = None,
    ):
        super().__init__()

        self.on_mesa_capturada = on_mesa_capturada
        self.on_plato_capturado = on_plato_capturado
        self.on_pedido_capturado = on_pedido_capturado
        self.on_cliente_capturado = on_cliente_capturado

        self.title("CSW Restaurante | Sistema POS y Gestión de Pedidos")
        self.geometry("1250x750")
        self.minsize(1050, 650)
        self.configure(bg=self.COLOR_FONDO)

        self._configurar_estilos()
        self._crear_estructura()

        self.mostrar_inicio()

    # =========================================================
    # CONFIGURACIÓN DE ESTILOS
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
            foreground=self.COLOR_TEXTO_SECUNDARIO
        )

        estilo.configure(
            "Seccion.TLabel",
            font=("Segoe UI", 15, "bold"),
            background=self.COLOR_BLANCO,
            foreground=self.COLOR_TEXTO
        )

        estilo.configure(
            "Campo.TLabel",
            font=("Segoe UI", 10),
            background=self.COLOR_BLANCO,
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
            padding=6
        )

        estilo.configure(
            "Accion.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 10)
        )

        estilo.map(
            "Accion.TButton",
            background=[
                ("active", self.COLOR_PRINCIPAL_OSCURO)
            ]
        )

    # =========================================================
    # ESTRUCTURA PRINCIPAL
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

        encabezado = tk.Frame(
            self.menu_lateral,
            bg=self.COLOR_MENU
        )

        encabezado.pack(
            fill="x",
            padx=22,
            pady=(28, 28)
        )

        tk.Label(
            encabezado,
            text="CSW",
            font=("Segoe UI", 23, "bold"),
            fg=self.COLOR_PRINCIPAL,
            bg=self.COLOR_MENU
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text="Restaurante",
            font=("Segoe UI", 15, "bold"),
            fg="white",
            bg=self.COLOR_MENU
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text="Sistema POS y Gestión",
            font=("Segoe UI", 9),
            fg="#B8B0C8",
            bg=self.COLOR_MENU
        ).pack(anchor="w", pady=(4, 0))

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
            self.mostrar_platos
        )

        self._crear_boton_menu(
            "▤   Pedidos",
            self.mostrar_pedidos
        )

        self._crear_boton_menu(
            "♙   Comensales",
            self.mostrar_clientes
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
            pady=22
        )

        tk.Label(
            pie,
            text="Construcción de Software",
            font=("Segoe UI", 8),
            fg="#938AA5",
            bg=self.COLOR_MENU
        ).pack(anchor="w")

        tk.Label(
            pie,
            text="Versión 1.0",
            font=("Segoe UI", 8),
            fg="#938AA5",
            bg=self.COLOR_MENU
        ).pack(anchor="w", pady=(3, 0))

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

        self.area_principal.columnconfigure(0, weight=1)
        self.area_principal.rowconfigure(1, weight=1)

        barra_superior = tk.Frame(
            self.area_principal,
            bg="white",
            height=65
        )

        barra_superior.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        barra_superior.grid_propagate(False)

        tk.Label(
            barra_superior,
            text="Sistema POS y Gestión de Pedidos",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            barra_superior,
            text="● Sistema activo",
            font=("Segoe UI", 9),
            bg="white",
            fg=self.COLOR_EXITO
        ).pack(
            side="right",
            padx=30
        )

        self.contenido = tk.Frame(
            self.area_principal,
            bg=self.COLOR_FONDO
        )

        self.contenido.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=25
        )

    # =========================================================
    # UTILIDADES
    # =========================================================

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

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
            pady=(2, 20)
        )

    def crear_tarjeta(self, padre, titulo):
        tarjeta = tk.Frame(
            padre,
            bg=self.COLOR_BLANCO,
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
            pady=(20, 15)
        )

        return tarjeta

    def crear_boton_principal(self, padre, texto, comando):
        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=self.COLOR_PRINCIPAL,
            fg="white",
            activebackground=self.COLOR_PRINCIPAL_OSCURO,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=9
        )

    # =========================================================
    # INICIO
    # =========================================================

    def mostrar_inicio(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Panel principal",
            "Administre las principales operaciones del restaurante."
        )

        panel = tk.Frame(
            self.contenido,
            bg=self.COLOR_FONDO
        )

        panel.pack(fill="both", expand=True)

        tarjetas = [
            (
                "Mesas",
                "Gestión y registro de mesas.",
                self.mostrar_mesas
            ),
            (
                "Platillos",
                "Registro de productos del menú.",
                self.mostrar_platos
            ),
            (
                "Pedidos",
                "Creación y consulta de pedidos.",
                self.mostrar_pedidos
            ),
            (
                "Comensales",
                "Registro de información de clientes.",
                self.mostrar_clientes
            ),
            (
                "Preparación",
                "Seguimiento del estado de los pedidos.",
                self.mostrar_preparacion
            ),
            (
                "Cuentas",
                "Consulta y cálculo visual del consumo.",
                self.mostrar_cuentas
            )
        ]

        for indice, datos in enumerate(tarjetas):
            titulo, descripcion, comando = datos

            tarjeta = tk.Frame(
                panel,
                bg="white",
                highlightbackground=self.COLOR_BORDE,
                highlightthickness=1
            )

            fila = indice // 2
            columna = indice % 2

            tarjeta.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=8,
                pady=8
            )

            panel.columnconfigure(columna, weight=1)
            panel.rowconfigure(fila, weight=1)

            tk.Label(
                tarjeta,
                text=titulo,
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg=self.COLOR_TEXTO
            ).pack(
                anchor="w",
                padx=24,
                pady=(25, 7)
            )

            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Segoe UI", 10),
                bg="white",
                fg=self.COLOR_TEXTO_SECUNDARIO
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
                pady=25
            )

    # =========================================================
    # MESAS
    # =========================================================

    def mostrar_mesas(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de mesas",
            "Registre la información básica de las mesas del restaurante."
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Nueva mesa"
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
            pady=7
        )

        self.mesa_numero = ttk.Entry(formulario)

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
            pady=7
        )

        self.mesa_capacidad = ttk.Entry(formulario)

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
            pady=(18, 7)
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

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.crear_boton_principal(
            formulario,
            "Registrar mesa",
            self.capturar_mesa
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(25, 0)
        )

    def capturar_mesa(self):
        datos = {
            "numero": self.mesa_numero.get(),
            "capacidad": self.mesa_capacidad.get(),
            "ubicacion": self.mesa_ubicacion.get()
        }

        if self.on_mesa_capturada:
            self.on_mesa_capturada(datos)

    # =========================================================
    # PLATILLOS
    # =========================================================

    def mostrar_platos(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de platillos",
            "Capture la información de los productos disponibles en el menú."
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Nuevo platillo"
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
            pady=7
        )

        self.plato_nombre = ttk.Entry(formulario)

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
            pady=7
        )

        self.plato_precio = ttk.Entry(formulario)

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
            pady=(18, 7)
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
            text="Estado",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(18, 7)
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

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.crear_boton_principal(
            formulario,
            "Registrar platillo",
            self.capturar_plato
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(25, 0)
        )

    def capturar_plato(self):
        datos = {
            "nombre": self.plato_nombre.get(),
            "precio": self.plato_precio.get(),
            "categoria": self.plato_categoria.get(),
            "estado": self.plato_estado.get()
        }

        if self.on_plato_capturado:
            self.on_plato_capturado(datos)

    # =========================================================
    # PEDIDOS
    # =========================================================

    def mostrar_pedidos(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de pedidos",
            "Capture los datos necesarios para registrar un pedido."
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
            text="Número de mesa",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=7
        )

        self.pedido_mesa = ttk.Entry(formulario)

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
            sticky="w",
            pady=7
        )

        self.pedido_cliente = ttk.Entry(formulario)

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
            pady=(18, 7)
        )

        self.pedido_plato = ttk.Entry(formulario)

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
            pady=(18, 7)
        )

        self.pedido_cantidad = ttk.Entry(formulario)

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
            pady=(18, 7)
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

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.crear_boton_principal(
            formulario,
            "Crear pedido",
            self.capturar_pedido
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(25, 0)
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

        if self.on_pedido_capturado:
            self.on_pedido_capturado(datos)

    # =========================================================
    # COMENSALES
    # =========================================================

    def mostrar_clientes(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Gestión de comensales",
            "Capture los datos básicos del cliente."
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Nuevo comensal"
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
            sticky="w",
            pady=7
        )

        self.cliente_nombre = ttk.Entry(formulario)

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
            sticky="w",
            pady=7
        )

        self.cliente_documento = ttk.Entry(formulario)

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
            pady=(18, 7)
        )

        self.cliente_telefono = ttk.Entry(formulario)

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
            pady=(18, 7)
        )

        self.cliente_correo = ttk.Entry(formulario)

        self.cliente_correo.grid(
            row=3,
            column=1,
            sticky="ew"
        )

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.crear_boton_principal(
            formulario,
            "Registrar comensal",
            self.capturar_cliente
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(25, 0)
        )

    def capturar_cliente(self):
        datos = {
            "nombre": self.cliente_nombre.get(),
            "documento": self.cliente_documento.get(),
            "telefono": self.cliente_telefono.get(),
            "correo": self.cliente_correo.get()
        }

        if self.on_cliente_capturado:
            self.on_cliente_capturado(datos)

    # =========================================================
    # PREPARACIÓN
    # =========================================================

    def mostrar_preparacion(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Estado de preparación",
            "Visualice el avance de los pedidos enviados a cocina."
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
            pady=(0, 25)
        )

        encabezados = [
            "Pedido",
            "Mesa",
            "Platillo",
            "Estado"
        ]

        for columna, texto in enumerate(encabezados):
            tk.Label(
                contenedor,
                text=texto,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#374151"
            ).grid(
                row=0,
                column=columna,
                sticky="w",
                padx=10,
                pady=10
            )

        pedidos_demo = [
            ("#001", "Mesa 03", "Lomo saltado", "Pendiente"),
            ("#002", "Mesa 07", "Ají de gallina", "En preparación"),
            ("#003", "Mesa 02", "Arroz con pollo", "Listo")
        ]

        for fila, pedido in enumerate(pedidos_demo, start=1):
            for columna, valor in enumerate(pedido):
                color = "#4B5563"

                if columna == 3:
                    if valor == "Listo":
                        color = "#16A34A"
                    elif valor == "En preparación":
                        color = self.COLOR_PRINCIPAL_OSCURO
                    else:
                        color = "#D97706"

                tk.Label(
                    contenedor,
                    text=valor,
                    font=("Segoe UI", 10),
                    bg="white",
                    fg=color
                ).grid(
                    row=fila,
                    column=columna,
                    sticky="w",
                    padx=10,
                    pady=12
                )

        for columna in range(4):
            contenedor.columnconfigure(
                columna,
                weight=1
            )

    # =========================================================
    # CUENTAS
    # =========================================================

    def mostrar_cuentas(self):
        self.limpiar_contenido()

        self.crear_titulo(
            "Cálculo de cuentas",
            "Seleccione una mesa para consultar el resumen del consumo."
        )

        tarjeta = self.crear_tarjeta(
            self.contenido,
            "Cuenta de mesa"
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
            pady=7
        )

        self.cuenta_mesa = ttk.Entry(formulario)

        self.cuenta_mesa.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 15)
        )

        resumen = tk.Frame(
            formulario,
            bg=self.COLOR_FONDO
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
            font=("Segoe UI", 10),
            bg=self.COLOR_FONDO,
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=8
        )

        self.lbl_subtotal = tk.Label(
            resumen,
            text="S/ 0.00",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_PRINCIPAL_OSCURO
        )

        self.lbl_subtotal.grid(
            row=0,
            column=1,
            sticky="e",
            padx=15
        )

        tk.Label(
            resumen,
            text="Servicio",
            font=("Segoe UI", 10),
            bg=self.COLOR_FONDO,
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=15,
            pady=8
        )

        self.lbl_servicio = tk.Label(
            resumen,
            text="S/ 0.00",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_PRINCIPAL_OSCURO
        )

        self.lbl_servicio.grid(
            row=1,
            column=1,
            sticky="e",
            padx=15
        )

        tk.Label(
            resumen,
            text="Total",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=15,
            pady=10
        )

        self.lbl_total = tk.Label(
            resumen,
            text="S/ 0.00",
            font=("Segoe UI", 14, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_PRINCIPAL_OSCURO
        )

        self.lbl_total.grid(
            row=2,
            column=1,
            sticky="e",
            padx=15
        )

        resumen.columnconfigure(0, weight=1)
        resumen.columnconfigure(1, weight=1)

        self.crear_boton_principal(
            formulario,
            "Consultar cuenta",
            lambda: None
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(10, 0)
        )

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)


def iniciar_interfaz():
    app = RestauranteApp()
    app.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()