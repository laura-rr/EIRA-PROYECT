import re

from src.config import CATEGORIAS_VALIDAS, TIEMPOS_PRESTAMO_VALIDOS


def limpiar_texto(texto: str) -> str:
    return texto.strip()


def validar_nombre_apellido(texto: str) -> bool:
    texto = limpiar_texto(texto)
    if len(texto) < 3:
        return False
    return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+", texto))


def validar_documento(documento: str) -> bool:
    documento = limpiar_texto(documento)
    if not documento.isdigit():
        return False
    return 3 <= len(documento) <= 15


def validar_correo(correo: str) -> bool:
    correo = limpiar_texto(correo)
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$"
    return bool(re.fullmatch(patron, correo))


def validar_tiempo_prestamo(tiempo: int) -> bool:
    return tiempo in TIEMPOS_PRESTAMO_VALIDOS


def validar_nombre_item(nombre: str) -> bool:
    nombre = limpiar_texto(nombre)
    return len(nombre) >= 3


def validar_categoria(categoria: str) -> bool:
    categoria = limpiar_texto(categoria)
    return categoria in CATEGORIAS_VALIDAS


def validar_precio(precio_texto: str) -> bool:
    precio_texto = limpiar_texto(precio_texto)
    try:
        precio = float(precio_texto)
        return precio > 0
    except ValueError:
        return False


def convertir_precio(precio_texto: str) -> float:
    return float(limpiar_texto(precio_texto))


def convertir_tiempo_prestamo(tiempo_texto: str) -> int:
    return int(limpiar_texto(tiempo_texto))