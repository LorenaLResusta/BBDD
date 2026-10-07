---
title: "Consultas avanzadas - Prácticas"
weight: 2
bookToc: true
---

# UD07 · Prácticas

{{< ra "RA3:a,c,d,e,f,g,h" "RA2:f" >}}

| Práctica | Tipo | Nivel | CE principales |
|---|---|---|---|
| [7.1 Consultas resumen](#práctica-71--consultas-resumen) | Guiada | ●○○ | RA3.e |
| [7.2 Composiciones paso a paso](#práctica-72--composiciones-paso-a-paso) | Guiada | ●●○ | RA3.c, RA3.d |
| [7.3 Informes para jefatura](#práctica-73--informes-para-jefatura) | Autónoma | ●●○ | RA3.c, RA3.d, RA3.e |
| [7.4 Subconsultas](#práctica-74--subconsultas) | Autónoma | ●●○ | RA3.f |
| [7.5 Múltiples selecciones y vistas](#práctica-75--múltiples-selecciones-y-vistas) | Autónoma | ●●○ | RA3.g, RA2.f |
| [7.6 Optimización: medir antes y después](#práctica-76--optimización-medir-antes-y-después) | Guiada | ●●● | RA3.h |
| [7.7 Reto: el cuadro de mando](#práctica-77--reto-el-cuadro-de-mando) | Reto | ●●● | RA3.c-h |
| [Proyecto EduGest · UD07](#proyecto-edugest--ud07-informes) | Proyecto | ●●● | RA3 completo |

> [!IMPORTANT]
> Trabaja sobre **EDUGEST con los datos originales** (scripts 01 y 02) y con `ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';`. Intenta cada consulta antes de abrir la solución; como mínimo, comprueba que obtienes el **mismo número de filas**.

---

## Práctica 7.1 · Consultas resumen

{{< practica num="7.1" tipo="Guiada" duracion="2 sesiones" nivel="1" ra="RA3: e" sgbd="Oracle 26ai · EDUGEST" entrega="p7_1.sql" >}}

#### Objetivo

Usar funciones de agregado, `GROUP BY` y `HAVING`, y entender cómo influyen los valores nulos en los resultados.

#### Desarrollo

{{% steps %}}

1. **Totales generales.** ¿Cuántos alumnos hay, cuántos tienen grupo y en cuántos grupos distintos están?

    ```sql
    SELECT COUNT(*) AS alumnos, COUNT(cod_grupo) AS con_grupo, COUNT(DISTINCT cod_grupo) AS grupos
    FROM   alumno;
    ```

    | ALUMNOS | CON_GRUPO | GRUPOS |
    |---|---|---|
    | 32 | 29 | 5 |

    *1 fila*


2. **Agrupar por una columna.** Número de alumnos por localidad, de más a menos.

    ```sql
    SELECT localidad, COUNT(*) AS alumnos
    FROM   alumno
    GROUP  BY localidad
    ORDER  BY alumnos DESC, localidad;
    ```

    | LOCALIDAD | ALUMNOS |
    |---|---|
    | Alicante | 13 |
    | Mutxamel | 6 |
    | Sant Joan d'Alacant | 4 |
    | El Campello | 3 |
    | Elche | 3 |
    | San Vicente del Raspeig | 3 |

    *6 filas*


3. **Agrupar por varias columnas.** Faltas y horas de falta por mes y por tipo (justificada o no).

    ```sql
    SELECT TO_CHAR(fecha, 'YYYY-MM') AS mes, justificada,
           COUNT(*) AS faltas, SUM(horas) AS horas
    FROM   falta_asistencia
    GROUP  BY TO_CHAR(fecha, 'YYYY-MM'), justificada
    ORDER  BY mes, justificada;
    ```

    | MES | JUSTIFICADA | FALTAS | HORAS |
    |---|---|---|---|
    | 2025-09 | N | 3 | 5 |
    | 2025-09 | S | 2 | 2 |
    | 2025-10 | N | 4 | 6 |
    | 2025-10 | S | 3 | 4 |
    | 2025-11 | N | 2 | 5 |
    | 2025-11 | S | 2 | 4 |
    | 2025-12 | N | 2 | 2 |
    | 2026-01 | N | 5 | 10 |
    | 2026-02 | N | 3 | 5 |
    | 2026-02 | S | 5 | 11 |
    | 2026-03 | N | 5 | 11 |
    | 2026-03 | S | 4 | 5 |
    | 2026-04 | N | 3 | 6 |
    | 2026-04 | S | 1 | 1 |
    | 2026-05 | S | 2 | 4 |

    *15 filas*


4. **Filtrar grupos.** Módulos (por `id_modulo`) con al menos un suspenso y su número de suspensos, solo si hay **dos o más**.

    ```sql
    SELECT id_modulo, COUNT(*) AS suspensos
    FROM   matricula
    WHERE  nota_final < 5
    GROUP  BY id_modulo
    HAVING COUNT(*) >= 2
    ORDER  BY suspensos DESC, id_modulo;
    ```

    | ID_MODULO | SUSPENSOS |
    |---|---|
    | 3 | 4 |
    | 18 | 3 |
    | 2 | 2 |
    | 6 | 2 |
    | 7 | 2 |
    | 10 | 2 |
    | 11 | 2 |
    | 13 | 2 |

    *8 filas*


5. **Contar condiciones.** Para cada convocatoria: matrículas, aprobadas, suspensas y sin calificar.

    ```sql
    SELECT convocatoria,
           COUNT(*) AS total,
           SUM(CASE WHEN nota_final >= 5 THEN 1 ELSE 0 END) AS aprobadas,
           SUM(CASE WHEN nota_final <  5 THEN 1 ELSE 0 END) AS suspensas,
           COUNT(*) - COUNT(nota_final)                    AS sin_calificar
    FROM   matricula
    GROUP  BY convocatoria
    ORDER  BY convocatoria;
    ```

    | CONVOCATORIA | TOTAL | APROBADAS | SUSPENSAS | SIN_CALIFICAR |
    |---|---|---|---|---|
    | 1 | 140 | 108 | 26 | 6 |
    | 2 | 3 | 2 | 1 | 0 |

    *2 filas*


6. **Provoca los errores típicos** y anota el mensaje:

    ```sql
    SELECT localidad, nombre, COUNT(*) FROM alumno GROUP BY localidad;   -- ORA-00979
    SELECT localidad, COUNT(*) FROM alumno;                              -- ORA-00937
    SELECT localidad FROM alumno WHERE COUNT(*) > 3 GROUP BY localidad;  -- ORA-00934
    ```

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] En el paso 1 entiendes por qué `COUNT(*)` y `COUNT(cod_grupo)` dan resultados distintos.
- [ ] En el paso 5, la suma de aprobadas, suspensas y sin calificar coincide con el total de cada convocatoria.
- [ ] Sabes corregir cada uno de los tres errores del paso 6.
{{% /comprobacion %}}

#### Ampliación

Repite el paso 2 añadiendo `ROLLUP`: `GROUP BY ROLLUP(localidad)`. ¿Qué fila nueva aparece? ¿Qué valor tiene `localidad` en ella?

---

## Práctica 7.2 · Composiciones paso a paso

{{< practica num="7.2" tipo="Guiada" duracion="2 sesiones" nivel="2" ra="RA3: c, d" sgbd="Oracle 26ai · EDUGEST" entrega="p7_2.sql + respuestas" >}}

#### Objetivo

Construir composiciones de varias tablas siguiendo el camino de claves ajenas, y decidir cuándo hace falta una composición externa.

#### Desarrollo

{{% steps %}}

1. **Traza el camino.** Queremos, para cada falta de asistencia, el nombre del alumno, el nombre del módulo y el ciclo. Sobre el diagrama relacional de EduGest, el camino es:

    ```mermaid
    flowchart LR
        F[FALTA_ASISTENCIA] -- id_matricula --> M[MATRICULA]
        M -- id_alumno --> A[ALUMNO]
        M -- id_modulo --> MO[MODULO]
        MO -- cod_ciclo --> C[CICLO]
    ```

2. **Añade las tablas una a una** y comprueba el número de filas en cada paso. Si el número **aumenta** de forma inesperada, falta una condición o la composición no sigue una clave ajena.

    ```sql
    -- Paso a: solo faltas
    SELECT COUNT(*) FROM falta_asistencia f;                                  -- 46
    -- Paso b: + matrícula
    SELECT COUNT(*) FROM falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula;              -- 46
    -- Paso c: + alumno y módulo
    SELECT COUNT(*) FROM falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
           JOIN modulo mo   ON mo.id_modulo   = m.id_modulo;                 -- 46
    ```

3. **Escribe la consulta final**, limitada a las faltas no justificadas de 3 horas:

    ```sql
    SELECT f.fecha, a.apellidos || ', ' || a.nombre AS alumno,
           mo.nombre AS modulo, c.cod_ciclo, f.horas
    FROM   falta_asistencia f
           JOIN matricula m ON m.id_matricula = f.id_matricula
           JOIN alumno a    ON a.id_alumno    = m.id_alumno
           JOIN modulo mo   ON mo.id_modulo   = m.id_modulo
           JOIN ciclo c     ON c.cod_ciclo    = mo.cod_ciclo
    WHERE  f.justificada = 'N' AND f.horas = 3
    ORDER  BY f.fecha;
    ```

    | FECHA | ALUMNO | MODULO | COD_CICLO | HORAS |
    |---|---|---|---|---|
    | 22/09/2025 | Quiles Marco, Valeria | Entornos de desarrollo | DAM | 3 |
    | 21/10/2025 | Ripoll Agulló, Iván | Sistemas de gestión empresarial | DAM | 3 |
    | 25/11/2025 | Cerdá Tomás, Nerea | Sistemas informáticos | DAM | 3 |
    | 06/01/2026 | Amorós Guillem, Sara | Diseño de interfaces web | DAW | 3 |
    | 21/01/2026 | Tomás Vidal, Álex | Lenguajes de marcas y sistemas de gestión de información | ASIR | 3 |
    | 25/02/2026 | Alemany Vidal, Martina | Sistemas de gestión empresarial | DAM | 3 |
    | 10/03/2026 | Cerdá Pérez, Tomás | Programación | DAM | 3 |
    | 19/03/2026 | Ferri Baeza, Adrián | Programación | DAM | 3 |
    | 25/03/2026 | Alemany Pérez, Daniel | Entornos de desarrollo | DAW | 3 |
    | 29/04/2026 | Alemany Vidal, Martina | Programación de servicios y procesos | DAM | 3 |

    *10 filas*


4. **Provoca un producto cartesiano** quitando la condición `ON` de `MODULO` (en Oracle, sustituye `JOIN modulo mo ON ...` por `CROSS JOIN modulo mo`). ¿Cuántas filas salen ahora en el paso c? ¿Por qué?

5. **Interna frente a externa.** Ejecuta las dos consultas y explica la diferencia:

    ```sql
    -- (a) Interna
    SELECT c.cod_ciclo, COUNT(g.cod_grupo) AS grupos
    FROM   ciclo c JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
    GROUP  BY c.cod_ciclo ORDER BY c.cod_ciclo;

    -- (b) Externa
    SELECT c.cod_ciclo, COUNT(g.cod_grupo) AS grupos
    FROM   ciclo c LEFT JOIN grupo g ON g.cod_ciclo = c.cod_ciclo
    GROUP  BY c.cod_ciclo ORDER BY c.cod_ciclo;
    ```

    | (a) Interna | | (b) Externa | |
    |---|---|---|---|
    | ASIR | 2 | ASIR | 2 |
    | DAM | 2 | DAM | 2 |
    | DAW | 2 | DAW | 2 |
    | | | **SMR** | **0** |

6. **La trampa del WHERE.** Queremos todos los profesores y las horas que imparten **en 2DAM** (0 si no imparten allí). Compara:

    ```sql
    -- (a) Incorrecta: el WHERE elimina a quien no imparte en 2DAM
    SELECT p.nombre, NVL(SUM(i.horas_semanales), 0) AS horas_2dam
    FROM   profesor p LEFT JOIN imparte i ON i.id_profesor = p.id_profesor
    WHERE  i.cod_grupo = '2DAM'
    GROUP  BY p.id_profesor, p.nombre ORDER BY p.id_profesor;     -- 4 filas

    -- (b) Correcta: la condición sobre la tabla opcional va en el ON
    SELECT p.nombre, NVL(SUM(i.horas_semanales), 0) AS horas_2dam
    FROM   profesor p LEFT JOIN imparte i
           ON i.id_profesor = p.id_profesor AND i.cod_grupo = '2DAM'
    GROUP  BY p.id_profesor, p.nombre ORDER BY p.id_profesor;     -- 12 filas
    ```

    | NOMBRE | HORAS_2DAM |
    |---|---|
    | Marta | 0 |
    | Javier | 3 |
    | Lucía | 6 |
    | Andrés | 4 |
    | Elena | 0 |
    | Raúl | 3 |
    | Nuria | 0 |
    | Pablo | 0 |
    | Carmen | 0 |
    | Sergio | 0 |
    | Laura | 0 |
    | David | 0 |

    *12 filas*


{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Las tres consultas del paso 2 devuelven 46 filas.
- [ ] En el paso 4 obtienes 46 × 24 = 1104 filas y sabes explicarlo.
- [ ] Sabes explicar por qué SMR solo aparece con `LEFT JOIN` y por qué el `COUNT` da 0 y no 1.
- [ ] En el paso 6, la versión (b) devuelve los 12 profesores.
{{% /comprobacion %}}

---

## Práctica 7.3 · Informes para jefatura

{{< practica num="7.3" tipo="Autónoma" duracion="3 sesiones" nivel="2" ra="RA3: c, d, e" sgbd="Oracle 26ai · EDUGEST" entrega="p7_3.sql comentado" >}}

#### Objetivo

Resolver de forma autónoma consultas de varias tablas, decidiendo el tipo de composición y combinándolas con agrupamientos.

#### Enunciado

**J1.** Listado de módulos con el nombre completo de su ciclo, solo de 2º curso.

{{% details title="Solución J1" %}}
```sql
SELECT c.nombre AS ciclo, mo.codigo, mo.nombre AS modulo
FROM   modulo mo JOIN ciclo c ON c.cod_ciclo = mo.cod_ciclo
WHERE  mo.curso = 2
ORDER  BY c.nombre, mo.codigo;
```

| CICLO | CODIGO | MODULO |
|---|---|---|
| Desarrollo de Aplicaciones Multiplataforma | 0486 | Acceso a datos |
| Desarrollo de Aplicaciones Multiplataforma | 0488 | Desarrollo de interfaces |
| Desarrollo de Aplicaciones Multiplataforma | 0489 | Programación multimedia y dispositivos móviles |
| Desarrollo de Aplicaciones Multiplataforma | 0490 | Programación de servicios y procesos |
| Desarrollo de Aplicaciones Multiplataforma | 0491 | Sistemas de gestión empresarial |
| Desarrollo de Aplicaciones Web | 0612 | Desarrollo web en entorno cliente |
| Desarrollo de Aplicaciones Web | 0613 | Desarrollo web en entorno servidor |
| Desarrollo de Aplicaciones Web | 0614 | Despliegue de aplicaciones web |
| Desarrollo de Aplicaciones Web | 0615 | Diseño de interfaces web |

*9 filas*

{{% /details %}}

**J2.** Profesorado con el nombre de su departamento y, si es jefe de algún departamento, el nombre de ese departamento (si no, vacío).

{{% details title="Solución J2" %}}
```sql
SELECT p.nombre, p.apellidos, d.nombre AS departamento, dj.nombre AS jefe_de
FROM   profesor p
       JOIN departamento d       ON d.id_departamento = p.id_departamento
       LEFT JOIN departamento dj ON dj.id_jefe        = p.id_profesor
ORDER  BY p.id_profesor;
```

| NOMBRE | APELLIDOS | DEPARTAMENTO | JEFE_DE |
|---|---|---|---|
| Marta | Soler Ivars | Informática y Comunicaciones | Informática y Comunicaciones |
| Javier | Pastor Gil | Informática y Comunicaciones | (null) |
| Lucía | Ferrándiz Mora | Informática y Comunicaciones | (null) |
| Andrés | Navarro Ruiz | Informática y Comunicaciones | (null) |
| Elena | Brotons Sala | Informática y Comunicaciones | (null) |
| Raúl | Cano Vidal | Informática y Comunicaciones | (null) |
| Nuria | Gómez Pérez | Informática y Comunicaciones | (null) |
| Pablo | Lillo Martí | Informática y Comunicaciones | (null) |
| Carmen | Ortiz Llorca | Formación y Orientación Laboral | Formación y Orientación Laboral |
| Sergio | Ramos Climent | Formación y Orientación Laboral | (null) |
| Laura | Vicent Ribes | Inglés | Inglés |
| David | Esteve Juan | Administración y Gestión | Administración y Gestión |

*12 filas*

La tabla `DEPARTAMENTO` aparece **dos veces** con alias distintos, porque se relaciona con `PROFESOR` por dos caminos diferentes.
{{% /details %}}

**J3.** Carga docente: para cada profesor que imparte clase, número de módulos, número de grupos distintos y horas semanales totales, de más a menos horas.

{{% details title="Solución J3" %}}
```sql
SELECT p.nombre, p.apellidos,
       COUNT(*)                    AS modulos,
       COUNT(DISTINCT i.cod_grupo) AS grupos,
       SUM(i.horas_semanales)      AS horas
FROM   imparte i JOIN profesor p ON p.id_profesor = i.id_profesor
GROUP  BY p.id_profesor, p.nombre, p.apellidos
ORDER  BY horas DESC, p.apellidos;
```

| NOMBRE | APELLIDOS | MODULOS | GRUPOS | HORAS |
|---|---|---|---|---|
| Javier | Pastor Gil | 4 | 4 | 16 |
| Elena | Brotons Sala | 3 | 2 | 15 |
| Raúl | Cano Vidal | 3 | 3 | 15 |
| Nuria | Gómez Pérez | 4 | 4 | 15 |
| Andrés | Navarro Ruiz | 4 | 4 | 15 |
| Marta | Soler Ivars | 3 | 3 | 15 |
| Lucía | Ferrándiz Mora | 3 | 2 | 14 |

*7 filas*

{{% /details %}}

**J4.** Todos los grupos con su número de alumnos y su tutor; deben aparecer los grupos sin alumnos y sin tutor.

{{% details title="Solución J4" %}}
```sql
SELECT g.cod_grupo,
       COUNT(a.id_alumno) AS alumnos,
       NVL2(p.id_profesor, p.nombre || ' ' || p.apellidos, '(sin tutor)') AS tutor
FROM   grupo g
       LEFT JOIN alumno a   ON a.cod_grupo   = g.cod_grupo
       LEFT JOIN profesor p ON p.id_profesor = g.id_tutor
GROUP  BY g.cod_grupo, p.id_profesor, p.nombre, p.apellidos
ORDER  BY g.cod_grupo;
```

| COD_GRUPO | ALUMNOS | TUTOR |
|---|---|---|
| 1ASIR | 5 | Elena Brotons Sala |
| 1DAM | 7 | Lucía Ferrándiz Mora |
| 1DAW | 6 | Raúl Cano Vidal |
| 2ASIR | 0 | (sin tutor) |
| 2DAM | 6 | Andrés Navarro Ruiz |
| 2DAW | 5 | Nuria Gómez Pérez |

*6 filas*

{{% /details %}}

**J5.** Porcentaje de aprobados por módulo de DAM (código, nombre, matrículas calificadas y porcentaje con un decimal), del peor al mejor porcentaje.

{{% details title="Solución J5" %}}
```sql
SELECT mo.codigo, mo.nombre,
       COUNT(m.nota_final) AS calificadas,
       ROUND(100 * SUM(CASE WHEN m.nota_final >= 5 THEN 1 ELSE 0 END) / COUNT(m.nota_final), 1) AS pct_aprobados
FROM   modulo mo JOIN matricula m ON m.id_modulo = mo.id_modulo
WHERE  mo.cod_ciclo = 'DAM'
GROUP  BY mo.id_modulo, mo.codigo, mo.nombre
ORDER  BY pct_aprobados, mo.codigo;
```

| CODIGO | NOMBRE | CALIFICADAS | PCT_APROBADOS |
|---|---|---|---|
| 0485 | Programación | 8 | 50 |
| 0486 | Acceso a datos | 6 | 66.7 |
| 0488 | Desarrollo de interfaces | 6 | 66.7 |
| 0491 | Sistemas de gestión empresarial | 6 | 66.7 |
| 0484 | Bases de datos | 7 | 71.4 |
| 0489 | Programación multimedia y dispositivos móviles | 6 | 83.3 |
| 0487 | Entornos de desarrollo | 7 | 85.7 |
| 0483 | Sistemas informáticos | 8 | 87.5 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | 7 | 100 |
| 0490 | Programación de servicios y procesos | 4 | 100 |

*10 filas*

{{% /details %}}

**J6.** Alumnado con más de 3 horas de faltas **no justificadas** en total (nombre, grupo y horas).

{{% details title="Solución J6" %}}
```sql
SELECT a.nombre, a.apellidos, a.cod_grupo, SUM(f.horas) AS horas_injustificadas
FROM   falta_asistencia f
       JOIN matricula m ON m.id_matricula = f.id_matricula
       JOIN alumno a    ON a.id_alumno    = m.id_alumno
WHERE  f.justificada = 'N'
GROUP  BY a.id_alumno, a.nombre, a.apellidos, a.cod_grupo
HAVING SUM(f.horas) > 3
ORDER  BY horas_injustificadas DESC, a.apellidos;
```

| NOMBRE | APELLIDOS | COD_GRUPO | HORAS_INJUSTIFICADAS |
|---|---|---|---|
| Martina | Alemany Vidal | 2DAM | 6 |
| Valeria | Quiles Marco | 1DAM | 5 |
| Tomás | Cerdá Pérez | 1DAM | 4 |
| Álex | Tomás Vidal | 1ASIR | 4 |
| Carla | Valero Cerdá | 1DAW | 4 |

*5 filas*

{{% /details %}}

**J7.** Profesorado del departamento de Informática y Comunicaciones que **no** es tutor de ningún grupo.

{{% details title="Solución J7" %}}
```sql
SELECT p.id_profesor, p.nombre, p.apellidos
FROM   profesor p
       JOIN departamento d ON d.id_departamento = p.id_departamento
       LEFT JOIN grupo g   ON g.id_tutor = p.id_profesor
WHERE  d.nombre = 'Informática y Comunicaciones'
AND    g.cod_grupo IS NULL
ORDER  BY p.id_profesor;
```

| ID_PROFESOR | NOMBRE | APELLIDOS |
|---|---|---|
| 101 | Marta | Soler Ivars |
| 102 | Javier | Pastor Gil |
| 108 | Pablo | Lillo Martí |

*3 filas*

Aquí la condición `g.cod_grupo IS NULL` **sí** va en el `WHERE`: es precisamente la que selecciona las filas sin pareja (anti-composición).
{{% /details %}}

**J8.** Para cada alumno de 1DAM, su nota en *Bases de datos* (0484) y en *Programación* (0485) en la misma fila.

{{% details title="Solución J8" %}}
```sql
SELECT a.apellidos, a.nombre,
       MAX(CASE WHEN mo.codigo = '0484' THEN m.nota_final END) AS bases_datos,
       MAX(CASE WHEN mo.codigo = '0485' THEN m.nota_final END) AS programacion
FROM   alumno a
       JOIN matricula m ON m.id_alumno = a.id_alumno
       JOIN modulo mo   ON mo.id_modulo = m.id_modulo
WHERE  a.cod_grupo = '1DAM'
GROUP  BY a.id_alumno, a.apellidos, a.nombre
ORDER  BY a.apellidos, a.nombre;
```

| APELLIDOS | NOMBRE | BASES_DATOS | PROGRAMACION |
|---|---|---|---|
| Brotons Soriano | Andrea | 5.75 | 4.75 |
| Cerdá Pérez | Tomás | 5.25 | 7.25 |
| Ferri Baeza | Adrián | 4.75 | 7.25 |
| Ferri Baeza | Paula | 6.5 | 3.25 |
| Iborra Ferri | Rubén | 4.75 | 4.5 |
| Quiles Marco | Valeria | 6.5 | 8 |
| Verdú Espí | Noelia | 8 | 6.75 |

*7 filas*

Esta técnica (pasar filas a columnas) se llama **pivotar**. Oracle también tiene la cláusula `PIVOT`.
{{% /details %}}

#### Comprobación

{{% comprobacion %}}
- [ ] Has elegido composición interna o externa según la pregunta y lo justificas en un comentario.
- [ ] J4 muestra 2ASIR con 0 alumnos y «(sin tutor)».
- [ ] J5 no divide entre las matrículas sin calificar.
{{% /comprobacion %}}

---

## Práctica 7.4 · Subconsultas

{{< practica num="7.4" tipo="Autónoma" duracion="2 sesiones" nivel="2" ra="RA3: f" sgbd="Oracle 26ai · EDUGEST" entrega="p7_4.sql" >}}

#### Enunciado

**S1.** Alumnado de mayor edad (puede haber empates).

{{% details title="Solución S1" %}}
```sql
SELECT nombre, apellidos, fecha_nacimiento
FROM   alumno
WHERE  fecha_nacimiento = (SELECT MIN(fecha_nacimiento) FROM alumno);
```

| NOMBRE | APELLIDOS | FECHA_NACIMIENTO |
|---|---|---|
| Sara | Amorós Guillem | 07/08/2000 |

*1 fila*

{{% /details %}}

**S2.** Módulos de DAW con más horas que **cualquier** módulo de 2º de DAM.

{{% details title="Solución S2" %}}
```sql
SELECT codigo, nombre, horas
FROM   modulo
WHERE  cod_ciclo = 'DAW'
AND    horas > ALL (SELECT horas FROM modulo WHERE cod_ciclo = 'DAM' AND curso = 2)
ORDER  BY horas DESC, codigo;
```

| CODIGO | NOMBRE | HORAS |
|---|---|---|
| 0485 | Programación | 256 |
| 0483 | Sistemas informáticos | 160 |
| 0484 | Bases de datos | 160 |
| 0613 | Desarrollo web en entorno servidor | 160 |
| 0612 | Desarrollo web en entorno cliente | 140 |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | 128 |

*6 filas*

`> ALL` equivale a «mayor que el máximo», es decir, mayor que 120.
{{% /details %}}

**S3.** Alumnos que tienen **alguna** falta de asistencia (usa `EXISTS`).

{{% details title="Solución S3" %}}
```sql
SELECT a.id_alumno, a.nombre, a.apellidos
FROM   alumno a
WHERE  EXISTS (SELECT 1
               FROM   falta_asistencia f JOIN matricula m ON m.id_matricula = f.id_matricula
               WHERE  m.id_alumno = a.id_alumno)
ORDER  BY a.id_alumno;
```

| ID_ALUMNO | NOMBRE | APELLIDOS |
|---|---|---|
| 1 | Adrián | Ferri Baeza |
| 3 | Noelia | Verdú Espí |
| 6 | Tomás | Cerdá Pérez |
| 7 | Valeria | Quiles Marco |
| 8 | Iván | Ripoll Agulló |
| 9 | Martina | Alemany Vidal |
| 10 | Nerea | Cerdá Tomás |
| 11 | Hugo | Brotons Iborra |
| 12 | Lucía | Belda Quiles |
| 13 | María | Domènech Quiles |
| 14 | Carla | Valero Cerdá |
| 16 | Julia | Espí Marco |
| 17 | Jorge | Iborra Alemany |
| 18 | Daniel | Alemany Pérez |
| 20 | Mateo | Sala Brotons |
| 21 | Elena | Carbonell Soriano |
| 22 | Sofía | Planelles Marco |
| 23 | Sara | Amorós Guillem |
| 25 | Diego | Iborra Torregrosa |
| 26 | Víctor | Tomás Guillem |
| 27 | Álex | Tomás Vidal |
| 28 | Pablo | Amorós Carbonell |
| 29 | Aitana | Pascual Brotons |

*23 filas*

{{% /details %}}

**S4.** Alumnos con grupo que **no** tienen ninguna falta.

{{% details title="Solución S4" %}}
```sql
SELECT a.id_alumno, a.nombre, a.apellidos, a.cod_grupo
FROM   alumno a
WHERE  a.cod_grupo IS NOT NULL
AND    NOT EXISTS (SELECT 1
                   FROM   falta_asistencia f JOIN matricula m ON m.id_matricula = f.id_matricula
                   WHERE  m.id_alumno = a.id_alumno)
ORDER  BY a.id_alumno;
```

| ID_ALUMNO | NOMBRE | APELLIDOS | COD_GRUPO |
|---|---|---|---|
| 2 | Rubén | Iborra Ferri | 1DAM |
| 4 | Paula | Ferri Baeza | 1DAM |
| 5 | Andrea | Brotons Soriano | 1DAM |
| 15 | Manuel | Soriano Domènech | 1DAW |
| 19 | Alba | Torregrosa Planelles | 1DAW |
| 24 | Nicolás | Verdú Castelló | 2DAW |

*6 filas*

{{% /details %}}

**S5.** Para cada alumno de 2DAW, su nota media y la diferencia con la media de **su grupo** (subconsulta correlacionada).

{{% details title="Solución S5" %}}
```sql
SELECT a.nombre, a.apellidos,
       ROUND(AVG(m.nota_final), 2) AS media_alumno,
       ROUND(AVG(m.nota_final) - (SELECT AVG(m2.nota_final)
                                  FROM   matricula m2 JOIN alumno a2 ON a2.id_alumno = m2.id_alumno
                                  WHERE  a2.cod_grupo = a.cod_grupo), 2) AS diferencia
FROM   alumno a JOIN matricula m ON m.id_alumno = a.id_alumno
WHERE  a.cod_grupo = '2DAW'
GROUP  BY a.id_alumno, a.nombre, a.apellidos, a.cod_grupo
ORDER  BY media_alumno DESC;
```

| NOMBRE | APELLIDOS | MEDIA_ALUMNO | DIFERENCIA |
|---|---|---|---|
| Mateo | Sala Brotons | 7.13 | 1.19 |
| Nicolás | Verdú Castelló | 6 | 0.07 |
| Sofía | Planelles Marco | 5.56 | -0.37 |
| Elena | Carbonell Soriano | 5.44 | -0.5 |
| Sara | Amorós Guillem | 5.42 | -0.52 |

*5 filas*

{{% /details %}}

**S6.** El grupo (o grupos) con más alumnos. Resuélvelo con una subconsulta en el `HAVING`.

{{% details title="Solución S6" %}}
```sql
SELECT cod_grupo, COUNT(*) AS alumnos
FROM   alumno
WHERE  cod_grupo IS NOT NULL
GROUP  BY cod_grupo
HAVING COUNT(*) = (SELECT MAX(COUNT(*)) FROM alumno WHERE cod_grupo IS NOT NULL GROUP BY cod_grupo);
```

| COD_GRUPO | ALUMNOS |
|---|---|
| 1DAM | 7 |

*1 fila*

`MAX(COUNT(*))` (agregados anidados) es una extensión de Oracle. La forma estándar usa una subconsulta en el `FROM` o `FETCH FIRST 1 ROWS WITH TIES`.
{{% /details %}}

**S7.** Explica por qué esta consulta no devuelve filas y corrígela de dos formas:

```sql
SELECT nombre FROM profesor WHERE id_profesor NOT IN (SELECT id_tutor FROM grupo);
```

{{% details title="Solución S7" %}}
La subconsulta devuelve un `NULL` (el tutor de 2ASIR). Correcciones:

```sql
SELECT nombre FROM profesor WHERE id_profesor NOT IN (SELECT id_tutor FROM grupo WHERE id_tutor IS NOT NULL);

SELECT p.nombre FROM profesor p WHERE NOT EXISTS (SELECT 1 FROM grupo g WHERE g.id_tutor = p.id_profesor);
```
Ambas devuelven 7 profesores: los 12 menos los 5 tutores.
{{% /details %}}

---

## Práctica 7.5 · Múltiples selecciones y vistas

{{< practica num="7.5" tipo="Autónoma" duracion="1 sesión" nivel="2" ra="RA3: g · RA2: f" sgbd="Oracle 26ai · EDUGEST" entrega="p7_5.sql" >}}

#### Enunciado

**U1.** Lista única de todas las **localidades** en las que vive alumnado de DAM o de DAW (sin repetir).

{{% details title="Solución U1" %}}
```sql
SELECT a.localidad FROM alumno a JOIN grupo g ON g.cod_grupo = a.cod_grupo WHERE g.cod_ciclo = 'DAM'
UNION
SELECT a.localidad FROM alumno a JOIN grupo g ON g.cod_grupo = a.cod_grupo WHERE g.cod_ciclo = 'DAW'
ORDER  BY 1;
```

| LOCALIDAD |
|---|
| Alicante |
| El Campello |
| Elche |
| Mutxamel |
| San Vicente del Raspeig |
| Sant Joan d'Alacant |

*6 filas*

¿Cómo resolverías lo mismo con una sola consulta y `IN`?
{{% /details %}}

**U2.** Localidades con alumnado **tanto** de DAM **como** de DAW.

{{% details title="Solución U2" %}}
```sql
SELECT a.localidad FROM alumno a JOIN grupo g ON g.cod_grupo = a.cod_grupo WHERE g.cod_ciclo = 'DAM'
INTERSECT
SELECT a.localidad FROM alumno a JOIN grupo g ON g.cod_grupo = a.cod_grupo WHERE g.cod_ciclo = 'DAW'
ORDER  BY 1;
```

| LOCALIDAD |
|---|
| Alicante |
| Elche |
| Mutxamel |

*3 filas*

{{% /details %}}

**U3.** Códigos de módulo oficiales que están en DAM pero **no** en DAW.

{{% details title="Solución U3" %}}
```sql
SELECT codigo FROM modulo WHERE cod_ciclo = 'DAM'
MINUS
SELECT codigo FROM modulo WHERE cod_ciclo = 'DAW'
ORDER  BY 1;
```

| CODIGO |
|---|
| 0486 |
| 0488 |
| 0489 |
| 0490 |
| 0491 |

*5 filas*

{{% /details %}}

**U4.** Crea la vista `v_acta` de la [teoría](/ud07-consultas-avanzadas/ud07-teoria#7-vistas-con-composiciones) y úsala para obtener el número de APTOS, NO APTOS y NC de cada módulo de 1DAW.

{{% details title="Solución U4" %}}
```sql
SELECT cod_modulo, modulo,
       SUM(CASE WHEN calificacion = 'APTO'    THEN 1 ELSE 0 END) AS aptos,
       SUM(CASE WHEN calificacion = 'NO APTO' THEN 1 ELSE 0 END) AS no_aptos,
       SUM(CASE WHEN calificacion = 'NC'      THEN 1 ELSE 0 END) AS nc
FROM   v_acta
WHERE  cod_grupo = '1DAW'
GROUP  BY cod_modulo, modulo
ORDER  BY cod_modulo;
```

| COD_MODULO | MODULO | APTOS | NO_APTOS | NC |
|---|---|---|---|---|
| 0373 | Lenguajes de marcas y sistemas de gestión de información | 5 | 1 | 0 |
| 0483 | Sistemas informáticos | 4 | 2 | 0 |
| 0484 | Bases de datos | 6 | 0 | 0 |
| 0485 | Programación | 4 | 2 | 0 |
| 0487 | Entornos de desarrollo | 5 | 0 | 1 |

*5 filas*

{{% /details %}}

---

## Práctica 7.6 · Optimización: medir antes y después

{{< practica num="7.6" tipo="Guiada" duracion="2 sesiones" nivel="3" ra="RA3: h" sgbd="Oracle 26ai · SQL Developer (Explicar plan, Autotrace) o SQLcl" entrega="p7_6.sql + tabla de mediciones + capturas de los planes" >}}

#### Objetivo

Comprobar con mediciones reales cómo afectan los índices y la forma de escribir una consulta a su plan de ejecución y a su rendimiento.

#### Contexto

EduGest tiene muy pocos datos para notar diferencias. Simularemos el **histórico de accesos** del portal del alumnado durante varios cursos: medio millón de filas.

#### Desarrollo

{{% steps %}}

1. **Crea y llena la tabla** (conectado como `EDUGEST`). `CONNECT BY LEVEL` es un truco de Oracle para generar filas:

    ```sql
    CREATE TABLE acceso_portal (
        id_acceso   NUMBER(10)   CONSTRAINT pk_acceso_portal PRIMARY KEY,
        id_alumno   NUMBER(6)    NOT NULL,
        fecha_hora  DATE         NOT NULL,
        ip          VARCHAR2(15) NOT NULL,
        seccion     VARCHAR2(20) NOT NULL
    );

    INSERT INTO acceso_portal
    SELECT LEVEL,
           MOD(LEVEL * 7, 5000) + 1,
           DATE '2022-09-01' + MOD(LEVEL * 13, 1460) + MOD(LEVEL, 86400) / 86400,
           '10.0.' || MOD(LEVEL, 256) || '.' || MOD(LEVEL * 3, 256),
           CASE MOD(LEVEL, 5) WHEN 0 THEN 'NOTAS' WHEN 1 THEN 'FALTAS' WHEN 2 THEN 'HORARIO'
                              WHEN 3 THEN 'MENSAJES' ELSE 'PERFIL' END
    FROM   dual
    CONNECT BY LEVEL <= 500000;
    COMMIT;

    EXEC DBMS_STATS.GATHER_TABLE_STATS(USER, 'ACCESO_PORTAL');
    SET TIMING ON
    ```

2. **Consulta 1: buscar por alumno sin índice.**

    ```sql
    SELECT COUNT(*) FROM acceso_portal WHERE id_alumno = 1234;
    ```

    Obtén el plan (F10 en SQL Developer, o `EXPLAIN PLAN FOR ...` + `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);`). Anota la operación, el coste y el tiempo. Debe aparecer `TABLE ACCESS FULL`.

3. **Crea un índice** y repite la medición:

    ```sql
    CREATE INDEX ix_acceso_alumno ON acceso_portal (id_alumno);
    ```

    El plan debe cambiar a `INDEX RANGE SCAN`, con un coste mucho menor. Como solo se pide `COUNT(*)`, Oracle ni siquiera necesita leer la tabla.

4. **Consulta 2: función sobre la columna.** Compara estas dos consultas equivalentes:

    ```sql
    -- (a) Función sobre la columna fecha_hora
    SELECT COUNT(*) FROM acceso_portal WHERE TRUNC(fecha_hora) = DATE '2024-03-15';
    -- (b) Rango sobre la columna sin modificarla
    SELECT COUNT(*) FROM acceso_portal
    WHERE  fecha_hora >= DATE '2024-03-15' AND fecha_hora < DATE '2024-03-16';
    ```

    Crea `CREATE INDEX ix_acceso_fecha ON acceso_portal (fecha_hora);` y compara los planes de (a) y (b). Solo (b) puede usar el índice.

5. **Consulta 3: selectividad.** Con un índice sobre `seccion`, ¿usa Oracle el índice para `WHERE seccion = 'NOTAS'`? Esa condición devuelve el 20 % de la tabla: lo más probable es que el optimizador prefiera `TABLE ACCESS FULL`. Compruébalo y explica por qué es la decisión correcta.

6. **Consulta 4: composición.** Mide la composición con `ALUMNO` antes y después de que exista el índice `ix_acceso_alumno`:

    ```sql
    SELECT a.cod_grupo, COUNT(*) AS accesos
    FROM   acceso_portal ap JOIN alumno a ON a.id_alumno = ap.id_alumno
    GROUP  BY a.cod_grupo;
    ```

7. **Limpia** al terminar: `DROP TABLE acceso_portal PURGE;`

{{% /steps %}}

#### Comprobación

{{% comprobacion %}}
Completa la tabla de mediciones con tus datos (los valores exactos dependen de tu equipo):

| Consulta | Sin índice: operación / coste / tiempo | Con índice: operación / coste / tiempo |
|---|---|---|
| 1 · `id_alumno = 1234` | `TABLE ACCESS FULL` / … / … | `INDEX RANGE SCAN` / … / … |
| 2a · `TRUNC(fecha_hora) = ...` | | |
| 2b · rango de fechas | | |
| 3 · `seccion = 'NOTAS'` | | |
| 4 · composición con `ALUMNO` | | |

- [ ] La consulta 1 devuelve 100 accesos y su coste baja de forma clara con el índice.
- [ ] Explicas por qué 2a no usa el índice y cómo lo conseguirías sin reescribirla (índice basado en función sobre `TRUNC(fecha_hora)`).
- [ ] Explicas por qué en la consulta 3 un acceso completo puede ser mejor que el índice.

> [!WARNING]
> Las mediciones de tiempo varían entre ejecuciones porque Oracle guarda en caché los bloques leídos. Ejecuta cada consulta **dos o tres veces** y anota el tiempo de las últimas. El **coste** del plan es una estimación del optimizador, no un tiempo.
{{% /comprobacion %}}

#### Ampliación

Añade `/*+ FULL(ap) */` justo después de `SELECT` en la consulta 1 con índice y compara. Las *hints* obligan al optimizador a usar un plan concreto; en producción solo se usan cuando se ha demostrado que el optimizador se equivoca.

---

## Práctica 7.7 · Reto: el cuadro de mando

{{< practica num="7.7" tipo="Reto" duracion="2 sesiones" nivel="3" ra="RA3: c, d, e, f, g, h" sgbd="Oracle 26ai · EDUGEST" entrega="p7_7.sql + defensa oral" >}}

#### Enunciado

La dirección quiere un **cuadro de mando** con una sola consulta por indicador. Resuelve cada uno con la técnica que consideres más adecuada y justifica la elección:

1. Para cada ciclo (incluido SMR): número de grupos, de alumnos, de matrículas y nota media.
2. Los **dos** mejores alumnos de cada grupo según su nota media (pista: `RANK()` o `ROW_NUMBER()` con `PARTITION BY`).
3. Para cada profesor que imparte clase: la nota media de sus alumnos en los módulos que imparte **en los grupos en los que los imparte**. (Cuidado: la composición entre `IMPARTE` y `MATRICULA` debe usar el módulo **y** el grupo del alumno.)
4. Alumnos que han suspendido **todos** los módulos en los que están calificados.
5. Porcentaje de horas de falta justificadas sobre el total, por grupo.
6. Escribe una de las consultas anteriores de dos formas distintas (por ejemplo, subconsulta frente a composición) y compara sus planes de ejecución.

#### Comprobación

{{% comprobacion %}}
- [ ] El indicador 1 tiene 4 filas y SMR aparece con ceros.
- [ ] El indicador 3 no mezcla alumnos de otros grupos con el mismo módulo.
- [ ] Puedes defender cada consulta y explicar su plan de ejecución.

{{% details title="Pista para el indicador 4" %}}
«Todos suspendidos» equivale a «no existe ninguno aprobado» y «tiene al menos uno calificado»: `NOT EXISTS (... nota_final >= 5)` y `EXISTS (... nota_final IS NOT NULL)`. Otra forma: `GROUP BY` alumno con `HAVING MAX(nota_final) < 5`.
{{% /details %}}
{{% /comprobacion %}}

---

## Proyecto EduGest · UD07: informes

{{< practica num="EduGest-7" tipo="Proyecto" duracion="Trabajo transversal (2 semanas)" nivel="3" ra="RA3: a-h · RA2: f" sgbd="Oracle 26ai · EDUGEST" entrega="edugest/06_informes.sql + 07_vistas_informes.sql + docs/07-optimizacion.md" >}}

#### Enunciado

1. Escribe **diez informes** para EduGest que en conjunto usen: composiciones internas y externas (al menos tres tablas en alguno), consultas resumen con `HAVING`, subconsultas (una correlacionada y una con `EXISTS`), un operador de conjuntos y una función analítica.
2. Convierte los tres informes más usados en **vistas** y concede `SELECT` sobre ellas al rol adecuado de la práctica 5.7.
3. **Optimización:** elige dos de tus informes, obtén su plan de ejecución, propón una mejora (índice o reescritura) y documenta el antes y el después en `07-optimizacion.md`. Si EduGest tiene pocos datos para notar la diferencia, explícalo y apóyate en la práctica 7.6.

#### Comprobación

{{% comprobacion %}}
- [ ] Cada informe tiene un comentario con el perfil que lo usa, la pregunta que responde y el número de filas.
- [ ] Las vistas se pueden consultar desde el usuario del rol correspondiente.
- [ ] El documento de optimización incluye los planes antes y después.
{{% /comprobacion %}}
