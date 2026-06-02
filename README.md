# EIRA

Sistema de gestión de préstamos desarrollado en Python para consola, orientado al registro de usuarios, inventario de ítems, préstamos, devoluciones, ventas por incumplimiento y generación de reportes.

## Descripción del proyecto

**EIRA** es un software académico desarrollado para dar solución al problema planteado en el curso de Algoritmia y Programación. El sistema permite gestionar préstamos de objetos, registrar usuarios, controlar devoluciones, generar certificados, emitir facturas por incumplimiento y consultar reportes generales.

El programa funciona desde consola y almacena la información mediante archivos planos en formato JSON, además de permitir la exportación de reportes a CSV.

## Objetivo

Construir un programa en Python que permita:

- Registrar usuarios con validaciones.
- Registrar ítems dentro de un inventario.
- Crear préstamos únicamente a usuarios registrados.
- Registrar devoluciones de préstamos activos.
- Generar certificados de devolución en texto plano.
- Detectar préstamos con 20 o más días para notificación.
- Generar ventas por incumplimiento cuando un préstamo supera los 30 días.
- Emitir facturas con impuesto del 23%.
- Consultar reportes generales y administrativos.
- Exportar el estado general de préstamos a CSV.

## Funcionalidades principales

### Gestión de usuarios

- Registro de usuarios.
- Validación de nombre, apellido, documento, correo y tiempo de préstamo.
- Consulta de usuarios registrados.

### Gestión de ítems

- Registro de ítems por categoría.
- Generación de ID único por categoría.
- Registro del precio de compra.
- Clasificación del estado del ítem mediante lógica difusa básica.
- Consulta de inventario general y de ítems disponibles.

### Gestión de préstamos

- Registro de préstamos.
- Validación de usuario existente.
- Validación de disponibilidad del ítem.
- Cálculo de fecha de préstamo y fecha límite.
- Consulta de préstamos activos y generales.

### Devoluciones y ventas

- Registro de devoluciones de préstamos activos.
- Generación de certificado de devolución en TXT.
- Detección de préstamos con 20 o más días.
- Generación de venta por incumplimiento.
- Cálculo de subtotal, impuesto por conchudez del 23% y total.
- Generación de factura de venta en TXT.

### Reportes y administración

- Total de préstamos registrados.
- Total de ítems devueltos.
- Total de ventas realizadas.
- Total pago realizado.
- Lista de usuarios.
- Usuario con mayor y menor cantidad de préstamos.
- Estado general de préstamos ordenado por días transcurridos.
- Exportación de reporte general a CSV.
- Acceso a módulo administrador con usuario y contraseña.

## Estructura del proyecto

```text
EIRA/
├── README.md
├── main.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── archivos.py
│   ├── validaciones.py
│   ├── claseUsuarios.py
│   ├── clasePrestamo.py
│   ├── items.py
│   ├── usuarios.py
│   ├── prestamos.py
│   ├── facturacion.py
│   └── reportes.py
├── data/
│   ├── usuarios.json
│   ├── items.json
│   ├── prestamos.json
│   ├── ventas.json
│   └── administradores.json
├── salidas/
│   ├── certificados/
│   ├── facturas/
│   └── csv/
└── doc/
    ├── manual_usuario.md
    ├── licencia.md
    ├── reporte_vision.md
    ├── especificacion_requisitos.md
    ├── plan_proyecto.md
    └── plan_versionado.md
```

## Requisitos

- Python 3.10 o superior
- Consola o terminal
- No requiere librerías externas adicionales

## Ejecución del programa

Ubícate en la carpeta raíz del proyecto y ejecuta:

```bash
python main.py

## Credenciales de administrador

El sistema incluye un acceso básico al módulo administrador con las siguientes credenciales iniciales:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

Estas credenciales se almacenan en:

```text
data/administradores.json
```

## Archivos generados por el sistema

El programa genera automáticamente salidas en las siguientes carpetas:

- `salidas/certificados/`: certificados de devolución en TXT
- `salidas/facturas/`: facturas de venta en TXT
- `salidas/csv/`: reportes exportados en CSV

## Tecnologías utilizadas

- Python
- Programación orientada a objetos
- Archivos planos JSON
- Exportación CSV
- Consola interactiva

## Cumplimiento del enunciado

Este proyecto fue diseñado para cumplir con los requisitos del trabajo final, incluyendo:

- uso de clases y objetos
- manejo de usuarios
- manejo de préstamos
- registro de ítems
- devoluciones
- ventas por incumplimiento
- reportes administrativos
- almacenamiento en archivos planos
- exportación a CSV
- estructura del código en carpeta `src`
- manual de usuario en carpeta `doc`

## Integrantes

- Integrante 1: Eidy Vanesa Martelos Zapata
- Integrante 2: Laura Rodriguez

## Curso

**Algoritmia y Programación**  
**Facultad de Ingeniería**  
**Departamento de Ingeniería Industrial**

## Licencia

Este proyecto tiene una licencia de uso académico y educativo. La información completa se encuentra en el archivo:
doc/licencia.md

## Observaciones

Este sistema fue desarrollado con fines académicos como solución al proyecto integrador del curso.