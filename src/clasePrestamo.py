class clasePrestamo:
    def __init__(
        self,
        id_prestamo: str,
        documento_usuario: str,
        nombre_usuario: str,
        id_item: str,
        nombre_item: str,
        categoria_item: str,
        fecha_prestamo: str,
        fecha_limite: str,
        estado: str = "Activo",
        fecha_devolucion: str = "",
        fecha_venta: str = "",
    ) -> None:
        self.id_prestamo = id_prestamo.strip().upper()
        self.documento_usuario = documento_usuario.strip()
        self.nombre_usuario = nombre_usuario.strip()
        self.id_item = id_item.strip().upper()
        self.nombre_item = nombre_item.strip()
        self.categoria_item = categoria_item.strip()
        self.fecha_prestamo = fecha_prestamo.strip()
        self.fecha_limite = fecha_limite.strip()
        self.estado = estado.strip()
        self.fecha_devolucion = fecha_devolucion.strip()
        self.fecha_venta = fecha_venta.strip()

    def to_dict(self) -> dict:
        return {
            "id_prestamo": self.id_prestamo,
            "documento_usuario": self.documento_usuario,
            "nombre_usuario": self.nombre_usuario,
            "id_item": self.id_item,
            "nombre_item": self.nombre_item,
            "categoria_item": self.categoria_item,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_limite": self.fecha_limite,
            "estado": self.estado,
            "fecha_devolucion": self.fecha_devolucion,
            "fecha_venta": self.fecha_venta,
        }
