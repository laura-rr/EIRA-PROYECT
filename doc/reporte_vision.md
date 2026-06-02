# Reporte de Visión

## Introducción

El presente documento describe la visión general del sistema **EIRA**, desarrollado como solución al problema de gestión de préstamos planteado en el curso de **Algoritmia y Programación**. Su propósito es presentar de forma clara la idea central del software, sus objetivos y los beneficios que ofrece al usuario.

## Descripción general del software

**EIRA** es un programa de consola desarrollado en Python que permite gestionar el préstamo de objetos mediante el registro de usuarios, control de inventario, creación de préstamos, devoluciones, generación de ventas por incumplimiento y consulta de reportes.

El sistema fue diseñado para responder a la necesidad de organizar la información relacionada con los artículos prestados, evitando pérdidas de control sobre quién tiene cada objeto, cuándo fue prestado y cuál es su estado actual.

## Problema que resuelve

El software busca solucionar la dificultad de llevar un control manual sobre los préstamos de objetos. En muchos casos, cuando no existe un registro organizado, se pierde información importante como:

- A quién se le prestó un objeto
- Qué artículo fue prestado
- Cuándo se realizó el préstamo
- Cuándo debía devolverse
- Si el objeto fue devuelto o debe ser cobrado

**EIRA** permite centralizar esta información y facilitar su consulta mediante un sistema sencillo, organizado y funcional.

## Objetivo del sistema

El objetivo principal de **EIRA** es permitir la administración de préstamos de objetos de manera estructurada, utilizando archivos planos y un sistema de consola que facilite el registro, control y seguimiento de usuarios, ítems y préstamos.

## Beneficios del software

Entre los principales beneficios del sistema se encuentran:

- Organización de la información de usuarios e ítems
- Mejor control sobre los préstamos activos
- Seguimiento de tiempos de préstamo
- Registro formal de devoluciones
- Generación de ventas por incumplimiento
- Acceso a reportes administrativos
- Exportación de información a CSV
- Facilidad de uso desde consola

## Alcance

El sistema **EIRA** permite:

- Registrar usuarios con validaciones
- Registrar ítems con categoría, precio y estado
- Crear préstamos a usuarios registrados
- Registrar devoluciones de préstamos activos
- Generar certificados de devolución
- Generar facturas de venta por incumplimiento
- Consultar reportes generales y administrativos
- Exportar información a CSV

El alcance del proyecto está orientado a fines académicos y al cumplimiento de los requerimientos establecidos en el trabajo final del curso.

## Usuarios del sistema

El sistema está orientado principalmente a un usuario administrador del préstamo de objetos, quien necesita registrar información, consultar el estado de los préstamos y generar reportes del funcionamiento general del sistema.

## Conclusión

El proyecto **EIRA** representa una solución práctica y académica para la gestión de préstamos, permitiendo un mejor control de la información y facilitando los procesos de registro, consulta y seguimiento requeridos en el contexto del curso.