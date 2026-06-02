class claseUsuarios:
    def __init__(
        self,
        nombre: str,
        apellido: str,
        documento: str,
        correo: str,
        tiempo_prestamo: int,
    ) -> None:
        self.nombre = nombre.strip().title()
        self.apellido = apellido.strip().title()
        self.documento = documento.strip()
        self.correo = correo.strip().lower()
        self.tiempo_prestamo = tiempo_prestamo

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "correo": self.correo,
            "tiempo_prestamo": self.tiempo_prestamo,
        }
    
    