from src.archivos import crear_archivos_base
from src.config import inicializar_proyecto
from src.facturacion import (
    registrar_devolucion,
    registrar_venta_manual,
)
from src.items import (
    listar_items,
    listar_items_disponibles,
    registrar_item,
)
from src.prestamos import (
    listar_prestamos,
    listar_prestamos_activos,
    mostrar_notificaciones_20_dias,
    mostrar_prestamos_para_venta,
    registrar_prestamo,
)
from src.reportes import (
    exportar_estado_general_prestamos_csv,
    menu_administrador,
    mostrar_estado_general_prestamos,
)
from src.usuarios import (
    listar_usuarios,
    mostrar_usuario_por_documento,
    registrar_usuario,
)


def mostrar_menu_principal() -> None:
    print("\n" + "=" * 50)
    print("      SISTEMA DE GESTIÓN DE PRÉSTAMOS EIRA")
    print("=" * 50)
    print("1. Registrar usuario")
    print("2. Registrar ítem")
    print("3. Registrar préstamo")
    print("4. Registrar devolución")
    print("5. Generar venta por incumplimiento")
    print("6. Listar usuarios")
    print("7. Consultar usuario por documento")
    print("8. Listar inventario general")
    print("9. Listar ítems disponibles")
    print("10. Listar préstamos")
    print("11. Listar préstamos activos")
    print("12. Ver notificaciones de 20 días")
    print("13. Ver préstamos candidatos a venta")
    print("14. Consultar estado general de préstamos")
    print("15. Exportar estado general a CSV")
    print("16. Módulo administrador")
    print("0. Salir")
    print("=" * 50)


def ejecutar_opcion(opcion: str) -> bool:
    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        registrar_item()
    elif opcion == "3":
        registrar_prestamo()
    elif opcion == "4":
        registrar_devolucion()
    elif opcion == "5":
        registrar_venta_manual()
    elif opcion == "6":
        listar_usuarios()
    elif opcion == "7":
        mostrar_usuario_por_documento()
    elif opcion == "8":
        listar_items()
    elif opcion == "9":
        listar_items_disponibles()
    elif opcion == "10":
        listar_prestamos()
    elif opcion == "11":
        listar_prestamos_activos()
    elif opcion == "12":
        mostrar_notificaciones_20_dias()
    elif opcion == "13":
        mostrar_prestamos_para_venta()
    elif opcion == "14":
        mostrar_estado_general_prestamos()
    elif opcion == "15":
        exportar_estado_general_prestamos_csv()
    elif opcion == "16":
        menu_administrador()
    elif opcion == "0":
        print("Gracias por usar el sistema.")
        return False
    else:
        print("Opción inválida. Intente de nuevo.")
    return True


def main() -> None:
    inicializar_proyecto()
    crear_archivos_base()

    continuar = True
    while continuar:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        continuar = ejecutar_opcion(opcion)


if __name__ == "__main__":
    main()