from src.archivos import guardar_json, leer_json
from src.config import CATEGORIAS_VALIDAS, ITEMS_FILE
from src.validaciones import (
    convertir_precio,
    limpiar_texto,
    validar_categoria,
    validar_nombre_item,
    validar_precio,
)


class Item:
    def __init__(
        self,
        id_item: str,
        nombre: str,
        categoria: str,
        precio_compra: float,
        estado: str,
        disponible: bool = True,
    ) -> None:
        self.id_item = id_item.strip().upper()
        self.nombre = nombre.strip().title()
        self.categoria = categoria.strip()
        self.precio_compra = float(precio_compra)
        self.estado = estado.strip()
        self.disponible = disponible

    def to_dict(self) -> dict:
        return {
            "id_item": self.id_item,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio_compra": self.precio_compra,
            "estado": self.estado,
            "disponible": self.disponible,
        }


def obtener_items() -> list[dict]:
    return leer_json(ITEMS_FILE)


def guardar_items(items: list[dict]) -> None:
    guardar_json(ITEMS_FILE, items)


def obtener_prefijo_categoria(categoria: str) -> str:
    prefijos = {
        "Videojuegos": "VID",
        "Libros": "LIB",
        "Música y video": "MUS",
        "Herramientas": "HER",
        "Dinero": "DIN",
        "Misceláneo y varios": "MIS",
    }
    return prefijos[categoria]


def generar_id_item(categoria: str) -> str:
    items = obtener_items()
    prefijo = obtener_prefijo_categoria(categoria)
    consecutivos = []

    for item in items:
        id_item = item.get("id_item", "")
        if id_item.startswith(prefijo + "-"):
            partes = id_item.split("-")
            if len(partes) == 2 and partes[1].isdigit():
                consecutivos.append(int(partes[1]))

    siguiente = 1 if not consecutivos else max(consecutivos) + 1
    return f"{prefijo}-{siguiente:03d}"


def calcular_estado_difuso(valor_estado: float) -> str:
    if valor_estado < 0 or valor_estado > 10:
        raise ValueError("La valoración del estado debe estar entre 0 y 10.")

    if valor_estado < 4:
        return "Malo"
    if valor_estado < 7:
        return "Regular"
    return "Bueno"


def buscar_item_por_id(id_item: str) -> dict | None:
    id_item = limpiar_texto(id_item).upper()
    items = obtener_items()

    for item in items:
        if item.get("id_item") == id_item:
            return item

    return None


def pedir_nombre_item() -> str:
    while True:
        nombre = input("Ingrese el nombre del ítem: ").strip()
        if validar_nombre_item(nombre):
            return limpiar_texto(nombre)
        print("Error: el nombre del ítem debe tener al menos 3 caracteres.")


def pedir_categoria() -> str:
    while True:
        print("\nCategorías disponibles:")
        for indice, categoria in enumerate(CATEGORIAS_VALIDAS, start=1):
            print(f"{indice}. {categoria}")

        categoria = input("Ingrese la categoría exacta del ítem: ").strip()
        if validar_categoria(categoria):
            return limpiar_texto(categoria)

        print("Error: debe elegir una categoría válida.")


def pedir_precio_compra() -> float:
    while True:
        precio_texto = input("Ingrese el precio de compra del ítem: ").strip()
        if validar_precio(precio_texto):
            return convertir_precio(precio_texto)
        print("Error: el precio debe ser numérico y mayor que 0.")


def pedir_valor_estado() -> float:
    while True:
        valor_texto = input("Ingrese una valoración del estado del ítem entre 0 y 10: ").strip()
        try:
            valor = float(valor_texto)
            if 0 <= valor <= 10:
                return valor
            print("Error: la valoración debe estar entre 0 y 10.")
        except ValueError:
            print("Error: ingrese un número válido.")


def registrar_item() -> bool:
    print("\n--- Registro de Ítem ---")

    nombre = pedir_nombre_item()
    categoria = pedir_categoria()
    precio_compra = pedir_precio_compra()
    valor_estado = pedir_valor_estado()

    id_item = generar_id_item(categoria)
    estado = calcular_estado_difuso(valor_estado)

    item = Item(
        id_item=id_item,
        nombre=nombre,
        categoria=categoria,
        precio_compra=precio_compra,
        estado=estado,
        disponible=True,
    )

    items = obtener_items()
    items.append(item.to_dict())
    guardar_items(items)

    print(f"Ítem registrado correctamente con ID: {id_item}")
    print(f"Estado asignado: {estado}")
    return True


def listar_items() -> None:
    items = obtener_items()

    if not items:
        print("\nNo hay ítems registrados.")
        return

    print("\n--- Inventario General ---")
    for indice, item in enumerate(items, start=1):
        disponibilidad = "Disponible" if item["disponible"] else "No disponible"
        print(
            f"{indice}. ID: {item['id_item']} | "
            f"Nombre: {item['nombre']} | "
            f"Categoría: {item['categoria']} | "
            f"Precio: ${item['precio_compra']:.2f} | "
            f"Estado: {item['estado']} | "
            f"{disponibilidad}"
        )


def listar_items_disponibles() -> None:
    items = obtener_items()
    disponibles = [item for item in items if item.get("disponible") is True]

    if not disponibles:
        print("\nNo hay ítems disponibles para préstamo.")
        return

    print("\n--- Ítems Disponibles ---")
    for indice, item in enumerate(disponibles, start=1):
        print(
            f"{indice}. ID: {item['id_item']} | "
            f"Nombre: {item['nombre']} | "
            f"Categoría: {item['categoria']} | "
            f"Precio: ${item['precio_compra']:.2f} | "
            f"Estado: {item['estado']}"
        )


def actualizar_disponibilidad_item(id_item: str, disponible: bool) -> bool:
    items = obtener_items()
    id_item = limpiar_texto(id_item).upper()

    for item in items:
        if item.get("id_item") == id_item:
            item["disponible"] = disponible
            guardar_items(items)
            return True

    return False