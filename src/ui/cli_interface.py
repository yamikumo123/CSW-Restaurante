"""
Módulo de Interfaz de Línea de Comandos (CLI)
Célula 3: Interfaz (GUI/CLI)
Responsable: Captura, validación de entradas y formateo de respuestas.
"""


# ==========================================
# FUNCIONES AUXILIARES DE VALIDACIÓN
# ==========================================

def leer_texto(mensaje: str) -> str:
    """Solicita un texto asegurando que no esté vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  [Error] El campo no puede estar vacío. Intente de nuevo.")


def leer_entero(mensaje: str, minimo: int = None) -> int:
    """Solicita un número entero con validación de tipo y valor mínimo."""
    while True:
        try:
            valor = int(input(mensaje).strip())
            if minimo is not None and valor < minimo:
                print(f"  [Error] El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  [Error] Debe ingresar un número entero válido.")


def leer_flotante(mensaje: str, minimo: float = None) -> float:
    """Solicita un número decimal (flotante) con validación de tipo y valor mínimo."""
    while True:
        try:
            valor = float(input(mensaje).strip())
            if minimo is not None and valor <= minimo:
                print(f"  [Error] El monto debe ser mayor a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  [Error] Debe ingresar un número decimal válido (ejemplo: 15.50).")


# ==========================================
# FORMATO Y PRESENTACIÓN VISUAL
# ==========================================

def mostrar_encabezado(titulo: str) -> None:
    """Imprime un título formateado dentro de un marco visual."""
    ancho = 55
    print("\n" + "=" * ancho)
    print(f"{titulo.upper():^{ancho}}")
    print("=" * ancho)


def mostrar_tabla_platillos(platillos: list) -> None:
    """Muestra una lista de platillos en formato de tabla limpia."""
    if not platillos:
        print("\n  [i] No hay platillos registrados en el sistema.")
        return

    print("\n" + "-" * 55)
    print(f"{'ID':<6} | {'Platillo':<30} | {'Precio':<10}")
    print("-" * 55)
    for p in platillos:
        # Se asume que p puede ser un objeto o un diccionario
        pid = getattr(p, 'id', p.get('id', '-'))
        nombre = getattr(p, 'nombre', p.get('nombre', 'Sin nombre'))
        precio = getattr(p, 'precio', p.get('precio', 0.0))
        print(f"{str(pid):<6} | {nombre:<30} | S/. {precio:>7.2f}")
    print("-" * 55)


def mostrar_cuenta_mora(numero_mesa: int, items: list, total: float) -> None:
    """Muestra el detalle estructurado de la cuenta/boleta de una mesa."""
    mostrar_encabezado(f"RESUMEN DE CUENTA - MESA N° {numero_mesa}")
    print(f"{'Cant.':<6} | {'Descripción':<30} | {'Subtotal':<10}")
    print("-" * 55)
    for item in items:
        cant = item.get('cantidad', 1)
        desc = item.get('nombre', 'Platillo')
        subt = item.get('subtotal', 0.0)
        print(f"{cant:<6} | {desc:<30} | S/. {subt:>7.2f}")
    print("-" * 55)
    print(f"{'TOTAL A PAGAR:':<39} S/. {total:>7.2f}")
    print("=" * 55)


# ==========================================
# MENÚS Y CAPTURA DE DATOS DE CASOS DE USO
# ==========================================

def capturar_datos_platillo() -> dict:
    """Captura los datos necesarios para registrar un platillo."""
    mostrar_encabezado("REGISTRO DE NUEVO PLATILLO")
    nombre = leer_texto("Ingrese el nombre del platillo: ")
    precio = leer_flotante("Ingrese el precio del platillo (S/.): ", minimo=0.0)
    categoria = leer_texto("Ingrese la categoría (Entrada/Fondo/Bebida/Postre): ")
    
    return {
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria
    }


def capturar_datos_mesa() -> dict:
    """Captura los datos necesarios para aperturar o asignar una mesa."""
    mostrar_encabezado("GESTIÓN DE MESA Y COMENSALES")
    numero_mesa = leer_entero("Ingrese el número de mesa: ", minimo=1)
    capacidad = leer_entero("Ingrese el número de comensales: ", minimo=1)
    
    return {
        "numero_mesa": numero_mesa,
        "capacidad": capacidad
    }


def mostrar_menu_principal() -> str:
    """Despliega el menú principal e interactúa para recibir la opción elegida."""
    mostrar_encabezado("SISTEMA POS - CSW RESTAURANTE")
    print("  [1] Registrar nuevo platillo")
    print("  [2] Aperturar/Asignar mesa con comensales")
    print("  [3] Registrar pedido en mesa")
    print("  [4] Consultar menú de platillos")
    print("  [5] Calcular y generar cuenta de mesa")
    print("  [0] Salir del sistema")
    print("=" * 55)
    
    opcion = input("Seleccione una opción [0-5]: ").strip()
    return opcion