## Tareas de transformación: del E/R al modelo relacional

Las tareas de este apartado parten de un **diagrama EER ya hecho**, dibujado con la misma notación que el [banco de ejercicios de la UD02](/ud02-modelo-er/ud02-practicas#banco-de-ejercicios). Hay que obtener el **esquema relacional** y anotar las **pérdidas semánticas**: lo que el diagrama dice y las tablas no pueden garantizar por sí solas.

A diferencia del diagrama E/R, donde caben varias soluciones, la transformación de un diagrama dado es casi única. Los nombres de las claves ajenas pueden variar (`cod_emp`, `codigo_empleado`…), pero las **PK, FK, UK y VNN** tienen que ser las mismas.

### Notación del esquema

Cada tabla se escribe con sus columnas y, debajo, sus restricciones:

```text
CONTENEDOR (cod_contenedor, descripcion, dni_capitan, cod_puerto)
   PK:  cod_contenedor
   FK:  dni_capitan → CAPITAN
   FK:  cod_puerto  → PUERTO
   VNN: dni_capitan, cod_puerto
```

| Marca | Nombre | ¿Admite duplicados? | ¿Admite nulos? |
|---|---|---|---|
| **PK** | Clave primaria | No | No |
| **UK** | Clave alternativa (*unique*) | No | No, si es clave candidata (se añade VNN) |
| **FK** | Clave ajena | Sí\* | Sí\* |
| **VNN** | Valor no nulo (*not null*) | — | No |

\* Salvo que la columna forme parte también de una PK o UK, o tenga VNN.

> [!TIP]
> Es la misma información que la notación `TABLA(`<u>clave</u>`, columna, `*clave_ajena*`)` de las prácticas anteriores, pero en forma de lista. Con ella es más fácil revisar que no falta ninguna restricción y, en la UD05, cada línea se convierte casi directamente en una cláusula de `CREATE TABLE`.

### Reglas de transformación (resumen)

| Elemento del E/R | Resultado en el modelo relacional |
|---|---|
| Entidad fuerte | Tabla. El identificador pasa a PK; las claves alternativas, a UK. |
| Entidad débil por identificación (**ID**) | Tabla. PK = PK de la entidad propietaria + discriminador. La parte heredada es también FK. |
| Entidad débil por existencia (**E**) | Tabla con PK propia. La FK hacia la propietaria lleva **VNN**. |
| Relación 1:N | La PK del lado 1 viaja como **FK** a la tabla del lado N, con los atributos de la relación. Si el lado N no puede existir sin el otro (mínimo 1), la FK lleva **VNN**. |
| Relación N:M | **Tabla nueva**. PK = las dos claves (más el atributo que permita repetir la pareja, si lo hay). Cada clave es FK. |
| 1:1 con (0,1) y (0,1) | **Tabla nueva**: PK = clave de una entidad; UK = clave de la otra. |
| 1:1 con (0,1) y (1,1) | Se propaga la clave a la tabla de la entidad que participa obligatoriamente, con **UK** y **VNN**. |
| 1:1 con (1,1) y (1,1) | **Una sola tabla**: PK = clave de una entidad; UK = clave de la otra. |
| Reflexiva | Igual que la binaria del mismo tipo, con la misma tabla en los dos extremos (columnas renombradas). |
| Ternaria N:N:N | Tabla con las tres claves como PK. |
| Ternaria 1:N:N | PK = claves de los dos lados N; la del lado 1, con **VNN**. |
| Ternaria 1:1:N | PK = clave del lado N + una de las de lado 1; la otra combinación, **UK**. |
| Generalización | Tabla para la superclase y una por subclase, con la PK de la superclase como PK y FK. Total y disjunta **no se pueden** expresar: son pérdidas. |
| Agregación | La relación agregada se trata como una tabla más; su clave es la que la identifica. |
| Atributo multivaluado | Tabla nueva con la PK de la entidad y el valor. |

> [!IMPORTANT]
> **Pérdidas semánticas habituales.** Las claves no pueden garantizar: el mínimo 1 del lado 1 de una relación 1:N («todo profesor imparte al menos un módulo»), la existencia de una entidad respecto a una relación cuando están en tablas distintas, las generalizaciones totales o disjuntas y las restricciones entre relaciones («C solo se relaciona con D si lo está con B»). Se anotan y se resuelven en la implementación con `CHECK`, disparadores (UD09) o procedimientos.

---

## Práctica 3.6 · Entender un esquema relacional

{{< practica num="3.6" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA6: b, c, d" sgbd="Papel" entrega="Hoja de respuestas" >}}

#### Objetivo

Hacer el camino inverso: a partir de unas tablas con sus restricciones, **deducir las cardinalidades** de la relación que representan.

#### Contexto

Antes de transformar diagramas conviene saber «leer» un esquema. Cada restricción (PK, UK, FK, VNN) responde a una pregunta sobre la relación: ¿puede repetirse?, ¿puede faltar?

#### Desarrollo

El juego consiste en responder a cuatro preguntas usando la tabla de la notación (duplicados y nulos). Primero, un caso abstracto:

```text
T1 (A, B, C)          T2 (E, F)
   PK: A                 PK: E
                         FK: F → T1
```

- ¿Con cuántas filas de `T2` puede relacionarse una fila de `T1`? El valor de `A` puede aparecer en la columna `F` de **muchas** filas de `T2` (una FK admite duplicados), o de ninguna: **(0,N)**.
- ¿Con cuántas filas de `T1` se relaciona una fila de `T2`? `F` guarda **un único** valor y puede ser nulo (la FK admite nulos): **(0,1)**.

Ahora, la relación entre alumnos y asignaturas («los alumnos se matriculan de asignaturas»). Para cada esquema responde a:

1. ¿De cuántas asignaturas puede matricularse un alumno?
2. ¿Está obligado el alumno a matricularse de alguna asignatura?
3. ¿Cuántos alumnos puede tener una asignatura?
4. ¿Es necesario que las asignaturas tengan alumnos?

| Caso | Esquema |
|---|---|
| A | `ASIGNATURA (codigo, nombre, curso)` PK: codigo · `ALUMNO (dni, nombre, asig)` PK: dni · FK: asig → ASIGNATURA |
| B | Igual que A, añadiendo **VNN: asig** |
| C | `ALUMNO (dni, nombre)` PK: dni · `ASIGNATURA (codigo, nombre, curso, dni)` PK: codigo · UK: dni · FK: dni → ALUMNO |
| D | `ALUMNO (dni, nombre)` PK: dni · `ASIGNATURA (codigo, nombre, curso)` PK: codigo · `MATRICULA (dni, asig)` PK: (dni, asig) · FK: dni → ALUMNO · FK: asig → ASIGNATURA |
| E | Igual que D, pero con **PK: dni** en `MATRICULA` |
| F | `ASIGNATURA (codigo, nombre, curso, dni, nombre_alumno)` PK: codigo · UK: dni · VNN: dni (no hay tabla `ALUMNO`) |

{{% details title="Solución (inténtalo antes de abrirla)" %}}
| Caso | 1. Asignaturas por alumno | 2. ¿Obligado? | 3. Alumnos por asignatura | 4. ¿Necesario? | Relación |
|---|---|---|---|---|---|
| A | Una (`asig` guarda un valor) | No (`asig` admite nulos) | Muchos (FK admite duplicados) | No | 1:N · (0,1) y (0,N) |
| B | Una | **Sí** (VNN) | Muchos | No | 1:N · (1,1) y (0,N) |
| C | Una (UK: el dni no se repite) | No | Uno (la columna guarda un valor) | No (`dni` admite nulos) | 1:1 · (0,1) y (0,1) |
| D | Varias | No | Muchos | No | N:M · (0,N) y (0,N) |
| E | Una (el dni no se repite en `MATRICULA`) | No | Muchos | No | 1:N con tabla propia · (0,1) y (0,N) |
| F | Una | Sí | Uno | Sí | 1:1 · (1,1) y (1,1), fusionada en una tabla |

Fíjate en que **ninguna** combinación de PK, UK, FK y VNN obliga a que una asignatura tenga alumnos (pregunta 4) cuando están en tablas distintas: es una pérdida semántica típica.
{{% /details %}}

#### Comprobación

- [ ] Para cada caso has escrito las cuatro respuestas y la cardinalidad (mín, máx) de cada lado.
- [ ] Has relacionado cada respuesta con una restricción concreta (PK, UK, FK o VNN).

#### Errores habituales

> [!WARNING]
> - Pensar que una FK no admite duplicados. Lo que no se repite es la **PK** de la tabla referenciada, no la columna que la referencia.
> - Confundir el caso E con el D: una tabla intermedia no implica siempre N:M; depende de su clave primaria.

#### Ampliación

Escribe el esquema que corresponde a «un alumno se matricula de **una o varias** asignaturas y una asignatura tiene **como máximo 30** alumnos». ¿Qué parte puedes expresar con PK, UK, FK y VNN y qué parte queda como pérdida semántica?

---

### Tarea 1 · Naviera: capitanes, contenedores, puertos y barcos

{{< practica num="1" etiqueta="Tarea" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA6: b, c, d, e" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar relaciones 1:N con participación obligatoria y una N:M que guarda un histórico.

#### Contexto

Es el diagrama del [ejercicio 4 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-4--naviera-capitanes-contenedores-puertos-y-barcos).

{{< figura src="ud02/ej04.svg" alt="CAPITÁN transporta CONTENEDOR (1:N), CONTENEDOR llega a PUERTO (N:1), CAPITÁN gobierna BARCO (N:M con fecha_inicio y fecha_fin)" caption="Diagrama de partida: naviera" >}}

#### Enunciado

Obtén el esquema relacional del diagrama, indicando para cada tabla su PK, sus FK, sus UK y las columnas con VNN. Anota las pérdidas semánticas.

#### Tareas

1. Escribe una tabla por entidad.
2. Decide dónde van las claves de *transporta* y *llega a*. ¿Llevan VNN?
3. Convierte *gobierna* en tabla. ¿Qué columnas forman su PK? ¿Por qué no basta con (capitán, barco)?
4. Lista las pérdidas semánticas.

#### Comprobación

- [ ] Hay 5 tablas.
- [ ] `CONTENEDOR` tiene dos FK, ambas con VNN.
- [ ] La PK de `GOBIERNA` incluye `fecha_inicio`.

#### Errores habituales

> [!WARNING]
> - Crear una tabla para cada relación 1:N. Solo las N:M (y algunas 1:1) generan tabla nueva.
> - Dejar la PK de `GOBIERNA` en (dni, matrícula): impediría que un capitán vuelva a gobernar el mismo barco.

{{% details title="Solución" %}}
```text
CAPITAN (dni, nombre, telefono, direccion, salario, poblacion)
   PK:  dni

BARCO (matricula, nombre, potencia_motor, astillero)
   PK:  matricula

PUERTO (cod_puerto, nombre)
   PK:  cod_puerto

CONTENEDOR (cod_contenedor, descripcion, dir_remitente, dir_destinatario, dni_capitan, cod_puerto)
   PK:  cod_contenedor
   FK:  dni_capitan → CAPITAN
   FK:  cod_puerto  → PUERTO
   VNN: dni_capitan, cod_puerto

GOBIERNA (dni_capitan, matricula, fecha_inicio, fecha_fin)
   PK:  (dni_capitan, matricula, fecha_inicio)
   FK:  dni_capitan → CAPITAN
   FK:  matricula   → BARCO
```

**Pérdidas semánticas**

- Un capitán no gobierna dos barcos a la vez (periodos solapados): se controlará con un disparador.
- `fecha_fin` posterior a `fecha_inicio`: no es una pérdida, se resuelve con `CHECK` en la UD05.

> [!NOTE]
> En la solución del curso anterior la PK de `GOBIERNA` era (nombre_barco, dni_capitán) y el barco se identificaba por el nombre. Con la fecha en la clave se conserva el histórico; y la matrícula es mejor identificador que el nombre, que puede repetirse.
{{% /details %}}

#### Ampliación

La naviera quiere saber en qué **barco** viaja cada contenedor. Añade la relación al diagrama y transforma solo la parte que cambia.

---

### Tarea 2 · Instituto: módulos, matrículas, delegados y casilleros

{{< practica num="2" etiqueta="Tarea" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar dos relaciones reflexivas (1:N y N:M) y una 1:1 con mínimos 0 en los dos lados.

#### Contexto

Es el diagrama del [ejercicio 6 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-6--instituto-módulos-matrículas-delegados-y-casilleros).

{{< figura src="ud02/ej06.svg" alt="PROFESOR imparte MÓDULO; MÓDULO es requisito de MÓDULO; ALUMNO se matricula en MÓDULO; ALUMNO es delegado de ALUMNO; ALUMNO tiene CASILLERO" caption="Diagrama de partida: instituto" >}}

#### Enunciado

Obtén el esquema relacional completo con PK, FK, UK y VNN, y anota las pérdidas semánticas.

#### Tareas

1. Transforma las entidades y la relación *imparte*.
2. Transforma las dos reflexivas. ¿Cuál necesita tabla propia y cuál no?
3. Transforma *tiene* aplicando la regla de la 1:1 con (0,1) y (0,1).
4. Lista las pérdidas semánticas.

#### Comprobación

- [ ] Hay 7 tablas.
- [ ] El delegado es una FK de `ALUMNO` a la propia tabla `ALUMNO`.
- [ ] `TIENE` tiene una PK y una UK.

#### Errores habituales

> [!WARNING]
> - Poner `fecha_matricula` en `ALUMNO` (en la solución antigua aparecía en las dos tablas). Solo va en `MATRICULA`.
> - Usar el mismo nombre de columna para los dos módulos de `ES_REQUISITO`.

{{% details title="Solución" %}}
```text
PROFESOR (dni, nombre, direccion, telefono)
   PK:  dni

MODULO (codigo, nombre, dni_profesor)
   PK:  codigo
   FK:  dni_profesor → PROFESOR
   VNN: dni_profesor

ES_REQUISITO (cod_previo, cod_posterior)
   PK:  (cod_previo, cod_posterior)
   FK:  cod_previo    → MODULO
   FK:  cod_posterior → MODULO

ALUMNO (n_expediente, nombre, apellidos, fecha_nacimiento, curso, exp_delegado)
   PK:  n_expediente
   FK:  exp_delegado → ALUMNO

MATRICULA (n_expediente, cod_modulo, fecha_matricula)
   PK:  (n_expediente, cod_modulo)
   FK:  n_expediente → ALUMNO
   FK:  cod_modulo   → MODULO

CASILLERO (n_casillero, tamano_m)
   PK:  n_casillero

TIENE (n_expediente, n_casillero)
   PK:  n_expediente
   UK:  n_casillero
   VNN: n_casillero
   FK:  n_expediente → ALUMNO
   FK:  n_casillero  → CASILLERO
```

**Pérdidas semánticas**

- Todo profesor imparte al menos un módulo y todo alumno está matriculado de al menos uno: el mínimo 1 del lado 1 no se puede garantizar con claves.
- El delegado y sus representados son del mismo curso.
- Un módulo no puede ser requisito de sí mismo ni formar ciclos (el primer caso se resuelve con `CHECK (cod_previo <> cod_posterior)`).

> [!TIP]
> Alternativa también correcta: guardar `n_casillero` en `ALUMNO` con UK (admite nulos). Evita una tabla, pero deja nulos en los alumnos sin casillero. La regla de la 1:1 con (0,1) y (0,1) prefiere la tabla propia para no tener nulos.
{{% /details %}}

#### Ampliación

Un alumno puede repetir y matricularse **dos veces** del mismo módulo en cursos distintos. ¿Qué cambia en `MATRICULA`?

---

### Tarea 3 · Concesionario: ventas, revisiones y mecánicos

{{< practica num="3" etiqueta="Tarea" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA6: b, c, d, e" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar una entidad débil por identificación, una reflexiva 1:N y claves alternativas.

#### Contexto

Es el diagrama del [ejercicio 10 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-10--concesionario-ventas-revisiones-y-mecánicos).

{{< figura src="ud02/ej10.svg" alt="CLIENTE compra COCHE (1:N), COCHE pasa REVISIÓN (débil, ID), MECÁNICO realiza REVISIÓN, MECÁNICO supervisa a MECÁNICO" caption="Diagrama de partida: concesionario" >}}

#### Enunciado

Obtén el esquema relacional con PK, FK, UK y VNN. Indica qué columnas de `REVISION` son a la vez PK y FK.

#### Comprobación

- [ ] La PK de `REVISION` es compuesta e incluye la matrícula.
- [ ] `nif` y `dni` son UK.
- [ ] La FK del cliente en `COCHE` admite nulos (coche sin vender).

#### Errores habituales

> [!WARNING]
> - Escribir `PK (codigo, matricula)` sin marcar `matricula` como FK.
> - Poner VNN en `cod_cliente` de `COCHE`: el diagrama dice (0,1), un coche puede estar sin vender.

{{% details title="Solución" %}}
```text
CLIENTE (cod_cliente, nif, nombre, direccion, ciudad, telefono)
   PK:  cod_cliente
   UK:  nif
   VNN: nif

COCHE (matricula, marca, modelo, color, precio_venta, cod_cliente)
   PK:  matricula
   FK:  cod_cliente → CLIENTE

MECANICO (cod_empleado, dni, nombre, telefono, direccion, cod_supervisor)
   PK:  cod_empleado
   UK:  dni
   VNN: dni
   FK:  cod_supervisor → MECANICO

REVISION (matricula, n_revision, cambio_filtro, cambio_aceite, cambio_frenos, otros, cod_mecanico)
   PK:  (matricula, n_revision)
   FK:  matricula    → COCHE
   FK:  cod_mecanico → MECANICO
   VNN: cod_mecanico
```

**Pérdidas semánticas**

- Un mecánico no puede supervisarse a sí mismo: `CHECK (cod_supervisor <> cod_empleado)`.
- No puede haber ciclos de supervisión (A supervisa a B y B a A): disparador.
{{% /details %}}

#### Ampliación

El taller guarda **qué piezas** se cambian en cada revisión y cuántas. Añade la entidad `PIEZA` y transforma la nueva relación. ¿Cuántas columnas tiene la PK de la tabla nueva?

---

### Tarea 4 · Casas rurales

{{< practica num="4" etiqueta="Tarea" tipo="Autónoma" duracion="1-2 sesiones" nivel="2" ra="RA6: b, c, d, e" sgbd="Papel" entrega="Dos esquemas relacionales + pérdidas semánticas" >}}

#### Objetivo

Transformar una cadena de entidades débiles con **claves ajenas compuestas** y distinguir la dependencia en identificación (ID) de la dependencia en existencia (E).

#### Contexto

El primer diagrama es el del [ejercicio 11 de la UD02](/ud02-modelo-er/ud02-practicas#ejercicio-11--casas-rurales-provincias-ciudades-y-habitaciones). El segundo es la variante de su ampliación.

{{< figura src="ud02/ej11.svg" alt="PROVINCIA tiene CIUDAD (débil). CASA_RURAL está en CIUDAD. CASA_RURAL dispone de HABITACIÓN (débil). CLIENTE se aloja en HABITACIÓN." caption="Diagrama 4.1: casas rurales" >}}

{{< figura src="ud03/tarea-rurales-b.svg" alt="PROVINCIA tiene CIUDAD (débil, ID). CASA depende en existencia de CIUDAD (E). PERSONA vive en CASA. PERSONA posee CASA con fecha de compra." caption="Diagrama 4.2: variante con residentes y propietarios" >}}

#### Enunciado

Obtén el esquema relacional de los dos diagramas.

#### Tareas

1. Escribe la PK de `CIUDAD`. ¿Cuántas columnas tiene la FK que la referencia desde `CASA_RURAL`?
2. Transforma `HABITACION` y la relación *se aloja*.
3. En el diagrama 4.2, ¿qué diferencia hay en el esquema entre la dependencia **ID** de `CIUDAD` y la **E** de `CASA`?

#### Comprobación

- [ ] Todas las FK que apuntan a `CIUDAD` tienen **dos** columnas.
- [ ] La PK de `SE_ALOJA` incluye la fecha de entrada.
- [ ] En 4.2, `CASA` tiene PK propia y su FK a `CIUDAD` lleva VNN.

#### Errores habituales

> [!WARNING]
> - Escribir `FK: nombre_ciudad → CIUDAD` con una sola columna. La FK debe apuntar a la PK **completa** (era el error de la solución antigua).
> - Incluir la ciudad en la PK de `CASA` en el diagrama 4.2: la dependencia es de existencia, no de identificación.

{{% details title="Solución" %}}
**Diagrama 4.1**

```text
PROVINCIA (nombre, area, poblacion)
   PK:  nombre

CIUDAD (nombre_provincia, nombre, habitantes)
   PK:  (nombre_provincia, nombre)
   FK:  nombre_provincia → PROVINCIA

CASA_RURAL (nombre, localizacion, desayuno, nombre_provincia, nombre_ciudad)
   PK:  nombre
   FK:  (nombre_provincia, nombre_ciudad) → CIUDAD
   VNN: nombre_provincia, nombre_ciudad

HABITACION (nombre_casa, numero, descripcion, precio)
   PK:  (nombre_casa, numero)
   FK:  nombre_casa → CASA_RURAL

CLIENTE (dni, nombre, direccion, telefono)
   PK:  dni

SE_ALOJA (dni, nombre_casa, numero, fecha_entrada, fecha_salida)
   PK:  (dni, nombre_casa, numero, fecha_entrada)
   FK:  dni → CLIENTE
   FK:  (nombre_casa, numero) → HABITACION
```

**Diagrama 4.2**

```text
PROVINCIA (nombre)
   PK:  nombre

CIUDAD (nombre_provincia, nombre)
   PK:  (nombre_provincia, nombre)
   FK:  nombre_provincia → PROVINCIA

CASA (id_casa, precio, valoracion, nombre_provincia, nombre_ciudad)
   PK:  id_casa
   FK:  (nombre_provincia, nombre_ciudad) → CIUDAD
   VNN: nombre_provincia, nombre_ciudad

PERSONA (id_persona, nombre, id_casa_vive)
   PK:  id_persona
   FK:  id_casa_vive → CASA

POSEE (id_casa, id_persona, fecha_compra)
   PK:  (id_casa, id_persona)
   FK:  id_casa    → CASA
   FK:  id_persona → PERSONA
```

**Pérdidas semánticas**

- Toda provincia tiene al menos una ciudad y toda casa rural al menos una habitación (mínimo 1 del lado 1).
- Toda casa tiene al menos un propietario: no se puede obligar a que exista una fila en `POSEE`.
- En 4.1, la fecha de salida posterior a la de entrada y que no haya estancias solapadas en la misma habitación (disparador).

> [!NOTE]
> **ID frente a E.** Las dos dependencias producen una FK con VNN; la diferencia es que con **ID** la FK forma parte de la PK y con **E** no.
{{% /details %}}

#### Ampliación

Un cliente quiere reservar **varias habitaciones** con una sola reserva (número de reserva, fecha y forma de pago). Rediseña la parte del E/R afectada y transfórmala.

---

### Tarea 5 · Esquema abstracto 1: ternaria 1:1:N y agregación

{{< practica num="5" etiqueta="Tarea" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Aplicar las reglas a un esquema sin significado (letras), donde solo cuentan la estructura y las cardinalidades.

#### Contexto

Los esquemas abstractos obligan a aplicar las reglas sin apoyarse en el sentido común del enunciado. Los atributos subrayados son identificadores; `a0` es el discriminador de la entidad débil `A`.

{{< figura src="ud03/tarea-abstracto-1.svg" alt="A débil de C por R1 (ID), reflexiva R3 sobre A, F y G especializan A (P,D), ternaria R2 entre A, D y E (1:1:N), agregación de C-R4-B relacionada con D por R5" caption="Esquema abstracto 1" >}}

#### Enunciado

Obtén el esquema lógico relacional y enuncia las **pérdidas semánticas**.

#### Tareas

1. ¿Cuál es la PK de `A`? ¿Y la de `F` y `G`?
2. ¿Qué clave identifica a la agregación? Transforma *R5*.
3. Transforma la ternaria *R2* (1 junto a `A`, 1 junto a `D`, N junto a `E`): PK y UK.
4. Enuncia las pérdidas.

#### Comprobación

- [ ] Todas las FK hacia `A` tienen dos columnas.
- [ ] `R2` tiene PK y UK distintas.
- [ ] Has anotado que no se capta que la generalización sea disjunta.

{{% details title="Solución" %}}
```text
B (b0, b1)
   PK:  b0

D (d0, d1)
   PK:  d0

E (e0, e1)
   PK:  e0

C (c0, c1, cB, cD)
   PK:  c0
   FK:  cB → B          (R4: C es el lado N)
   FK:  cD → D          (R5: la agregación se identifica por C, porque R4 es 1:N)

A (aC, a0, a1, aA_C, aA_0)
   PK:  (aC, a0)
   FK:  aC → C
   FK:  (aA_C, aA_0) → A          (R3)

F (fC, f0A, f0)
   PK:  (fC, f0A)
   FK:  (fC, f0A) → A

G (gC, g0)
   PK:  (gC, g0)
   FK:  (gC, g0) → A

R2 (rD, rE, rA_C, rA_0)
   PK:  (rD, rE)
   UK:  (rA_C, rA_0, rE)
   FK:  rD → D
   FK:  rE → E
   FK:  (rA_C, rA_0) → A
```

**Pérdidas semánticas**

- No se capta que la generalización sea **disjunta**: un mismo `A` podría estar en `F` y en `G`.
- No se capta que `C` solo pueda relacionarse con `D` (R5) si lo está con `B` (R4). En SQL se resuelve con `CHECK (cD IS NULL OR cB IS NOT NULL)`.

> [!NOTE]
> La ternaria 1:1:N da dos claves candidatas: por cada pareja (D, E) hay un único `A`, y por cada pareja (A, E) hay un único `D`. Una se elige como PK y la otra queda como UK.
{{% /details %}}

---

### Tarea 6 · Esquema abstracto 2: agregación con relación 1:1 y existencia

{{< practica num="6" etiqueta="Tarea" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar una agregación de una N:M, una 1:1 con atributo y dependencia en existencia, una ternaria 1:N:N y una reflexiva sobre una subclase.

{{< figura src="ud03/tarea-abstracto-2.svg" alt="A débil de C (R1, ID); F y E especializan A (P,D); R2 reflexiva 1:N sobre F; R3 N:M entre F y E; agregación de C-R4-D (N:M, D depende en existencia de R4) relacionada 1:1 con A por R5 (atributo m, E); ternaria R6 entre C, D y B (1:N:N)" caption="Esquema abstracto 2" >}}

#### Enunciado

Obtén el esquema lógico relacional y enuncia las pérdidas semánticas.

#### Tareas

1. Transforma la agregación: como *R4* es N:M, su tabla es la que representa la agregación.
2. Coloca *R5* (1:1, atributo `m`, la agregación depende en existencia de *R5*).
3. Transforma *R6* (1 junto a `C`).

#### Comprobación

- [ ] La tabla `R4` lleva la clave de `A`, el atributo `m`, una UK y VNN.
- [ ] `R6` tiene PK de dos columnas y la tercera con VNN.

{{% details title="Solución" %}}
```text
B (b0, b1)
   PK:  b0

C (c0, c1)
   PK:  c0

D (d0, d1)
   PK:  d0

A (aC, a0, a1)
   PK:  (aC, a0)
   FK:  aC → C

F (fC, f0A, f0, fP_C, fP_0)
   PK:  (fC, f0A)
   FK:  (fC, f0A) → A
   FK:  (fP_C, fP_0) → F           (R2)

E (eC, e0A, e0, e1)
   PK:  (eC, e0A)
   FK:  (eC, e0A) → A

R3 (rF_C, rF_0, rE_C, rE_0)
   PK:  (rF_C, rF_0, rE_C, rE_0)
   FK:  (rF_C, rF_0) → F
   FK:  (rE_C, rE_0) → E

R4 (rC, rD, rA_C, rA_0, m)
   PK:  (rC, rD)
   UK:  (rA_C, rA_0)
   VNN: rA_C, rA_0                  (la agregación depende en existencia de R5)
   FK:  rC → C
   FK:  rD → D
   FK:  (rA_C, rA_0) → A

R6 (rB, rD, rC)
   PK:  (rB, rD)
   VNN: rC
   FK:  rB → B
   FK:  rC → C
   FK:  rD → D
```

**Pérdidas semánticas**

- No se capta que la generalización sea **disjunta**.
- No se capta la dependencia en existencia de `D` respecto a *R4*: no se puede obligar a que cada fila de `D` aparezca en `R4`.
{{% /details %}}

---

### Tarea 7 · Esquema abstracto 3: ternaria con una entidad repetida

{{< practica num="7" etiqueta="Tarea" tipo="Reto" duracion="1-2 sesiones" nivel="3" ra="RA6: b, c, d, e, h" sgbd="Papel" entrega="Esquema relacional + pérdidas semánticas" >}}

#### Objetivo

Transformar una ternaria en la que una entidad participa dos veces, una 1:1 con (0,1) en los dos lados y una generalización total y solapada.

{{< figura src="ud03/tarea-abstracto-3.svg" alt="G débil de B (R5, ID); R6 1:1 G-H; agregación C-R4-D (C N, D 1) relacionada con G por R3 (atributo m, E) y N:M con F por R2; F y E especializan A (T,S); R1 ternaria F-F-E" caption="Esquema abstracto 3" >}}

#### Enunciado

Obtén el esquema lógico relacional y enuncia las pérdidas semánticas. En *R1*, `F` aparece dos veces: llama **F1** al extremo con N y **F2** al extremo con 1.

#### Tareas

1. ¿Qué clave identifica a la agregación si *R4* es 1:N?
2. Transforma *R3* (G con 1, la agregación con N y dependencia en existencia).
3. Transforma *R6* con la regla de la 1:1 con mínimos 0.
4. Transforma *R1* (F1: N, F2: 1, E: 1).

#### Comprobación

- [ ] La agregación queda representada por la tabla `C`.
- [ ] `R6` tiene PK de una columna y UK de dos.
- [ ] `R1` tiene PK (F1, F2) y UK (F1, E).

{{% details title="Solución" %}}
```text
B (b0, b1)
   PK:  b0

G (gB, g0, g1)
   PK:  (gB, g0)
   FK:  gB → B

H (h0, h1)
   PK:  h0

R6 (rH, rG_B, rG_0)
   PK:  rH
   UK:  (rG_B, rG_0)
   VNN: rG_B, rG_0
   FK:  rH → H
   FK:  (rG_B, rG_0) → G

D (d0, d1)
   PK:  d0

C (c0, c1, cD, cG_B, cG_0, m)
   PK:  c0
   FK:  cD → D                      (R4)
   FK:  (cG_B, cG_0) → G            (R3, con el atributo m)

A (a0, a1)
   PK:  a0

F (fA, f0)
   PK:  fA
   FK:  fA → A

E (eA, e0, e1)
   PK:  eA
   FK:  eA → A

R2 (rC, rF)
   PK:  (rC, rF)
   FK:  rC → C
   FK:  rF → F

R1 (rF1, rF2, rE)
   PK:  (rF1, rF2)
   UK:  (rF1, rE)
   VNN: rE
   FK:  rF1 → F
   FK:  rF2 → F
   FK:  rE  → E
```

**Pérdidas semánticas**

- No se capta que la generalización sea **total**: puede haber un `A` que no esté ni en `F` ni en `E`.
- No se capta que `C` solo pueda relacionarse con `G` (R3) o con `F` (R2) si está en la agregación, es decir, si tiene `D` (R4). Para *R3* basta `CHECK (cG_B IS NULL OR cD IS NOT NULL)`; para *R2* hace falta un disparador.
- No se capta la dependencia en existencia de la agregación respecto a *R3*: toda pareja (C, D) debería tener `G` (`CHECK (cD IS NULL OR cG_B IS NOT NULL)`).

> [!TIP]
> Comprueba la ternaria con datos: si (f1, f2) determina e, y (f1, e) determina f2, las dos combinaciones son claves candidatas. Elige una como PK y deja la otra como UK.
{{% /details %}}
