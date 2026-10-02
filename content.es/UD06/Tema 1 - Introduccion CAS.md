# Tema 1 - Introducción a las bases de datos

> Datos, sistemas gestores y principios de diseño para almacenar información de forma segura y eficiente.

| Datos del tema | Información |
| --- | --- |
| Módulo | Bases de Datos |
| Curso | 1.º ASIR |
| Modalidad | Semipresencial |

## Índice

1. [Datos, información y representación](#1-datos-información-y-representación)
2. [Bases de datos y sistemas gestores](#2-bases-de-datos-y-sistemas-gestores)
3. [Arquitectura y componentes de un SGBD](#3-arquitectura-y-componentes-de-un-sgbd)
4. [Integridad, concurrencia y transacciones](#4-integridad-concurrencia-y-transacciones)
5. [Seguridad, recuperación y administración](#5-seguridad-recuperación-y-administración)
6. [Modelos, arquitecturas y lenguajes](#6-modelos-arquitecturas-y-lenguajes)
7. [Resumen](#7-resumen)
8. [Recursos](#8-recursos)
9. [Autoevaluación](#9-autoevaluación)

---

## 1. Datos, información y representación

Los datos son representaciones informáticas de hechos de interés. La información aparece cuando esos datos se interpretan dentro de un contexto. Por ejemplo, `2026-09-14` es un dato; asociado a una matrícula puede informar de la fecha de alta de un alumno.

El diseño parte del mundo real, lo transforma en un modelo conceptual y, finalmente, lo representa mediante estructuras que puede almacenar un SGBD. Elegir correctamente los atributos y sus tipos es importante: guardar una fecha como texto dificulta ordenar, filtrar por intervalos o comprobar su validez.

Una representación tabular organiza datos en filas y columnas. Cada fila describe una ocurrencia, como un cliente, y cada columna describe una propiedad, como su nombre o correo. Cuando varias tablas comparten información se utilizan claves para mantener las relaciones sin repetir datos innecesariamente.

### Ejemplo 1.1

Una biblioteca puede representar a sus socios con una tabla `Socio(id_socio, nombre, email)`. El identificador permite distinguir a dos personas llamadas igual y el tipo de dato de `email` puede incluir una regla de validación apropiada.

## 2. Bases de datos y sistemas gestores

Una base de datos es un conjunto organizado de datos relacionados. Un sistema gestor de bases de datos, o SGBD, es el software que permite definir, consultar, modificar, proteger y recuperar esa información. MySQL, MariaDB, PostgreSQL, Oracle y SQL Server son ejemplos de SGBD.

Frente a los ficheros independientes, un SGBD reduce redundancia, centraliza reglas, permite acceso simultáneo, controla permisos y facilita copias de seguridad. Los ficheros siguen siendo adecuados para datos simples o intercambios puntuales, pero resultan difíciles de mantener cuando varias aplicaciones necesitan modificar información común.

Un SGBD ofrece una visión abstracta: las aplicaciones usan tablas, consultas y vistas sin necesitar conocer páginas de disco, índices o archivos internos. Esta separación hace posible mejorar el almacenamiento sin modificar necesariamente los programas que trabajan con los datos.

### Ejemplo 2.1

Un supermercado mantiene productos, ventas y stock. Cuando se registra una venta, el SGBD guarda el ticket, reduce existencias y conserva el historial. Sin transacciones, un fallo entre ambas operaciones podría registrar la venta sin actualizar el stock.

## 3. Arquitectura y componentes de un SGBD

La arquitectura ANSI/SPARC distingue tres niveles. El nivel externo contiene vistas adaptadas a cada perfil; el nivel conceptual define entidades, relaciones y restricciones de toda la BD; y el nivel interno organiza físicamente datos, índices, páginas y archivos. Esta separación aporta independencia lógica y física.

El diccionario de datos almacena metadatos: tablas, columnas, tipos, índices, vistas, permisos y restricciones. El procesador de consultas analiza SQL, comprueba nombres y autorizaciones; el optimizador elige un plan de menor coste; y el gestor de almacenamiento recupera o actualiza páginas de datos.

El gestor de transacciones coordina operaciones concurrentes y los registros de recuperación permiten restaurar un estado consistente tras un fallo. Los usuarios finales trabajan mediante aplicaciones, los usuarios avanzados pueden formular SQL y los programadores construyen las aplicaciones; el DBA administra el conjunto.

### Ejemplo 3.1

Ante `SELECT nombre FROM alumno WHERE id_alumno = 25`, el SGBD valida la tabla y columna, verifica permisos y decide si usa un índice por `id_alumno` o recorre la tabla. La consulta no cambia aunque el DBA cree posteriormente ese índice.

## 4. Integridad, concurrencia y transacciones

La integridad garantiza que los datos cumplan reglas coherentes. Una clave primaria identifica cada fila y no admite duplicados; una clave foránea impide referencias a registros inexistentes; las restricciones de dominio validan valores como precios positivos o fechas válidas.

La concurrencia permite que varias personas usen la misma BD a la vez. Sin control pueden producirse lecturas inconsistentes, modificaciones perdidas o resultados parciales. Los SGBD emplean bloqueos, control de versiones y niveles de aislamiento para equilibrar coherencia y rendimiento.

Una transacción agrupa operaciones que deben ejecutarse como una unidad. Las propiedades ACID describen atomicidad, consistencia, aislamiento y durabilidad. `COMMIT` confirma los cambios y `ROLLBACK` los deshace cuando aparece un error.

### Ejemplo 4.1

Una transferencia de 100 euros requiere restar saldo de una cuenta y sumarlo a otra. Ambas operaciones deben confirmarse juntas. Si la segunda falla, un `ROLLBACK` evita que el dinero desaparezca de la primera cuenta.

## 5. Seguridad, recuperación y administración

La seguridad limita el acceso según usuarios, roles y operaciones permitidas. Un usuario de consulta no debe poder borrar tablas y una aplicación no debe conectarse con privilegios de administrador. Las vistas pueden ocultar columnas sensibles, como datos de contacto o salarios.

La confidencialidad puede reforzarse con cifrado en tránsito y en reposo, pero exige una gestión segura de claves. Las contraseñas nunca deben almacenarse en texto claro: se protegen con funciones de derivación de claves y sal aleatoria, no con cifrado reversible convencional.

Las copias de seguridad y los registros de transacciones permiten recuperar información, pero una copia solo es útil si se puede restaurar. El DBA debe planificar copias, probar recuperaciones, monitorizar espacio y rendimiento, aplicar actualizaciones y documentar cambios.

### Ejemplo 5.1

En una clínica, recepción puede consultar citas, el personal médico accede a historiales necesarios para atender al paciente y administración gestiona facturación. Ninguno de esos perfiles requiere privilegios para alterar el esquema de la base de datos.

## 6. Modelos, arquitecturas y lenguajes

El modelo relacional representa datos mediante tablas y relaciones entre ellas. Los modelos jerárquico y en red usan estructuras de enlaces; los modelos orientados a objetos trabajan con objetos; y NoSQL incluye documentos, grafos, clave-valor y columnas. La elección depende de consultas, consistencia, escala y requisitos del problema.

Las bases de datos pueden desplegarse de manera centralizada, cliente-servidor o distribuida. Un sistema distribuido puede acercar datos a distintos lugares y aumentar disponibilidad, pero requiere gestionar réplica, sincronización, latencia y posibles conflictos.

SQL es el lenguaje estándar más habitual en SGBD relacionales. DDL define estructuras con `CREATE`, `ALTER` o `DROP`; DML consulta y modifica datos con `SELECT`, `INSERT`, `UPDATE` y `DELETE`; y DCL administra permisos con `GRANT` y `REVOKE`.

### Ejemplo 6.1

```sql
CREATE TABLE producto (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) CHECK (precio >= 0)
);
```

La tabla aplica una clave primaria, obliga a informar el nombre y evita precios negativos.

## 7. Resumen

Las bases de datos representan información de interés y los SGBD proporcionan los mecanismos para definirla, consultarla, protegerla y recuperarla. La abstracción entre modelo, consultas y almacenamiento permite evolucionar una solución sin acoplar cada aplicación a sus detalles físicos.

Integridad, transacciones, concurrencia, permisos y copias de seguridad son responsabilidades esenciales de un SGBD. Un diseño correcto combina estructura coherente, reglas explícitas y administración continua.

## 8. Recursos

- [PostgreSQL: documentación](https://www.postgresql.org/docs/)
- [MariaDB: documentación](https://mariadb.com/kb/en/documentation/)
- [Oracle Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/)
- [SQLBolt](https://sqlbolt.com/)

## 9. Autoevaluación

1. ¿Qué diferencia existe entre dato e información?
2. ¿Qué problema resuelve un SGBD frente a ficheros independientes?
3. ¿Qué representan los niveles externo, conceptual e interno?
4. ¿Qué función tiene el diccionario de datos?
5. ¿Qué propiedades garantiza ACID?
6. ¿Por qué una copia de seguridad debe probarse mediante restauración?
7. ¿Qué diferencia hay entre DDL, DML y DCL?
