from datetime import datetime, timedelta

from src.archivos import guardar_json, leer_json
from src.clasePrestamo import clasePrestamo
from src.config import PRESTAMOS_FILE
from src.items import actualizar_disponibilidad_item, buscar_item_por_id, listar_items_disponibles
from src.usuarios import buscar_usuario_por_documento


def obtener_prestamos() -> list[dict]:
    return leer_json(PRESTAMOS_FILE)


def guardar_prestamos(prestamos: list[dict]) -> None:
    guardar_json(PRESTAMOS_FILE, prestamos)


def generar_id_prestamo() -> str:
    prestamos = obtener_prestamos()
    consecutivos = []

    for prestamo in prestamos:
        id_prestamo = prestamo.get("id_prestamo", "")
        if id_prestamo.startswith("PRE-"):
            partes = id_prestamo.split("-")
            if len(partes) == 2 and partes[1].isdigit():
                consecutivos.append(int(partes[1]))

    siguiente = 1 if not consecutivos else max(consecutivos) + 1
    return f"PRE-{siguiente:03d}"


def obtener_fecha_actual() -> datetime:
    return datetime.now()


def formatear_fecha(fecha: datetime) -> str:
    return fecha.strftime("%Y-%m-%d")


def calcular_fecha_limite(fecha_prestamo: datetime, dias_prestamo: int) -> datetime:
    return fecha_prestamo + timedelta(days=dias_prestamo)


def calcular_dias_transcurridos(fecha_prestamo_texto: str) -> int:
    fecha_prestamo = datetime.strptime(fecha_prestamo_texto, "%Y-%m-%d")
    return (obtener_fecha_actual() - fecha_prestamo).days


def buscar_prestamo_por_id(id_prestamo: str) -> dict | None:
    id_prestamo = id_prestamo.strip().upper()

    for prestamo in obtener_prestamos():
        if prestamo.get("id_prestamo") == id_prestamo:
            return prestamo

    return None


def obtener_prestamos_activos() -> list[dict]:
    return [prestamo for prestamo in obtener_prestamos() if prestamo.get("estado") == "Activo"]


def obtener_prestamos_por_documento(documento: str) -> list[dict]:
    documento = documento.strip()
    return [prestamo for prestamo in obtener_prestamos() if prestamo.get("documento_usuario") == documento]


def obtener_prestamos_activos_por_documento(documento: str) -> list[dict]:
    documento = documento.strip()
    return [
        prestamo
        for prestamo in obtener_prestamos()
        if prestamo.get("documento_usuario") == documento and prestamo.get("estado") == "Activo"
    ]


def pedir_documento_usuario_prestamo() -> str:
    while True:
        documento = input("Ingrese el documento del usuario: ").strip()
        usuario = buscar_usuario_por_documento(documento)

        if usuario is None:
            print("Error: el usuario no existe. Debe registrarlo primero.")
            continue

        return documento


def pedir_id_item_prestamo() -> str:
    while True:
        listar_items_disponibles()
        id_item = input("Ingrese el ID del ítem a prestar: ").strip().upper()
        item = buscar_item_por_id(id_item)

        if item is None:
            print("Error: el ítem no existe.")
            continue

        if item.get("disponible") is not True:
            print("Error: el ítem no está disponible para préstamo.")
            continue

        return id_item


def registrar_prestamo() -> bool:
    print("\n--- Registro de Préstamo ---")

    documento = pedir_documento_usuario_prestamo()
    usuario = buscar_usuario_por_documento(documento)
    id_item = pedir_id_item_prestamo()
    item = buscar_item_por_id(id_item)

    if usuario is None or item is None:
        print("Error: no fue posible completar el préstamo.")
        return False

    fecha_prestamo = obtener_fecha_actual()
    fecha_limite = calcular_fecha_limite(fecha_prestamo, int(usuario["tiempo_prestamo"]))

    prestamo = clasePrestamo(
        id_prestamo=generar_id_prestamo(),
        documento_usuario=usuario["documento"],
        nombre_usuario=f"{usuario['nombre']} {usuario['apellido']}",
        id_item=item["id_item"],
        nombre_item=item["nombre"],
        categoria_item=item["categoria"],
        fecha_prestamo=formatear_fecha(fecha_prestamo),
        fecha_limite=formatear_fecha(fecha_limite),
        estado="Activo",
    )

    prestamos = obtener_prestamos()
    prestamos.append(prestamo.to_dict())
    guardar_prestamos(prestamos)
    actualizar_disponibilidad_item(item["id_item"], False)

    print("Préstamo registrado correctamente.")
    print(f"ID préstamo: {prestamo.id_prestamo}")
    print(f"Fecha préstamo: {prestamo.fecha_prestamo}")
    print(f"Fecha límite: {prestamo.fecha_limite}")
    return True


def listar_prestamos() -> None:
    prestamos = obtener_prestamos()

    if not prestamos:
        print("\nNo hay préstamos registrados.")
        return

    print("\n--- Lista de Préstamos ---")
    for indice, prestamo in enumerate(prestamos, start=1):
        print(
            f"{indice}. ID: {prestamo['id_prestamo']} | "
            f"Usuario: {prestamo['nombre_usuario']} | "
            f"Documento: {prestamo['documento_usuario']} | "
            f"Ítem: {prestamo['nombre_item']} | "
            f"ID Ítem: {prestamo['id_item']} | "
            f"Fecha préstamo: {prestamo['fecha_prestamo']} | "
            f"Fecha límite: {prestamo['fecha_limite']} | "
            f"Estado: {prestamo['estado']}"
        )


def listar_prestamos_activos() -> None:
    prestamos_activos = obtener_prestamos_activos()

    if not prestamos_activos:
        print("\nNo hay préstamos activos.")
        return

    print("\n--- Préstamos Activos ---")
    for indice, prestamo in enumerate(prestamos_activos, start=1):
        dias = calcular_dias_transcurridos(prestamo["fecha_prestamo"])
        print(
            f"{indice}. ID: {prestamo['id_prestamo']} | "
            f"Usuario: {prestamo['nombre_usuario']} | "
            f"Ítem: {prestamo['nombre_item']} | "
            f"Días transcurridos: {dias} | "
            f"Estado: {prestamo['estado']}"
        )


def obtener_prestamos_con_mas_de_20_dias() -> list[dict]:
    resultado = []

    for prestamo in obtener_prestamos_activos():
        dias = calcular_dias_transcurridos(prestamo["fecha_prestamo"])
        if dias >= 20:
            copia = dict(prestamo)
            copia["dias_transcurridos"] = dias
            resultado.append(copia)

    return resultado


def obtener_prestamos_con_mas_de_30_dias() -> list[dict]:
    resultado = []

    for prestamo in obtener_prestamos_activos():
        dias = calcular_dias_transcurridos(prestamo["fecha_prestamo"])
        if dias > 30:
            copia = dict(prestamo)
            copia["dias_transcurridos"] = dias
            resultado.append(copia)

    return resultado


def mostrar_notificaciones_20_dias() -> None:
    prestamos = obtener_prestamos_con_mas_de_20_dias()

    if not prestamos:
        print("\nNo hay préstamos con 20 días o más.")
        return

    print("\n--- Notificaciones de recuperación o devolución ---")
    for prestamo in prestamos:
        print(
            f"Préstamo {prestamo['id_prestamo']} | "
            f"Usuario: {prestamo['nombre_usuario']} | "
            f"Ítem: {prestamo['nombre_item']} | "
            f"Días transcurridos: {prestamo['dias_transcurridos']}"
        )


def mostrar_prestamos_para_venta() -> None:
    prestamos = obtener_prestamos_con_mas_de_30_dias()

    if not prestamos:
        print("\nNo hay préstamos que superen 30 días.")
        return

    print("\n--- Préstamos candidatos a venta ---")
    for prestamo in prestamos:
        print(
            f"Préstamo {prestamo['id_prestamo']} | "
            f"Usuario: {prestamo['nombre_usuario']} | "
            f"Ítem: {prestamo['nombre_item']} | "
            f"Días transcurridos: {prestamo['dias_transcurridos']}"
        )