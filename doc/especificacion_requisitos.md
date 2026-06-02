# Especificación de Requisitos

## Introducción

Este documento presenta los requisitos funcionales y no funcionales del sistema **EIRA**, desarrollado para la gestión de préstamos de objetos mediante una aplicación de consola en Python. Su propósito es describir de forma clara las funciones que debe cumplir el sistema y las condiciones de calidad esperadas para su funcionamiento.

## Requisitos funcionales

Los requisitos funcionales describen las acciones y procesos que el sistema **EIRA** debe ejecutar para cumplir con su propósito de gestión de préstamos.

### RF1. Registro de usuarios
El sistema debe permitir registrar usuarios con los siguientes datos:
- Nombre
- Apellido
- Documento
- Correo electrónico
- Tiempo de préstamo permitido

### RF2. Validación de datos de usuario
El sistema debe validar que:
- El nombre tenga mínimo 3 letras y no contenga números.
- El apellido tenga mínimo 3 letras y no contenga números.
- El documento tenga entre 3 y 15 dígitos y contenga solo números.
- El correo electrónico incluya `@` y termine en `.com`.
- El tiempo de préstamo permitido solo pueda ser `5`, `10`, `15` o `30` días.

### RF3. Registro de ítems
El sistema debe permitir registrar ítems con la siguiente información:
- Nombre del ítem
- Categoría
- Precio de compra
- Estado del ítem

### RF4. Clasificación del estado del ítem
El sistema debe clasificar el estado del ítem usando una lógica difusa básica, a partir de una valoración numérica ingresada por el usuario.

### RF5. Generación de ID para ítems
El sistema debe generar automáticamente un identificador único para cada ítem según su categoría.

### RF6. Registro de préstamos
El sistema debe permitir registrar préstamos únicamente a usuarios previamente registrados y con ítems disponibles en el inventario.

### RF7. Cálculo de fecha límite
El sistema debe calcular automáticamente la fecha límite de devolución con base en la fecha de préstamo y el tiempo permitido para el usuario.

### RF8. Registro de devoluciones
El sistema debe permitir registrar devoluciones únicamente de préstamos activos.

### RF9. Generación de certificado de devolución
El sistema debe generar un certificado de devolución en formato TXT cuando un préstamo sea devuelto correctamente.

### RF10. Notificación de préstamos con 20 días o más
El sistema debe permitir consultar préstamos que tengan 20 o más días transcurridos desde su fecha de registro.

### RF11. Generación de venta por incumplimiento
El sistema debe generar una venta cuando un préstamo supere los 30 días de duración.

### RF12. Generación de factura de venta
El sistema debe generar una factura en formato TXT con subtotal, impuesto del 23% y total a pagar.

### RF13. Consulta del estado general de préstamos
El sistema debe mostrar el estado general de los préstamos ordenado por cantidad de días transcurridos.

### RF14. Exportación a CSV
El sistema debe permitir exportar el estado general de préstamos a un archivo en formato CSV.

### RF15. Acceso al módulo administrador
El sistema debe restringir el acceso al módulo administrador mediante usuario y contraseña.

### RF16. Generación de reportes administrativos
El sistema debe permitir consultar en el módulo administrador:
- Total de préstamos registrados
- Total de ítems devueltos
- Total de ventas realizadas
- Total pago realizado
- Lista de usuarios
- Usuario con mayor cantidad de préstamos
- Usuario con menor cantidad de préstamos

## Requisitos no funcionales

Los requisitos no funcionales describen las condiciones de calidad que debe cumplir el sistema **EIRA** durante su funcionamiento.

### RNF1. Usabilidad
El sistema debe presentar un menú de consola claro, entendible y fácil de usar para el usuario.

### RNF2. Organización del código
El proyecto debe mantener una estructura organizada, separando el código fuente en la carpeta `src` y la documentación en la carpeta `doc`.

### RNF3. Persistencia de la información
El sistema debe almacenar la información en archivos planos, permitiendo conservar los datos registrados entre ejecuciones.

### RNF4. Rendimiento
El sistema debe responder de manera adecuada en la consulta, registro y actualización de información para el volumen de datos manejado en un proyecto académico.

### RNF5. Mantenibilidad
El código debe ser legible, modular y fácil de comprender para facilitar su revisión, prueba y mejora.

### RNF6. Seguridad básica
El acceso al módulo administrador debe estar protegido mediante usuario y contraseña.

### RNF7. Portabilidad
El sistema debe poder ejecutarse en cualquier equipo que tenga instalado Python y una terminal compatible.

### RNF8. Integridad de datos
El sistema debe validar la información ingresada por el usuario para reducir errores en el registro de usuarios, ítems y préstamos.

### RNF9. Generación de documentos
El sistema debe permitir la creación de archivos TXT y CSV como evidencia de devoluciones, ventas y reportes.

### RNF10. Enfoque académico
El sistema debe responder a los requerimientos del trabajo final del curso y ser adecuado para su sustentación y evaluación académica.

## Conclusión

La especificación de requisitos del sistema **EIRA** permite establecer de manera clara las funciones principales del software y las condiciones de calidad esperadas para su desarrollo y uso. Este documento sirve como base para comprender el alcance del sistema y verificar que la solución implementada responda a las necesidades planteadas en el proyecto académico.