# Archivo: pf_Algoritmos/src/facturacion.py
from datetime import datetime

from src.archivos import escribir_txt, guardar_json, leer_json
from src.config import FACTURAS_DIR, IMPUESTO_CONCHUDEZ, VENTAS_FILE, CERTIFICADOS_DIR
from src.items import actualizar_disponibilidad_item, buscar_item_por_id
from src.prestamos import (
    buscar_prestamo_por_id,
    calcular_dias_transcurridos,
    guardar_prestamos,
    obtener_prestamos,
    obtener_prestamos_activos_por_documento,
    obtener_prestamos_con_mas_de_30_dias,
)


def obtener_ventas() -> list[dict]:
    return leer_json(VENTAS_FILE)


def guardar_ventas(ventas: list[dict]) -> None:
    guardar_json(VENTAS_FILE, ventas)


def obtener_fecha_actual_texto() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def generar_id_venta() -> str:
    ventas = obtener_ventas()
    consecutivos = []

    for venta in ventas:
        id_venta = venta.get("id_venta", "")
        if id_venta.startswith("VEN-"):
            partes = id_venta.split("-")
            if len(partes) == 2 and partes[1].isdigit():
                consecutivos.append(int(partes[1]))

    siguiente = 1 if not consecutivos else max(consecutivos) + 1
    return f"VEN-{siguiente:03d}"


def generar_nombre_certificado(prestamo: dict, fecha_devolucion: str) -> str:
    nombre_usuario = prestamo["nombre_usuario"].replace(" ", "_")
    return f"{nombre_usuario}_{fecha_devolucion}_{prestamo['id_prestamo']}.txt"


def generar_nombre_factura(venta: dict) -> str:
    nombre_usuario = venta["nombre_usuario"].replace(" ", "_")
    return f"{nombre_usuario}_{venta['id_venta']}.txt"


def construir_contenido_certificado(prestamo: dict, fecha_devolucion: str, dias_transcurridos: int) -> str:
    return (
        "CERTIFICADO DE DEVOLUCIÓN\n"
        "====================================\n"
        f"Fecha de devolución: {fecha_devolucion}\n"
        f"ID del préstamo: {prestamo['id_prestamo']}\n"
        f"Usuario: {prestamo['nombre_usuario']}\n"
        f"Documento: {prestamo['documento_usuario']}\n"
        f"Ítem: {prestamo['nombre_item']}\n"
        f"ID del ítem: {prestamo['id_item']}\n"
        f"Categoría: {prestamo['categoria_item']}\n"
        f"Fecha del préstamo: {prestamo['fecha_prestamo']}\n"
        f"Fecha límite: {prestamo['fecha_limite']}\n"
        f"Días transcurridos: {dias_transcurridos}\n"
        f"Estado final: Devuelto\n"
        "====================================\n"
        "Se certifica que el artículo fue devuelto correctamente.\n"
    )


def construir_contenido_factura(venta: dict) -> str:
    return (
        "FACTURA DE VENTA POR INCUMPLIMIENTO\n"
        "====================================\n"
        f"ID de venta: {venta['id_venta']}\n"
        f"Fecha de venta: {venta['fecha_venta']}\n"
        f"ID del préstamo: {venta['id_prestamo']}\n"
        f"Usuario: {venta['nombre_usuario']}\n"
        f"Documento: {venta['documento_usuario']}\n"
        f"Ítem: {venta['nombre_item']}\n"
        f"ID del ítem: {venta['id_item']}\n"
        f"Categoría: {venta['categoria_item']}\n"
        f"Precio base: ${venta['subtotal']:.2f}\n"
        f"Impuesto por conchudez (23%): ${venta['impuesto']:.2f}\n"
        f"Total a pagar: ${venta['total']:.2f}\n"
        f"Días transcurridos: {venta['dias_transcurridos']}\n"
        "Motivo: El artículo superó los 30 días de préstamo y debe ser comprado por el prestador.\n"
        "====================================\n"
    )


def generar_certificado_devolucion(prestamo: dict, fecha_devolucion: str, dias_transcurridos: int) -> str:
    nombre_archivo = generar_nombre_certificado(prestamo, fecha_devolucion)
    ruta = CERTIFICADOS_DIR / nombre_archivo
    contenido = construir_contenido_certificado(prestamo, fecha_devolucion, dias_transcurridos)
    escribir_txt(ruta, contenido)
    return str(ruta)


def generar_factura_venta(venta: dict) -> str:
    nombre_archivo = generar_nombre_factura(venta)
    ruta = FACTURAS_DIR / nombre_archivo
    contenido = construir_contenido_factura(venta)
    escribir_txt(ruta, contenido)
    return str(ruta)


def listar_prestamos_activos_de_usuario(documento: str) -> list[dict]:
    return obtener_prestamos_activos_por_documento(documento)


def mostrar_prestamos_activos_de_usuario(documento: str) -> None:
    prestamos = listar_prestamos_activos_de_usuario(documento)

    if not prestamos:
        print("El usuario no tiene préstamos activos.")
        return

    print("\n--- Préstamos activos del usuario ---")
    for indice, prestamo in enumerate(prestamos, start=1):
        print(
            f"{indice}. ID préstamo: {prestamo['id_prestamo']} | "
            f"Ítem: {prestamo['nombre_item']} | "
            f"ID ítem: {prestamo['id_item']} | "
            f"Fecha préstamo: {prestamo['fecha_prestamo']} | "
            f"Fecha límite: {prestamo['fecha_limite']}"
        )


def registrar_devolucion() -> bool:
    print("\n--- Registrar devolución ---")
    documento = input("Ingrese el documento del usuario: ").strip()
    prestamos_usuario = listar_prestamos_activos_de_usuario(documento)

    if not prestamos_usuario:
        print("No se puede registrar la devolución porque el usuario no tiene préstamos activos.")
        return False

    mostrar_prestamos_activos_de_usuario(documento)
    id_prestamo = input("Ingrese el ID del préstamo a devolver: ").strip().upper()
    prestamo = buscar_prestamo_por_id(id_prestamo)

    if prestamo is None or prestamo.get("estado") != "Activo":
        print("Error: el préstamo no existe o no está activo.")
        return False

    fecha_devolucion = obtener_fecha_actual_texto()
    dias_transcurridos = calcular_dias_transcurridos(prestamo["fecha_prestamo"])

    if dias_transcurridos > 30:
        print("Este préstamo supera los 30 días. Debe gestionarse como venta.")
        return False

    prestamos = obtener_prestamos()
    for registro in prestamos:
        if registro.get("id_prestamo") == id_prestamo:
            registro["estado"] = "Devuelto"
            registro["fecha_devolucion"] = fecha_devolucion
            break

    guardar_prestamos(prestamos)
    actualizar_disponibilidad_item(prestamo["id_item"], True)

    ruta_certificado = generar_certificado_devolucion(prestamo, fecha_devolucion, dias_transcurridos)

    print("Devolución registrada correctamente.")
    print(f"Certificado generado en: {ruta_certificado}")
    return True


def construir_venta_desde_prestamo(prestamo: dict) -> dict | None:
    item = buscar_item_por_id(prestamo["id_item"])
    if item is None:
        return None

    subtotal = float(item["precio_compra"])
    impuesto = subtotal * IMPUESTO_CONCHUDEZ
    total = subtotal + impuesto
    fecha_venta = obtener_fecha_actual_texto()
    dias_transcurridos = calcular_dias_transcurridos(prestamo["fecha_prestamo"])

    return {
        "id_venta": generar_id_venta(),
        "id_prestamo": prestamo["id_prestamo"],
        "documento_usuario": prestamo["documento_usuario"],
        "nombre_usuario": prestamo["nombre_usuario"],
        "id_item": prestamo["id_item"],
        "nombre_item": prestamo["nombre_item"],
        "categoria_item": prestamo["categoria_item"],
        "fecha_venta": fecha_venta,
        "subtotal": subtotal,
        "impuesto": impuesto,
        "total": total,
        "dias_transcurridos": dias_transcurridos,
    }


def registrar_venta_por_id_prestamo(id_prestamo: str) -> bool:
    id_prestamo = id_prestamo.strip().upper()
    prestamo = buscar_prestamo_por_id(id_prestamo)

    if prestamo is None:
        print("Error: el préstamo no existe.")
        return False

    if prestamo.get("estado") != "Activo":
        print("Error: la venta solo aplica a préstamos activos.")
        return False

    dias_transcurridos = calcular_dias_transcurridos(prestamo["fecha_prestamo"])
    if dias_transcurridos <= 30:
        print("Error: este préstamo aún no supera los 30 días.")
        return False

    venta = construir_venta_desde_prestamo(prestamo)
    if venta is None:
        print("Error: no fue posible generar la venta.")
        return False

    ventas = obtener_ventas()
    ventas.append(venta)
    guardar_ventas(ventas)

    prestamos = obtener_prestamos()
    for registro in prestamos:
        if registro.get("id_prestamo") == id_prestamo:
            registro["estado"] = "Vendido por Incumplimiento"
            registro["fecha_venta"] = venta["fecha_venta"]
            break

    guardar_prestamos(prestamos)

    ruta_factura = generar_factura_venta(venta)

    print("Venta registrada correctamente.")
    print(f"Factura generada en: {ruta_factura}")
    return True


def mostrar_prestamos_vencidos_para_venta() -> None:
    prestamos = obtener_prestamos_con_mas_de_30_dias()

    if not prestamos:
        print("\nNo hay préstamos que superen 30 días.")
        return

    print("\n--- Préstamos vencidos para venta ---")
    for indice, prestamo in enumerate(prestamos, start=1):
        item = buscar_item_por_id(prestamo["id_item"])
        subtotal = float(item["precio_compra"]) if item else 0.0
        impuesto = subtotal * IMPUESTO_CONCHUDEZ
        total = subtotal + impuesto

        print(
            f"{indice}. ID préstamo: {prestamo['id_prestamo']} | "
            f"Usuario: {prestamo['nombre_usuario']} | "
            f"Ítem: {prestamo['nombre_item']} | "
            f"Días: {prestamo['dias_transcurridos']} | "
            f"Total estimado: ${total:.2f}"
        )


def registrar_venta_manual() -> bool:
    print("\n--- Generar venta por incumplimiento ---")
    mostrar_prestamos_vencidos_para_venta()
    id_prestamo = input("Ingrese el ID del préstamo a vender: ").strip().upper()
    return registrar_venta_por_id_prestamo(id_prestamo)