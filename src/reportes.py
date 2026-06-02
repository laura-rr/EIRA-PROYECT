from datetime import datetime

from src.archivos import exportar_csv, leer_json
from src.config import ADMINISTRADORES_FILE, CSV_DIR, PRESTAMOS_FILE, USUARIOS_FILE, VENTAS_FILE


def obtener_usuarios() -> list[dict]:
    return leer_json(USUARIOS_FILE)


def obtener_prestamos() -> list[dict]:
    return leer_json(PRESTAMOS_FILE)


def obtener_ventas() -> list[dict]:
    return leer_json(VENTAS_FILE)


def obtener_administradores() -> list[dict]:
    return leer_json(ADMINISTRADORES_FILE)


def validar_acceso_administrador(usuario: str, contrasena: str) -> bool:
    administradores = obtener_administradores()

    for admin in administradores:
        if admin.get("usuario") == usuario and admin.get("contrasena") == contrasena:
            return True

    return False


def iniciar_sesion_administrador() -> bool:
    print("\n--- Acceso Administrador ---")
    usuario = input("Ingrese el usuario administrador: ").strip()
    contrasena = input("Ingrese la contraseña: ").strip()

    if validar_acceso_administrador(usuario, contrasena):
        print("Acceso concedido.")
        return True

    print("Acceso denegado. Usuario o contraseña incorrectos.")
    return False


def total_prestamos_registrados() -> int:
    return len(obtener_prestamos())


def total_items_devueltos() -> int:
    return sum(1 for prestamo in obtener_prestamos() if prestamo.get("estado") == "Devuelto")


def total_ventas_realizadas() -> int:
    return len(obtener_ventas())


def total_pago_realizado() -> float:
    return sum(float(venta.get("total", 0)) for venta in obtener_ventas())


def contar_prestamos_por_usuario() -> dict[str, int]:
    conteo: dict[str, int] = {}

    for usuario in obtener_usuarios():
        documento = usuario["documento"]
        conteo[documento] = 0

    for prestamo in obtener_prestamos():
        documento = prestamo.get("documento_usuario", "")
        conteo[documento] = conteo.get(documento, 0) + 1

    return conteo


def buscar_datos_usuario(documento: str) -> dict | None:
    for usuario in obtener_usuarios():
        if usuario.get("documento") == documento:
            return usuario
    return None


def usuario_con_mayor_cantidad_prestamos() -> tuple[dict | None, int]:
    conteo = contar_prestamos_por_usuario()

    if not conteo:
        return None, 0

    documento = max(conteo, key=conteo.get)
    usuario = buscar_datos_usuario(documento)
    return usuario, conteo[documento]


def usuario_con_menor_cantidad_prestamos() -> tuple[dict | None, int]:
    conteo = contar_prestamos_por_usuario()

    if not conteo:
        return None, 0

    documento = min(conteo, key=conteo.get)
    usuario = buscar_datos_usuario(documento)
    return usuario, conteo[documento]


def calcular_dias_transcurridos(fecha_prestamo_texto: str) -> int:
    fecha_prestamo = datetime.strptime(fecha_prestamo_texto, "%Y-%m-%d")
    return (datetime.now() - fecha_prestamo).days


def construir_estado_general_prestamos() -> list[dict]:
    filas = []

    for prestamo in obtener_prestamos():
        dias_transcurridos = calcular_dias_transcurridos(prestamo["fecha_prestamo"])
        filas.append(
            {
                "id_prestamo": prestamo["id_prestamo"],
                "documento_usuario": prestamo["documento_usuario"],
                "nombre_usuario": prestamo["nombre_usuario"],
                "id_item": prestamo["id_item"],
                "nombre_item": prestamo["nombre_item"],
                "categoria_item": prestamo["categoria_item"],
                "fecha_prestamo": prestamo["fecha_prestamo"],
                "fecha_limite": prestamo["fecha_limite"],
                "estado": prestamo["estado"],
                "dias_transcurridos": dias_transcurridos,
            }
        )

    filas.sort(key=lambda fila: fila["dias_transcurridos"], reverse=True)
    return filas


def mostrar_estado_general_prestamos() -> None:
    filas = construir_estado_general_prestamos()

    if not filas:
        print("\nNo hay préstamos registrados.")
        return

    print("\n--- Estado general de préstamos ordenado por días ---")
    for indice, fila in enumerate(filas, start=1):
        print(
            f"{indice}. ID préstamo: {fila['id_prestamo']} | "
            f"Usuario: {fila['nombre_usuario']} | "
            f"Ítem: {fila['nombre_item']} | "
            f"Fecha préstamo: {fila['fecha_prestamo']} | "
            f"Fecha límite: {fila['fecha_limite']} | "
            f"Estado: {fila['estado']} | "
            f"Días: {fila['dias_transcurridos']}"
        )


def mostrar_lista_usuarios() -> None:
    usuarios = obtener_usuarios()

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    print("\n--- Lista de usuarios ---")
    for indice, usuario in enumerate(usuarios, start=1):
        print(
            f"{indice}. {usuario['nombre']} {usuario['apellido']} | "
            f"Documento: {usuario['documento']} | "
            f"Correo: {usuario['correo']} | "
            f"Tiempo préstamo: {usuario['tiempo_prestamo']} días"
        )


def mostrar_resumen_administrador() -> None:
    print("\n--- Reporte de Administrador ---")
    print(f"Total de préstamos registrados: {total_prestamos_registrados()}")
    print(f"Total de ítems devueltos: {total_items_devueltos()}")
    print(f"Total de ventas realizadas: {total_ventas_realizadas()}")
    print(f"Total pago realizado: ${total_pago_realizado():.2f}")

    usuario_mayor, total_mayor = usuario_con_mayor_cantidad_prestamos()
    if usuario_mayor is not None:
        print(
            "Usuario con mayor cantidad de préstamos: "
            f"{usuario_mayor['nombre']} {usuario_mayor['apellido']} "
            f"({total_mayor})"
        )
    else:
        print("Usuario con mayor cantidad de préstamos: No disponible")

    usuario_menor, total_menor = usuario_con_menor_cantidad_prestamos()
    if usuario_menor is not None:
        print(
            "Usuario con menor cantidad de préstamos: "
            f"{usuario_menor['nombre']} {usuario_menor['apellido']} "
            f"({total_menor})"
        )
    else:
        print("Usuario con menor cantidad de préstamos: No disponible")


def exportar_estado_general_prestamos_csv() -> bool:
    filas = construir_estado_general_prestamos()
    if not filas:
        print("No hay datos para exportar.")
        return False

    ruta = CSV_DIR / "estado_general_prestamos.csv"
    exito = exportar_csv(ruta, filas)

    if exito:
        print(f"Reporte exportado correctamente en: {ruta}")
        return True

    print("No fue posible exportar el reporte.")
    return False


def menu_administrador() -> None:
    if not iniciar_sesion_administrador():
        return

    while True:
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Ver resumen general")
        print("2. Ver lista de usuarios")
        print("3. Ver estado general de préstamos")
        print("4. Exportar estado general a CSV")
        print("5. Salir del módulo administrador")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_resumen_administrador()
        elif opcion == "2":
            mostrar_lista_usuarios()
        elif opcion == "3":
            mostrar_estado_general_prestamos()
        elif opcion == "4":
            exportar_estado_general_prestamos_csv()
        elif opcion == "5":
            print("Saliendo del módulo administrador.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")