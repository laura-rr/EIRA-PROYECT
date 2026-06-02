from src.archivos import guardar_json, leer_json
from src.claseUsuarios import claseUsuarios
from src.config import USUARIOS_FILE
from src.validaciones import (
    convertir_tiempo_prestamo,
    limpiar_texto,
    validar_correo,
    validar_documento,
    validar_nombre_apellido,
    validar_tiempo_prestamo,
)


def obtener_usuarios() -> list[dict]:
    return leer_json(USUARIOS_FILE)


def buscar_usuario_por_documento(documento: str) -> dict | None:
    documento = limpiar_texto(documento)
    usuarios = obtener_usuarios()

    for usuario in usuarios:
        if usuario.get("documento") == documento:
            return usuario

    return None


def existe_usuario(documento: str) -> bool:
    return buscar_usuario_por_documento(documento) is not None


def guardar_usuario(usuario: claseUsuarios) -> None:
    usuarios = obtener_usuarios()
    usuarios.append(usuario.to_dict())
    guardar_json(USUARIOS_FILE, usuarios)


def pedir_nombre() -> str:
    while True:
        nombre = input("Ingrese el nombre: ").strip()
        if validar_nombre_apellido(nombre):
            return limpiar_texto(nombre)
        print("Error: el nombre debe tener al menos 3 letras y no puede contener números.")


def pedir_apellido() -> str:
    while True:
        apellido = input("Ingrese el apellido: ").strip()
        if validar_nombre_apellido(apellido):
            return limpiar_texto(apellido)
        print("Error: el apellido debe tener al menos 3 letras y no puede contener números.")


def pedir_documento() -> str:
    while True:
        documento = input("Ingrese el documento: ").strip()
        if not validar_documento(documento):
            print("Error: el documento debe tener entre 3 y 15 dígitos y solo números.")
            continue

        if existe_usuario(documento):
            print("Error: ya existe un usuario registrado con ese documento.")
            continue

        return limpiar_texto(documento)


def pedir_correo() -> str:
    while True:
        correo = input("Ingrese el correo electrónico: ").strip()
        if validar_correo(correo):
            return limpiar_texto(correo).lower()
        print("Error: el correo debe tener formato válido y terminar en .com.")


def pedir_tiempo_prestamo() -> int:
    while True:
        tiempo_texto = input("Ingrese el tiempo de préstamo permitido (5, 10, 15 o 30): ").strip()

        if not tiempo_texto.isdigit():
            print("Error: el tiempo de préstamo debe ser numérico.")
            continue

        tiempo = convertir_tiempo_prestamo(tiempo_texto)
        if validar_tiempo_prestamo(tiempo):
            return tiempo

        print("Error: solo se permiten 5, 10, 15 o 30 días.")


def registrar_usuario() -> bool:
    print("\n--- Registro de Usuario ---")

    nombre = pedir_nombre()
    apellido = pedir_apellido()
    documento = pedir_documento()
    correo = pedir_correo()
    tiempo_prestamo = pedir_tiempo_prestamo()

    usuario = claseUsuarios(
        nombre=nombre,
        apellido=apellido,
        documento=documento,
        correo=correo,
        tiempo_prestamo=tiempo_prestamo,
    )

    guardar_usuario(usuario)
    print("Usuario registrado correctamente.")
    return True


def listar_usuarios() -> None:
    usuarios = obtener_usuarios()

    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return

    print("\n--- Lista de Usuarios ---")
    for indice, usuario in enumerate(usuarios, start=1):
        print(
            f"{indice}. {usuario['nombre']} {usuario['apellido']} | "
            f"Documento: {usuario['documento']} | "
            f"Correo: {usuario['correo']} | "
            f"Tiempo préstamo: {usuario['tiempo_prestamo']} días"
        )


def mostrar_usuario_por_documento() -> None:
    documento = input("Ingrese el documento del usuario a consultar: ").strip()
    usuario = buscar_usuario_por_documento(documento)

    if usuario is None:
        print("Usuario no encontrado.")
        return

    print("\n--- Usuario Encontrado ---")
    print(f"Nombre: {usuario['nombre']} {usuario['apellido']}")
    print(f"Documento: {usuario['documento']}")
    print(f"Correo: {usuario['correo']}")
    print(f"Tiempo de préstamo: {usuario['tiempo_prestamo']} días")