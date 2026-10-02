---
title: "1. Introducción"
weight: 1
---
## Resumen del tema
---

**Visión general:**  

- ¿Qué es y para qué sirve un SGBD? — Sistema que centraliza, organiza y protege datos para facilitar su acceso y gestión.  
- Ventajas principales: integridad, concurrencia, seguridad y reducción de redundancia.  
- Contextos habituales: comercios, bancos, hospitales y aplicaciones web.

_(Nota: este resumen ayuda a situar el contenido antes de entrar en definiciones y ejemplos técnicos.)_

`Ejemplo de campo monoespaciado`: nombre_usuario

Ejemplo de bloque de código SQL:

```sql
-- Crear tabla de ejemplo: clientes
CREATE TABLE Clientes (
	id INT PRIMARY KEY,
	nombre VARCHAR(100),
	direccion VARCHAR(200),
	localidad VARCHAR(50)
);

-- Insertar un registro de ejemplo
INSERT INTO Clientes (id, nombre, direccion, localidad)
VALUES (1, 'María Pérez', 'C/ Mayor, 10', 'Valencia');
```

> "Un buen diseño de datos evita muchos problemas posteriores." — consejo práctico

![Visión general SGBD](images/sgbd-overview.svg)

![Tipos de archivos](images/file-types.svg)

![Métodos de acceso](images/access-methods.svg)

![Ejemplo ER](images/er-example.svg)

<a id="resumen-del-tema"></a>

# Tema 0 — Sistemas de Almacenamiento

## Índice
- [1.1 Introducción](#11-introducción)
- [1.1.1 Historia y evolución de las bases de datos](#111-historia-y-evolución-de-las-bases-de-datos)
- [1.2 Sistemas basados en archivos](#12-sistemas-basados-en-archivos)
	- [1.2.1 ¿Qué es un archivo?](#122-qué-es-un-archivo)
	- [1.2.2 Tipos de archivos](#122-tipos-de-archivos)
		- [1.2.2.1 Archivos secuenciales](#1221-archivos-secuenciales)
		- [1.2.2.2 Archivos de acceso aleatorio](#1222-archivos-de-acceso-aleatorio)
		- [1.2.2.3 Archivos indexados](#1223-archivos-indexados)
	- [1.2.3 Cómo se almacenaba la información antes de los SGBD](#123-cómo-se-almacenaba-la-información-antes-de-los-sgbd)
	- [1.2.4 Inconvenientes de un sistema de gestión de archivos](#124-inconvenientes-de-un-sistema-de-gestión-de-archivos)
- [Ejemplos de la vida real](#ejemplos-de-la-vida-real)
- [Tips de autoevaluación](#tips-de-autoevaluación)

 
<div style="page-break-before: always;"></div>

## 1.1 Introducción
Las bases de datos se utilizan cuando el volumen de datos a manipular es muy alto y se requiere un tiempo de respuesta reducido.
Por lo tanto, es importante optimizar dos aspectos: la forma en que se almacenan los datos y la manera en que se consultan.
El uso de sistemas de gestión de bases de datos (SGBD) incrementa la eficiencia de las operaciones en la empresa y reduce los costes. Además ofrece ventajas como control de concurrencia, seguridad mejorada, integridad y respaldo/recuperación.

Hoy en día prácticamente todas las empresas usan bases de datos. Por ejemplo, cuando compras en un supermercado intervienen varias bases de datos:
- El código de barras se consulta para obtener la descripción del artículo y su precio.
- La base de datos del almacén actualiza la cantidad disponible del producto.
- Si pagas con tarjeta, la pasarela de pago consulta la base de datos bancaria para debitar el importe.

## 1.1.1 Historia y evolución de las bases de datos
- Antigüedad: los humanos han almacenado información desde siempre; muchos principios de organización de datos actuales derivan de prácticas antiguas en bibliotecas, oficinas y censos.
- 1884: Herman Hollerith desarrolló una máquina perforadora para procesar censos, reduciendo drásticamente el tiempo de cálculo. Consistía en tarjetas perforadas y dispositivos lectoras.
- Años 50: aparición de la cinta magnética; se automatizó la gestión de nóminas y otros procesos con sistemas de archivos secuenciales.
- Años 60: el uso de discos permitió accesos aleatorios e indexados. Surgieron modelos de datos como el modelo en red (CODASYL) y el modelo jerárquico (IMS). Un sistema representativo de la época fue SABRE, usado por American Airlines para gestionar reservas.
- 1970–1972: E. F. Codd publicó trabajos clave proponiendo el modelo relacional, separando la organización lógica de los datos de su almacenamiento físico.
- 1974–1977: aparecieron prototipos y productos relacionales como Ingres y System R; de estos proyectos surgieron productos comerciales y el estándar SQL.
- 1976: Peter Chen propuso el modelo Entidad-Relación (ER) para facilitar el diseño lógico centrado en la aplicación.
- Años 80: SQL se consolidó como lenguaje estándar; proliferaron productos comerciales y herramientas de desarrollo.
- Años 90 y 2000: crecimiento de cliente-servidor, herramientas de desarrollo, Internet y soluciones de código abierto (MySQL, Apache, etc.).

 
<div style="page-break-before: always;"></div>

## 1.2 Sistemas basados en archivos
Una base de datos es un conjunto de datos estructurados almacenados en un medio. En los ordenadores, estos datos se guardan en ficheros.
Antes de los SGBD, los primeros sistemas de bases de datos empleaban sistemas de archivos dependientes del sistema operativo (SO).

### 1.2.1 ¿Qué es un archivo?
Un archivo es una estructura de información creada por el sistema operativo para almacenar datos. Suelen disponer de un nombre y una extensión (por ejemplo: documento.html).
Muchos sistemas determinan el tipo de un archivo por su extensión: .html, .gif, .docx, etc. En los sistemas de archivos antiguos (por ejemplo MS‑DOS y primeras versiones de Windows) los nombres estaban limitados a 8 caracteres y una extensión de 3.

### 1.2.2 Tipos de archivos
Según su contenido:
- Configuración: .ini, .inf, .conf
- Código fuente: .sql, .c, .java
- Páginas web: .html, .php, .asp, .xml
- Imágenes: .jpg, .gif, .bmp
- Vídeo: .mpg, .mov, .avi
- Comprimidos: .zip, .gz, .rar, .tar
- Ejecutables: .exe, .com, .cgi

Según el acceso/organización:
- Archivos secuenciales
- Archivos de acceso aleatorio
- Archivos indexados

Acceso secuencial: los datos se almacenan y procesan en orden; para llegar a un elemento concreto hay que leer los anteriores.

Acceso aleatorio (directo): se accede directamente a la posición asignada a cada dato; permite procesar en cualquier orden.

#### 1.2.2.1 Archivos secuenciales
Fueron los primeros en aparecer; el medio físico típico eran las cintas magnéticas. Cada registro tenía campos fijos grabados sucesivamente. Eran muy útiles para procesos como impresión de etiquetas.

#### 1.2.2.2 Archivos de acceso aleatorio
Aparecen con disquetes y discos duros. Se puede acceder directamente a la posición deseada sin leer todo el archivo.
Posición = NumRegistro × LongitudRegistro

Ejemplo: un registro con codificación ANSI (1 byte por carácter):
- Nombre: 80 caracteres
- Dirección: 100 caracteres
- Localidad: 50 caracteres

Longitud = 230 bytes. El primer registro empieza en la posición 0, el segundo en 230, el tercero en 460, etc.

Características:
- Posicionamiento inmediato
- Registros de longitud fija
- Apertura para lectura y/o escritura
- Uso concurrente (limitado si no hay control)
- Borrado mediante llenado con ceros (puede dejar huecos)

#### 1.2.2.3 Archivos indexados
Utilizan un índice para acelerar los accesos. El índice guarda punteros a posiciones de registros, permitiendo búsquedas rápidas. Para organizar los índices se usan estructuras como árboles B o árboles binarios de búsqueda.

### 1.2.3 Cómo se almacenaba la información antes de los SGBD
Antes de los SGBD, la información se gestionaba con sistemas de archivos y cada aplicación mantenía sus propios ficheros y programas para gestionarlos.

Cada aplicación disponía de:
- Un conjunto de archivos de datos
- Un conjunto de programas que gestionaban esos archivos

Se usaban para nóminas, control de pedidos, mantenimiento de productos, etc. Los problemas aparecían cuando aumentaba el número de usuarios, las necesidades funcionales o la necesidad de interconectar programas.

### 1.2.4 Inconvenientes de un sistema de gestión de archivos
a) Redundancia e inconsistencia de datos: los mismos datos pueden repetirse en varios archivos con formatos distintos, aumentando costes y riesgo de inconsistencia.

b) Dependencia física-lógica: la estructura física de datos está codificada en los programas; cambiarla implica modificar y probar todos los programas afectados.

c) Dificultad para acceder y ampliar: nuevas consultas no previstas requieren codificación adicional.

d) Separación y aislamiento de los datos: los datos repartidos en distintos archivos dificultan la escritura de nuevos programas coherentes.

e) Problemas de atomicidad: asegurar que una operación compuesta se realice completamente o no se realice es complejo en sistemas de archivos.

f) Acceso concurrente complicado: varias actualizaciones simultáneas pueden provocar inconsistencias.

g) Dependencia del lenguaje: la definición de la estructura en el código provoca incompatibilidades entre archivos generados por distintos lenguajes.

h) Seguridad limitada: aplicar restricciones y controles resulta difícil cuando cada aplicación gestiona sus propios archivos.

i) Integridad de datos: imponer restricciones (por ejemplo, que una nota pertenezca a una asignatura existente) requiere código adicional y complica la gestión cuando las restricciones afectan a varios archivos.

Solución: surge la idea de separar los datos de los programas que los manipulan, permitiendo modificar la estructura de los datos sin cambiar las aplicaciones. Además, centralizar los datos en un repositorio único facilita la coherencia y la gestión: así emergen los SGBD.

 
<div style="page-break-before: always;"></div>

## Ejemplos de la vida real
- Supermercado: consulta de código de barras, actualización de stock, factura y pasarela de pago (TPV).
- Hospital: gestión de pacientes, historiales clínicos, citas y control de stock de medicamentos.
- Banco: cuentas, transacciones, conciliaciones y gestión de autorizaciones.
- Comercio electrónico: catálogo de productos, carrito de compras, pedidos, inventario y analítica de ventas.

 
<div style="page-break-before: always;"></div>

## Tips de autoevaluación
- ¿Puedes explicar en una frase por qué un SGBD es mejor que múltiples archivos planos?
- Describe un ejemplo práctico (supermercado o banco) indicando qué tablas y relaciones crearías.
- Identifica tres problemas que surgen con archivos secuenciales frente a archivos indexados.
- Ejercicio práctico: a partir del registro de ejemplo (Nombre, Dirección, Localidad) calcula la posición del registro número 10 si la longitud es 230 bytes.
- Práctica de diseño: dibuja un diagrama ER sencillo para una librería (Clientes, Libros, Préstamos) y define las claves primarias y foráneas.

---
