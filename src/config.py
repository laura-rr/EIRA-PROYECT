from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
SALIDAS_DIR = BASE_DIR / "salidas"
CERTIFICADOS_DIR = SALIDAS_DIR / "certificados"
FACTURAS_DIR = SALIDAS_DIR / "facturas"
CSV_DIR = SALIDAS_DIR / "csv"
DOC_DIR = BASE_DIR / "doc"

USUARIOS_FILE = DATA_DIR / "usuarios.json"
ITEMS_FILE = DATA_DIR / "items.json"
PRESTAMOS_FILE = DATA_DIR / "prestamos.json"
VENTAS_FILE = DATA_DIR / "ventas.json"
ADMINISTRADORES_FILE = DATA_DIR / "administradores.json"

CATEGORIAS_VALIDAS = [
    "Videojuegos",
    "Libros",
    "Música y video",
    "Herramientas",
    "Dinero",
    "Misceláneo y varios",
]

TIEMPOS_PRESTAMO_VALIDOS = [5, 10, 15, 30]
IMPUESTO_CONCHUDEZ = 0.23

ARCHIVOS_JSON_BASE = {
    USUARIOS_FILE: [],
    ITEMS_FILE: [],
    PRESTAMOS_FILE: [],
    VENTAS_FILE: [],
    ADMINISTRADORES_FILE: [
        {
            "usuario": "admin",
            "contrasena": "admin123",
        }
    ],
}


def inicializar_proyecto() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SALIDAS_DIR.mkdir(parents=True, exist_ok=True)
    CERTIFICADOS_DIR.mkdir(parents=True, exist_ok=True)
    FACTURAS_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)