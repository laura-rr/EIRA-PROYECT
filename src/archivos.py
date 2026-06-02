import csv
import json
from pathlib import Path
from typing import Any

from src.config import ARCHIVOS_JSON_BASE


def crear_archivos_base() -> None:
    for ruta, contenido_inicial in ARCHIVOS_JSON_BASE.items():
        if not ruta.exists():
            guardar_json(ruta, contenido_inicial)


def leer_json(ruta: Path) -> list[dict[str, Any]]:
    if not ruta.exists():
        return []

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
            if isinstance(contenido, list):
                return contenido
            return []
    except (json.JSONDecodeError, OSError):
        return []


def guardar_json(ruta: Path, datos: list[dict[str, Any]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def escribir_txt(ruta: Path, contenido: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def exportar_csv(ruta: Path, filas: list[dict[str, Any]]) -> bool:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    if not filas:
        return False

    encabezados = list(filas[0].keys())

    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=encabezados)
        writer.writeheader()
        writer.writerows(filas)

    return True