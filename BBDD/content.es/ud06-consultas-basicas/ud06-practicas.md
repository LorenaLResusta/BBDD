---
title: "Consultas sobre una tabla - Prácticas"
weight: 2
bookToc: true
---

# UD06 · Prácticas

{{< ra "RA3:a,b" "RA5:e" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [6.1 Primeras consultas y herramientas](#práctica-61--primeras-consultas-y-herramientas) | Guiada | ●○○ | RA3.a, RA3.b |
| [6.2 Consultas para secretaría](#práctica-62--consultas-para-secretaría) | Autónoma | ●●○ | RA3.b |
| [6.3 Laboratorio de valores nulos](#práctica-63--laboratorio-de-valores-nulos) | Guiada | ●●○ | RA3.b |
| [6.4 Funciones para informes](#práctica-64--funciones-para-informes) | Autónoma | ●●○ | RA3.b, RA5.e |
| [6.5 Validar datos con SQL](#práctica-65--validar-datos-con-sql) | Reto | ●●● | RA3.b, RA5.e |
| [Proyecto EduGest · UD06](#proyecto-edugest--ud06-consultas-del-día-a-día) | Proyecto | ●●○ | RA3.a, RA3.b |

> [!IMPORTANT]
> Todas las prácticas usan el esquema de referencia **EDUGEST** con los datos del [script 02](/guia/proyecto-edugest#4-scripts-descargables). Antes de empezar, ejecuta en tu sesión:
>
> ```sql
> ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';
> ```
>
> Si has modificado los datos en otras prácticas, vuelve a ejecutar los scripts 01 y 02 para que tus resultados coincidan con las soluciones.

---

## Práctica 6.1 · Primeras consultas y herramientas

{{< practica num="6.1" tipo="Guiada" duracion="1 sesión" nivel="1" ra="RA3: a, b" sgbd="Oracle 26ai · SQL Developer (o extensión de VS Code)" entrega="p6_1.sql + captura del generador de consultas" >}}

#### Objetivo

Conocer las herramientas de consulta (hoja de trabajo, generador de consultas, pestaña de datos) y escribir las primeras consultas sobre una tabla.

#### Desarrollo

{{% steps %}}

1. **Explora sin SQL.** En el navegador de conexiones, despliega *Tablas* → `MODULO` → pestaña *Datos*. Usa el filtro de la parte superior (escribe `cod_ciclo = 'DAW'`). Observa que la herramienta **genera** una condición SQL.

2. **Usa el generador de consultas.** Abre una hoja de trabajo, clic derecho → *Generador de consultas*. Arrastra la tabla `PROFESOR`, marca `NOMBRE`, `APELLIDOS` y `ESPECIALIDAD`, y añade el criterio `ID_DEPARTAMENTO = 1`. Pasa a la pestaña *SQL* y copia la consulta generada. Haz una captura.

3. **Escribe y ejecuta** cada consulta con `Ctrl+Intro`. Comprueba que el número de filas coincide.

    ```sql
    -- 1. Todos los grupos
    SELECT * FROM grupo;                                              -- 6 filas

    -- 2. Nombre y horas de los módulos de 2º de DAM
    SELECT nombre, horas FROM modulo WHERE cod_ciclo = 'DAM' AND curso = 2;   -- 5 filas

    -- 3. Grupos de tarde
    SELECT cod_grupo, cod_ciclo FROM grupo WHERE turno = 'T';         -- 2 filas

    -- 4. Profesorado ordenado por fecha de alta, del más antiguo al más reciente
    SELECT nombre, apellidos, fecha_alta FROM profesor ORDER BY fecha_alta;   -- 12 filas
    ```

4. **Ejecuta el script completo** con `F5` y compara: el resultado aparece como texto en la *Salida de script*, como en SQLcl.

5. **Exporta un resultado.** Clic derecho sobre la rejilla del resultado 4 → *Exportar* → formato CSV.

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las cuatro consultas devuelven 6, 5, 2 y 12 filas.
- [ ] La consulta del generador es equivalente a `SELECT nombre, apellidos, especialidad FROM profesor WHERE id_departamento = 1;` y devuelve 8 filas.
- [ ] Sabes explicar la diferencia entre ejecutar con `Ctrl+Intro` y con `F5`.
{{% /comprobacion %}}

---

## Práctica 6.2 · Consultas para secretaría

{{< practica num="6.2" tipo="Autónoma" duracion="3 sesiones" nivel="2" ra="RA3: b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_2.sql comentado" >}}

#### Objetivo

Resolver de forma autónoma consultas reales sobre una tabla combinando proyección, selección, ordenación, operadores y eliminación de duplicados.

#### Contexto

Secretaría necesita respuestas rápidas a preguntas del día a día. Escribe una consulta para cada una. Antes de mirar la solución, comprueba que obtienes **el mismo número de filas**.

#### Enunciado

**Bloque A · Proyección y ordenación**

**A1.** Código, nombre y horas de todos los módulos de ASIR, de más a menos horas.

{{% details title="Solución A1" %}}
```sql
SELECT codigo, nombre, horas
FROM   modulo
WHERE  cod_ciclo = 'ASIR'
ORDER  BY horas DESC;
```

| CODIGO | NOMBRE | HORAS |
|---|---|---|
| 0369 | Implantación de sistemas operativos | 224 |
| 0370 | Planificación y administración de redes | 192 |
| 0372 | Gestión de bases de datos | 160 |
| 0371 | Fundamentos de hardware | 96 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | 96 |

*5 filas*

{{% /details %}}

**A2.** Nombre completo del profesorado en el formato «Apellidos, Nombre», ordenado alfabéticamente, con una columna llamada `profesor`.

{{% details title="Solución A2" %}}
```sql
SELECT apellidos || ', ' || nombre AS profesor
FROM   profesor
ORDER  BY profesor;
```

| PROFESOR |
|---|
| Brotons Sala, Elena |
| Cano Vidal, Raúl |
| Esteve Juan, David |
| Ferrándiz Mora, Lucía |
| Gómez Pérez, Nuria |
| Lillo Martí, Pablo |
| Navarro Ruiz, Andrés |
| Ortiz Llorca, Carmen |
| Pastor Gil, Javier |
| Ramos Climent, Sergio |
| Soler Ivars, Marta |
| Vicent Ribes, Laura |

*12 filas*

{{% /details %}}

**A3.** Las distintas especialidades del profesorado, sin repetir.

{{% details title="Solución A3" %}}
```sql
SELECT DISTINCT especialidad FROM profesor ORDER BY especialidad;
```

| ESPECIALIDAD |
|---|
| Administración de Empresas |
| Formación y Orientación Laboral |
| Informática |
| Inglés |
| Sistemas y Aplicaciones Informáticas |

*5 filas*

{{% /details %}}

**A4.** Los distintos pares (ciclo, curso) que existen en la tabla de módulos.

{{% details title="Solución A4" %}}
```sql
SELECT DISTINCT cod_ciclo, curso FROM modulo ORDER BY cod_ciclo, curso;
```

| COD_CICLO | CURSO |
|---|---|
| ASIR | 1 |
| DAM | 1 |
| DAM | 2 |
| DAW | 1 |
| DAW | 2 |

*5 filas*

{{% /details %}}

**Bloque B · Selección**

**B1.** Alumnado que vive en Elche o en El Campello (nombre, apellidos y localidad).

{{% details title="Solución B1" %}}
```sql
SELECT nombre, apellidos, localidad
FROM   alumno
WHERE  localidad IN ('Elche', 'El Campello')
ORDER  BY localidad, apellidos;
```

| NOMBRE | APELLIDOS | LOCALIDAD |
|---|---|---|
| Daniel | Alemany Pérez | El Campello |
| Elena | Carbonell Soriano | El Campello |
| Jorge | Iborra Alemany | El Campello |
| Rubén | Iborra Ferri | Elche |
| Sofía | Planelles Marco | Elche |
| Víctor | Tomás Guillem | Elche |

*6 filas*

{{% /details %}}

**B2.** Módulos que tienen entre 96 y 128 horas, ambas incluidas.

{{% details title="Solución B2" %}}
```sql
SELECT codigo, nombre, cod_ciclo, horas
FROM   modulo
WHERE  horas BETWEEN 96 AND 128
ORDER  BY horas, codigo, cod_ciclo;
```

| CODIGO | NOMBRE | COD_CICLO | HORAS |
|---|---|---|---|
| 0371 | Fundamentos de hardware | ASIR | 96 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | ASIR | 96 |
| 0487 | Entornos de desarrollo | DAM | 96 |
| 0487 | Entornos de desarrollo | DAW | 96 |
| 0489 | Programación multimedia y dispositivos móviles | DAM | 100 |
| 0491 | Sistemas de gestión empresarial | DAM | 100 |
| 0486 | Acceso a datos | DAM | 120 |
| 0488 | Desarrollo de interfaces | DAM | 120 |
| 0615 | Diseño de interfaces web | DAW | 120 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | DAM | 128 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | DAW | 128 |

*11 filas*

{{% /details %}}

**B3.** Alumnado nacido antes de 2005, del mayor al menor.

{{% details title="Solución B3" %}}
```sql
SELECT nombre, apellidos, fecha_nacimiento
FROM   alumno
WHERE  fecha_nacimiento < DATE '2005-01-01'
ORDER  BY fecha_nacimiento;
```

| NOMBRE | APELLIDOS | FECHA_NACIMIENTO |
|---|---|---|
| Sara | Amorós Guillem | 07/08/2000 |
| Jorge | Iborra Alemany | 01/06/2001 |
| Daniel | Alemany Pérez | 22/08/2001 |
| Mateo | Sala Brotons | 09/04/2003 |
| Iván | Ripoll Agulló | 01/05/2003 |
| Lucía | Belda Quiles | 07/11/2003 |
| Valeria | Quiles Marco | 20/01/2004 |
| Noelia | Verdú Espí | 25/06/2004 |
| Carla | Valero Cerdá | 08/07/2004 |
| Sofía | Planelles Marco | 13/07/2004 |

*10 filas*

{{% /details %}}

**B4.** Profesorado del departamento 1 que **no** tiene la especialidad «Informática».

{{% details title="Solución B4" %}}
```sql
SELECT nombre, apellidos, especialidad
FROM   profesor
WHERE  id_departamento = 1
AND    especialidad <> 'Informática'
ORDER  BY apellidos;
```

| NOMBRE | APELLIDOS | ESPECIALIDAD |
|---|---|---|
| Elena | Brotons Sala | Sistemas y Aplicaciones Informáticas |
| Pablo | Lillo Martí | Sistemas y Aplicaciones Informáticas |
| Javier | Pastor Gil | Sistemas y Aplicaciones Informáticas |

*3 filas*

{{% /details %}}

**B5.** Módulos cuyo nombre contiene la palabra «web» (en cualquier combinación de mayúsculas).

{{% details title="Solución B5" %}}
```sql
SELECT codigo, nombre
FROM   modulo
WHERE  UPPER(nombre) LIKE '%WEB%'
ORDER  BY codigo;
```

| CODIGO | NOMBRE |
|---|---|
| 0612 | Desarrollo web en entorno cliente |
| 0613 | Desarrollo web en entorno servidor |
| 0614 | Despliegue de aplicaciones web |
| 0615 | Diseño de interfaces web |

*4 filas*

{{% /details %}}

**B6.** Matrículas en segunda convocatoria o posterior (id de matrícula, alumno, módulo, convocatoria y nota).

{{% details title="Solución B6" %}}
```sql
SELECT id_matricula, id_alumno, id_modulo, convocatoria, nota_final
FROM   matricula
WHERE  convocatoria >= 2
ORDER  BY id_alumno;
```

| ID_MATRICULA | ID_ALUMNO | ID_MODULO | CONVOCATORIA | NOTA_FINAL |
|---|---|---|---|---|
| 10051 | 10 | 1 | 2 | 7.25 |
| 10057 | 11 | 5 | 2 | 5.75 |
| 10063 | 12 | 3 | 2 | 2.75 |

*3 filas*

{{% /details %}}

**B7.** Faltas **justificadas** de 3 horas.

{{% details title="Solución B7" %}}
```sql
SELECT id_falta, id_matricula, fecha, horas
FROM   falta_asistencia
WHERE  justificada = 'S' AND horas = 3
ORDER  BY fecha;
```

| ID_FALTA | ID_MATRICULA | FECHA | HORAS |
|---|---|---|---|
| 43 | 10048 | 21/11/2025 | 3 |
| 6 | 10003 | 04/02/2026 | 3 |
| 14 | 10084 | 11/02/2026 | 3 |

*3 filas*

{{% /details %}}

**B8.** Faltas registradas en diciembre de 2025.

{{% details title="Solución B8" %}}
```sql
SELECT id_falta, id_matricula, fecha, horas, justificada
FROM   falta_asistencia
WHERE  fecha >= DATE '2025-12-01' AND fecha < DATE '2026-01-01'
ORDER  BY fecha;
```

| ID_FALTA | ID_MATRICULA | FECHA | HORAS | JUSTIFICADA |
|---|---|---|---|---|
| 26 | 10029 | 03/12/2025 | 1 | N |
| 35 | 10065 | 08/12/2025 | 1 | N |

*2 filas*

{{% /details %}}

**Bloque C · Valores nulos y límites**

**C1.** Matrículas **sin calificar**.

{{% details title="Solución C1" %}}
```sql
SELECT id_matricula, id_alumno, id_modulo
FROM   matricula
WHERE  nota_final IS NULL
ORDER  BY id_matricula;
```

| ID_MATRICULA | ID_ALUMNO | ID_MODULO |
|---|---|---|
| 10015 | 3 | 5 |
| 10039 | 8 | 9 |
| 10055 | 11 | 9 |
| 10087 | 17 | 14 |
| 10111 | 23 | 16 |
| 10135 | 28 | 21 |

*6 filas*

{{% /details %}}

**C2.** Grupos sin tutor asignado.

{{% details title="Solución C2" %}}
```sql
SELECT cod_grupo FROM grupo WHERE id_tutor IS NULL;
```

| COD_GRUPO |
|---|
| 2ASIR |

*1 fila*

{{% /details %}}

**C3.** Las tres matrículas con peor nota (entre las calificadas), con desempate por `id_matricula`.

{{% details title="Solución C3" %}}
```sql
SELECT id_matricula, id_alumno, id_modulo, nota_final
FROM   matricula
WHERE  nota_final IS NOT NULL
ORDER  BY nota_final, id_matricula
FETCH FIRST 3 ROWS ONLY;
```

| ID_MATRICULA | ID_ALUMNO | ID_MODULO | NOTA_FINAL |
|---|---|---|---|
| 10105 | 21 | 18 | 1.5 |
| 10137 | 28 | 23 | 1.75 |
| 10047 | 10 | 7 | 2.25 |

*3 filas*

{{% /details %}}

**C4.** Los dos profesores con más antigüedad en el centro.

{{% details title="Solución C4" %}}
```sql
SELECT nombre, apellidos, fecha_alta
FROM   profesor
ORDER  BY fecha_alta
FETCH FIRST 2 ROWS ONLY;
```

| NOMBRE | APELLIDOS | FECHA_ALTA |
|---|---|---|
| Marta | Soler Ivars | 01/09/2009 |
| Carmen | Ortiz Llorca | 01/09/2010 |

*2 filas*

{{% /details %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Cada consulta empieza con un comentario que repite la pregunta.
- [ ] Ninguna consulta compara con `= NULL` ni usa fechas como texto.
- [ ] Todas las consultas que devuelven listados tienen `ORDER BY`.
- [ ] El número de filas de cada consulta coincide con la solución.
{{% /comprobacion %}}

#### Errores habituales

> [!WARNING]
> - En B4, la condición `especialidad <> 'Informática'` excluye también a quien tenga la especialidad a `NULL`. En estos datos no hay ninguno, pero en una consulta real tendrías que decidir si incluirlos con `OR especialidad IS NULL`.
> - En B8, `fecha BETWEEN DATE '2025-12-01' AND DATE '2025-12-31'` no incluiría una falta del 31 a las 10:00. En estos datos todas las fechas son a las 00:00, pero acostúmbrate al intervalo semiabierto.

#### Ampliación

Escribe B5 de tres formas distintas (con `UPPER`, con `LOWER` y con `REGEXP_LIKE(nombre, 'web', 'i')`) y comprueba que dan el mismo resultado.

---

## Práctica 6.3 · Laboratorio de valores nulos

{{< practica num="6.3" tipo="Guiada" duracion="1 sesión" nivel="2" ra="RA3: b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="Tabla de predicciones + resultados reales" >}}

#### Objetivo

Comprender la lógica de tres valores **prediciendo** el resultado de consultas con `NULL` antes de ejecutarlas.

#### Desarrollo

Para cada consulta, **escribe primero tu predicción** del número de filas. Después ejecútala y anota el resultado real. Si no coinciden, explica por qué.

Datos de partida: `ALUMNO` tiene 32 filas; 3 sin grupo, 4 sin DNI, 3 sin email y 5 sin teléfono. `MATRICULA` tiene 143 filas, de las que 6 están sin calificar.

| # | Consulta | Tu predicción | Real |
|---|---|---|---|
| 1 | `SELECT COUNT(*) FROM alumno WHERE dni = NULL;` | | |
| 2 | `SELECT COUNT(*) FROM alumno WHERE dni IS NULL;` | | |
| 3 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM';` | | |
| 4 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo <> '1DAM' OR cod_grupo IS NULL;` | | |
| 5 | `SELECT COUNT(*) FROM alumno WHERE email IS NULL OR telefono IS NULL;` | | |
| 6 | `SELECT COUNT(*) FROM matricula WHERE nota_final >= 5;` | | |
| 7 | `SELECT COUNT(*) FROM matricula WHERE NOT (nota_final >= 5);` | | |
| 8 | `SELECT COUNT(*) FROM matricula WHERE NVL(nota_final, 0) < 5;` | | |
| 9 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo NOT IN ('1DAM', '2DAM');` | | |
| 10 | `SELECT COUNT(*) FROM alumno WHERE cod_grupo NOT IN ('1DAM', NULL);` | | |

{{% details title="Resultados reales y explicación" %}}
| # | Real | Explicación |
|---|---|---|
| 1 | 0 | `= NULL` nunca es verdadero |
| 2 | 4 | Forma correcta |
| 3 | 22 | 32 − 7 de 1DAM − 3 sin grupo (desconocido) |
| 4 | 25 | Ahora sí se incluyen los 3 sin grupo |
| 5 | 8 | 3 sin email + 5 sin teléfono; ningún alumno carece de los dos |
| 6 | 110 | Solo las calificadas con 5 o más |
| 7 | 27 | Los suspensos calificados. ¡`NOT` de desconocido sigue siendo desconocido! 6 + 110 + 27 = 143 |
| 8 | 33 | `NVL` convierte los 6 sin calificar en 0: 27 + 6 |
| 9 | 16 | 32 − 7 − 6 − 3 sin grupo |
| 10 | 0 | `NOT IN` con un `NULL` en la lista **nunca** devuelve filas: `x <> NULL` siempre es desconocido |
{{% /details %}}

> [!CAUTION]
> El caso 10 es una trampa clásica que aparecerá de nuevo en la UD07 con las subconsultas: `WHERE id NOT IN (SELECT ...)` no devuelve nada si la subconsulta devuelve algún `NULL`.

---

## Práctica 6.4 · Funciones para informes

{{< practica num="6.4" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA3: b · RA5: e" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_4.sql comentado" >}}

#### Objetivo

Usar las funciones de fila de Oracle para transformar y presentar los datos.

#### Enunciado

**F1.** Genera la **etiqueta del casillero** de cada alumno de 1DAM: inicial del nombre, punto, primer apellido en mayúsculas y el NIA entre corchetes. Ejemplo: `A. FERRI [10450037]`.

{{% details title="Solución F1" %}}
```sql
SELECT SUBSTR(nombre, 1, 1) || '. ' ||
       UPPER(SUBSTR(apellidos, 1, INSTR(apellidos, ' ') - 1)) ||
       ' [' || nia || ']' AS etiqueta
FROM   alumno
WHERE  cod_grupo = '1DAM'
ORDER  BY apellidos, nombre;
```

| ETIQUETA |
|---|
| A. BROTONS [10450185] |
| T. CERDÁ [10450222] |
| A. FERRI [10450037] |
| P. FERRI [10450148] |
| R. IBORRA [10450074] |
| V. QUILES [10450259] |
| N. VERDÚ [10450111] |

*7 filas*
{{% /details %}}

**F2.** Para cada módulo de DAW, muestra el código, el nombre y una columna `duracion` con el texto «Corto» (menos de 100 horas), «Medio» (de 100 a 159) o «Largo» (160 o más).

{{% details title="Solución F2" %}}
```sql
SELECT codigo, nombre,
       CASE
           WHEN horas < 100 THEN 'Corto'
           WHEN horas < 160 THEN 'Medio'
           ELSE 'Largo'
       END AS duracion
FROM   modulo
WHERE  cod_ciclo = 'DAW'
ORDER  BY codigo;
```

| CODIGO | NOMBRE | DURACION |
|---|---|---|
| 0373 | Lenguajes de marcas y sistemas de gestión de información | Medio |
| 0483 | Sistemas informáticos | Largo |
| 0484 | Bases de datos | Largo |
| 0485 | Programación | Largo |
| 0487 | Entornos de desarrollo | Corto |
| 0612 | Desarrollo web en entorno cliente | Medio |
| 0613 | Desarrollo web en entorno servidor | Largo |
| 0614 | Despliegue de aplicaciones web | Corto |
| 0615 | Diseño de interfaces web | Medio |

*9 filas*

{{% /details %}}

**F3.** Para el profesorado, muestra el nombre, la fecha de alta con el formato «01/09/2009» y el número de **años completos** de antigüedad a fecha 1 de septiembre de 2026.

{{% details title="Solución F3" %}}
```sql
SELECT nombre, apellidos,
       TO_CHAR(fecha_alta, 'DD/MM/YYYY') AS alta,
       TRUNC(MONTHS_BETWEEN(DATE '2026-09-01', fecha_alta) / 12) AS anios
FROM   profesor
ORDER  BY fecha_alta;
```

| NOMBRE | APELLIDOS | ALTA | ANIOS |
|---|---|---|---|
| Marta | Soler Ivars | 01/09/2009 | 17 |
| Carmen | Ortiz Llorca | 01/09/2010 | 16 |
| Javier | Pastor Gil | 01/09/2012 | 14 |
| Lucía | Ferrándiz Mora | 01/09/2015 | 11 |
| Laura | Vicent Ribes | 01/09/2016 | 10 |
| Andrés | Navarro Ruiz | 03/09/2018 | 7 |
| Sergio | Ramos Climent | 02/09/2019 | 6 |
| Elena | Brotons Sala | 01/09/2020 | 6 |
| Raúl | Cano Vidal | 01/09/2021 | 5 |
| Nuria | Gómez Pérez | 01/09/2023 | 3 |
| David | Esteve Juan | 02/09/2024 | 1 |
| Pablo | Lillo Martí | 01/09/2025 | 1 |

*12 filas*

Observa a Andrés (alta el 03/09/2018): a 1 de septiembre de 2026 le faltan dos días para cumplir 8 años, así que tiene **7** años completos.
{{% /details %}}

**F4.** Muestra el teléfono del alumnado de 2DAM de forma que, si no tiene, aparezca «Sin teléfono», y una columna `contacto` que muestre el email si existe y, si no, el teléfono.

{{% details title="Solución F4" %}}
```sql
SELECT nombre, apellidos,
       NVL(telefono, 'Sin teléfono')  AS telefono,
       COALESCE(email, telefono)      AS contacto
FROM   alumno
WHERE  cod_grupo = '2DAM'
ORDER  BY apellidos;
```

| NOMBRE | APELLIDOS | TELEFONO | CONTACTO |
|---|---|---|---|
| Martina | Alemany Vidal | 686052214 | martinaalemany9@alu.edugest.es |
| Lucía | Belda Quiles | 630313272 | luciabelda12@alu.edugest.es |
| Hugo | Brotons Iborra | 678897218 | hugobrotons11@alu.edugest.es |
| Nerea | Cerdá Tomás | Sin teléfono | nereacerda10@alu.edugest.es |
| María | Domènech Quiles | 675664399 | mariadomenech13@alu.edugest.es |
| Iván | Ripoll Agulló | 645665668 | 645665668 |

*6 filas*

{{% /details %}}

**F5.** Nombre del día de la semana (en castellano) de cada falta de asistencia de la matrícula 10044.

{{% details title="Solución F5" %}}
```sql
SELECT fecha,
       TO_CHAR(fecha, 'fmDay', 'NLS_DATE_LANGUAGE=SPANISH') AS dia_semana,
       horas, justificada
FROM   falta_asistencia
WHERE  id_matricula = 10044
ORDER  BY fecha;
```

| FECHA | DIA_SEMANA | HORAS | JUSTIFICADA |
|---|---|---|---|
| 11/03/2026 | Miércoles | 1 | S |
| 29/04/2026 | Miércoles | 3 | N |

*2 filas*

{{% /details %}}

**F6.** Para las matrículas del alumno 9, muestra la nota con **dos decimales** como texto (`TO_CHAR`), la nota redondeada y una columna `estado` con «Aprobado», «Suspenso» o «Pendiente».

{{% details title="Solución F6" %}}
```sql
SELECT id_matricula, id_modulo,
       TO_CHAR(nota_final, 'FM90.00') AS nota_texto,
       ROUND(nota_final)              AS redondeada,
       CASE
           WHEN nota_final IS NULL THEN 'Pendiente'
           WHEN nota_final >= 5    THEN 'Aprobado'
           ELSE 'Suspenso'
       END AS estado
FROM   matricula
WHERE  id_alumno = 9
ORDER  BY id_modulo;
```

| ID_MATRICULA | ID_MODULO | NOTA_TEXTO | REDONDEADA | ESTADO |
|---|---|---|---|---|
| 10041 | 6 | 9.00 | 9 | Aprobado |
| 10042 | 7 | 8.75 | 9 | Aprobado |
| 10043 | 8 | 8.00 | 8 | Aprobado |
| 10044 | 9 | 6.50 | 7 | Aprobado |
| 10045 | 10 | 9.75 | 10 | Aprobado |

*5 filas*

{{% /details %}}

#### Comprobación

{{% comprobacion %}}
- [ ] F1 funciona aunque un apellido tenga tildes.
- [ ] F3 calcula años **completos**, no la diferencia de años del calendario.
- [ ] F5 muestra los días en castellano aunque tu sesión esté en inglés.
{{% /comprobacion %}}

---

## Práctica 6.5 · Validar datos con SQL

{{< practica num="6.5" tipo="Reto" duracion="1 sesión" nivel="3" ra="RA3: b · RA5: e" sgbd="Oracle 26ai · esquema EDUGEST" entrega="p6_5.sql + informe de calidad de datos" >}}

#### Objetivo

Usar consultas y funciones del SGBD para auditar la **calidad de los datos**, una tarea profesional habitual antes de migrar o explotar una base de datos.

#### Contexto

Jefatura sospecha que hay datos mal introducidos. Te pide un informe de calidad.

#### Enunciado

1. **Letra del DNI.** La letra de un DNI es el carácter que ocupa la posición `MOD(número, 23) + 1` en la cadena `'TRWAGMYFPDXBNJZSQVHLCKE'`. Escribe una consulta que muestre el profesorado cuyo DNI tiene la letra **incorrecta**.
2. **Formato del correo.** Lista el alumnado cuyo email no cumple el patrón `texto@alu.edugest.es`.
3. **NIA.** Comprueba que todos los NIA tienen exactamente 8 dígitos numéricos.
4. **Coherencia de edades.** ¿Hay alumnado menor de 16 años a fecha 15/09/2025? ¿Y mayor de 30?
5. **Fechas de faltas.** ¿Hay faltas registradas en sábado o domingo?
6. Redacta un **informe** con los problemas encontrados y propón, para cada uno, una restricción (UD05) o un trigger (UD09) que lo habría evitado.

{{% details title="Pista para el apartado 1" %}}
```sql
SELECT nombre, apellidos, dni,
       SUBSTR('TRWAGMYFPDXBNJZSQVHLCKE', MOD(TO_NUMBER(SUBSTR(dni, 1, 8)), 23) + 1, 1) AS letra_correcta
FROM   profesor
WHERE  SUBSTR(dni, 9, 1) <> SUBSTR('TRWAGMYFPDXBNJZSQVHLCKE', MOD(TO_NUMBER(SUBSTR(dni, 1, 8)), 23) + 1, 1);
```
Debes encontrar **2** profesores con la letra incorrecta. ¿Valdría esta consulta para un NIE (que empieza por X, Y o Z)?
{{% /details %}}

{{% details title="Pista para el apartado 5" %}}
`TO_CHAR(fecha, 'D')` depende del territorio de la sesión (en unos países la semana empieza en domingo y en otros en lunes). Es más fiable `TO_CHAR(fecha, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') IN ('SAT', 'SUN')`.
{{% /details %}}

---

## Proyecto EduGest · UD06: consultas del día a día

{{< practica num="EduGest-6" tipo="Proyecto" duracion="Trabajo transversal (1 semana)" nivel="2" ra="RA3: a, b" sgbd="Oracle 26ai · esquema EDUGEST" entrega="edugest/05_consultas_basicas.sql" >}}

#### Enunciado

Entrevista (o imagina) a tres perfiles de EduGest: secretaría, tutoría y jefatura. Para cada uno, escribe **cinco preguntas** que se respondan con una consulta sobre **una sola tabla** y resuélvelas. Cada consulta debe:

1. Ir precedida de un comentario con el perfil, la pregunta y el número de filas que devuelve.
2. Usar al menos una de estas técnicas: `CASE`, una función de fecha, una función de texto, `NVL`/`COALESCE`, `FETCH FIRST`, `LIKE`, `IN` o `BETWEEN`.
3. Estar ordenada cuando devuelva un listado.

Incluye también una consulta creada con el **generador de consultas** de SQL Developer y explica qué ha generado.

#### Comprobación

{{% comprobacion %}}
- [ ] 15 consultas, todas ejecutables sin errores.
- [ ] Las técnicas indicadas aparecen al menos una vez cada una.
- [ ] Las preguntas son realistas y distintas a las de la práctica 6.2.
{{% /comprobacion %}}
