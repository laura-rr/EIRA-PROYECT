# Manual de Usuario

## Introducción

El presente manual tiene como objetivo guiar al usuario en el uso del sistema **EIRA**, un programa desarrollado en Python para la gestión de préstamos por consola. El sistema permite registrar usuarios, registrar ítems, gestionar préstamos, registrar devoluciones, generar ventas por incumplimiento y consultar reportes administrativos.

## Uso del sistema

El sistema **EIRA** funciona mediante un menú principal en consola. Desde allí, el usuario puede acceder a las diferentes opciones disponibles para registrar información, gestionar préstamos, registrar devoluciones, generar ventas y consultar reportes.

Al ejecutar el programa, se mostrará un menú con las acciones principales del sistema. El usuario debe ingresar el número correspondiente a la opción que desea utilizar.

## Menú principal

Al iniciar el programa, el sistema presenta un menú principal con las opciones necesarias para gestionar el funcionamiento de **EIRA**. Desde este menú se puede acceder al registro de usuarios, registro de ítems, préstamos, devoluciones, ventas, consultas y módulo administrador.

Las opciones disponibles son:

1. Registrar usuario  
2. Registrar ítem  
3. Registrar préstamo  
4. Registrar devolución  
5. Generar venta por incumplimiento  
6. Listar usuarios  
7. Consultar usuario por documento  
8. Listar inventario general  
9. Listar ítems disponibles  
10. Listar préstamos  
11. Listar préstamos activos  
12. Ver notificaciones de 20 días  
13. Ver préstamos candidatos a venta  
14. Consultar estado general de préstamos  
15. Exportar estado general a CSV  
16. Módulo administrador  
0. Salir

## Registro de usuarios

La opción **Registrar usuario** permite almacenar la información básica de cada persona que puede recibir préstamos dentro del sistema.

Para registrar un usuario, el programa solicita los siguientes datos:

- Nombre
- Apellido
- Documento
- Correo electrónico
- Tiempo de préstamo permitido

### Validaciones aplicadas

El sistema valida la información ingresada antes de guardar el usuario:

- **Nombre:** mínimo 3 letras y no puede contener números.
- **Apellido:** mínimo 3 letras y no puede contener números.
- **Documento:** solo puede contener números y debe tener entre 3 y 15 dígitos.
- **Correo electrónico:** debe incluir `@` y terminar en `.com`.
- **Tiempo de préstamo:** solo se permiten los valores `5`, `10`, `15` o `30` días.

Si alguno de los datos no cumple estas condiciones, el sistema muestra un mensaje de error y solicita nuevamente la información.

## Registro de ítems

La opción **Registrar ítem** permite agregar al inventario los objetos que podrán ser prestados a los usuarios registrados en el sistema.

Para registrar un ítem, el programa solicita los siguientes datos:

- Nombre del ítem
- Categoría
- Precio de compra
- Valoración del estado del ítem

### Validaciones aplicadas

El sistema valida la información ingresada antes de guardar el ítem:

- **Nombre del ítem:** debe tener al menos 3 caracteres.
- **Categoría:** debe pertenecer a una de las categorías permitidas por el sistema.
- **Precio de compra:** debe ser un valor numérico mayor que cero.
- **Valoración del estado:** debe estar entre 0 y 10.

### Categorías disponibles

Las categorías permitidas en el sistema son:

- Videojuegos
- Libros
- Música y video
- Herramientas
- Dinero
- Misceláneo y varios

### Generación del ID del ítem

Cada ítem registrado recibe un identificador único de acuerdo con su categoría. Este ID se genera automáticamente con un prefijo y un número consecutivo.

Ejemplos:

- `VID-001` para Videojuegos
- `LIB-001` para Libros
- `HER-001` para Herramientas

### Estado del ítem

El sistema clasifica el estado del ítem usando una lógica difusa básica, según la valoración ingresada por el usuario:

- **Malo:** de 0 a menos de 4
- **Regular:** de 4 a menos de 7
- **Bueno:** de 7 a 10

Si los datos son válidos, el ítem queda registrado en el inventario y disponible para préstamo.

## Registro de préstamos

La opción **Registrar préstamo** permite asociar un ítem disponible a un usuario previamente registrado en el sistema.

Para realizar un préstamo, el programa verifica primero que el usuario exista y que el ítem seleccionado se encuentre disponible en el inventario. Si alguna de estas condiciones no se cumple, el sistema no permite continuar con el registro.

### Condiciones del préstamo

- El usuario debe estar registrado previamente.
- El ítem debe existir en el inventario.
- El ítem debe estar disponible para préstamo.
- El tiempo de préstamo se toma a partir de la configuración definida para el usuario.

### Información registrada en el préstamo

Cuando el préstamo es exitoso, el sistema almacena:

- ID del préstamo
- Documento del usuario
- Nombre del usuario
- ID del ítem
- Nombre del ítem
- Categoría del ítem
- Fecha de préstamo
- Fecha límite de devolución
- Estado del préstamo

Una vez registrado el préstamo, el ítem cambia su estado de disponibilidad para evitar que sea prestado nuevamente mientras siga activo.

## Registro de devoluciones

La opción **Registrar devolución** permite devolver un ítem que haya sido prestado previamente y que aún se encuentre en estado activo dentro del sistema.

Para registrar una devolución, el programa solicita el documento del usuario y verifica si este tiene préstamos activos. Si el usuario no tiene préstamos registrados en estado activo, el sistema informa que no es posible realizar la devolución.

### Condiciones de la devolución

- Solo se pueden devolver préstamos que estén en estado **Activo**.
- El usuario debe tener al menos un préstamo activo registrado.
- Si el préstamo supera los 30 días, no se procesa como devolución, sino como venta por incumplimiento.

### Proceso de devolución

Cuando la devolución es válida, el sistema realiza las siguientes acciones:

- Cambia el estado del préstamo a **Devuelto**.
- Registra la fecha de devolución.
- Actualiza el ítem como disponible nuevamente.
- Genera un certificado de devolución en formato TXT.

### Certificado de devolución

El certificado generado incluye información como:

- Fecha de devolución
- ID del préstamo
- Nombre y documento del usuario
- Nombre e ID del ítem
- Categoría del ítem
- Fecha del préstamo
- Fecha límite
- Días transcurridos
- Estado final del préstamo

El archivo se guarda automáticamente en la carpeta `salidas/certificados/`.

## Generación de ventas por incumplimiento

La opción **Generar venta por incumplimiento** se utiliza cuando un préstamo supera los 30 días desde su fecha de registro. En este caso, el sistema no permite la devolución del ítem y procede a generar una venta obligatoria al usuario responsable.

### Condiciones para generar la venta

- El préstamo debe estar en estado **Activo**.
- Deben haber transcurrido más de 30 días desde la fecha del préstamo.
- El sistema toma como base el precio de compra del ítem registrado en el inventario.

### Proceso de venta

Cuando se genera la venta, el sistema realiza las siguientes acciones:

- Registra la venta en el archivo correspondiente.
- Calcula el valor base del artículo.
- Aplica el impuesto por conchudez del 23%.
- Calcula el total a pagar.
- Cambia el estado del préstamo a **Vendido por Incumplimiento**.
- Genera una factura de venta en formato TXT.

### Información de la factura

La factura generada contiene:

- ID de la venta
- Fecha de venta
- ID del préstamo
- Nombre y documento del usuario
- Nombre, ID y categoría del ítem
- Subtotal
- Impuesto del 23%
- Total a pagar
- Días transcurridos
- Motivo de la venta

El archivo se guarda automáticamente en la carpeta `salidas/facturas/`.

## Reportes y módulo administrador

El sistema **EIRA** incluye funciones de consulta y control que permiten conocer el estado general de los préstamos y acceder a información administrativa del programa.

### Estado general de préstamos

La opción **Consultar estado general de préstamos** permite visualizar todos los préstamos registrados en el sistema, mostrando la información organizada según la cantidad de días transcurridos desde la fecha de préstamo.

La información presentada incluye:

- ID del préstamo
- Nombre del usuario
- Documento del usuario
- Nombre del ítem
- ID del ítem
- Categoría
- Fecha de préstamo
- Fecha límite
- Estado del préstamo
- Días transcurridos

### Exportación a CSV

El sistema permite exportar el estado general de préstamos a un archivo en formato CSV. Esta función facilita la consulta externa de la información y el manejo de estadísticas en otras herramientas.

El archivo exportado se guarda automáticamente en la carpeta:

- `salidas/csv/`

### Módulo administrador

El acceso al módulo administrador está protegido mediante usuario y contraseña. Solo quienes tengan credenciales válidas pueden ingresar a esta sección.

Dentro del módulo administrador se pueden consultar los siguientes reportes:

- Total de préstamos registrados
- Total de ítems devueltos
- Total de ventas realizadas
- Total pago realizado
- Lista de usuarios
- Usuario con mayor cantidad de préstamos
- Usuario con menor cantidad de préstamos

## Recomendaciones de uso

Para un correcto funcionamiento del sistema, se recomienda:

- Registrar primero los usuarios antes de intentar generar préstamos.
- Registrar los ítems en el inventario antes de prestarlos.
- Verificar que los datos ingresados cumplan con las validaciones del sistema.
- Revisar periódicamente las notificaciones de préstamos con 20 o más días.
- Consultar los préstamos con más de 30 días para gestionar ventas por incumplimiento.
- Utilizar el módulo administrador para revisar estadísticas generales del sistema.
- Exportar el reporte CSV cuando se requiera consultar la información fuera del programa.

## Cierre

El sistema **EIRA** fue desarrollado para ofrecer una solución organizada y funcional al problema de gestión de préstamos planteado en el curso. A través de sus diferentes módulos, permite controlar usuarios, inventario, préstamos, devoluciones, ventas y reportes, cumpliendo con los requerimientos principales del proyecto.

Además, el uso de archivos planos, exportación a CSV y generación de documentos en texto plano permite que la información sea fácil de almacenar, consultar y presentar durante la sustentación del trabajo.