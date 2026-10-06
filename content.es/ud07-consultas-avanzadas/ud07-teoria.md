---
title: "Consultas avanzadas"
weight: 1
bookToc: true
---

# UD07 · Consultas avanzadas: agrupamiento, composiciones, subconsultas y optimización

## Resumen del tema

La información útil casi nunca está en una sola tabla ni fila a fila. Un acta de evaluación necesita datos del alumno, del módulo y de la matrícula; un informe de jefatura necesita **resúmenes** (medias, recuentos); y muchas preguntas se expresan en función de otras («alumnos con nota superior a la media»). En esta unidad aprenderás a:

- **resumir** con funciones de grupo, `GROUP BY` y `HAVING`;
- **combinar tablas** con composiciones internas (`INNER JOIN`) y externas (`LEFT`, `RIGHT`, `FULL JOIN`);
- **anidar consultas** con subconsultas, incluidas las correlacionadas y `EXISTS`;
- **combinar resultados** con `UNION`, `INTERSECT` y `MINUS`;
- **optimizar** consultas leyendo planes de ejecución.

{{< ra "RA3:a,c,d,e,f,g,h" "RA2:f" >}}

### Objetivos de aprendizaje

Al terminar esta unidad serás capaz de:

- Realizar consultas resumen con funciones de agregado y agrupaciones.
- Componer varias tablas con composiciones internas y externas, y elegir la adecuada.
- Escribir subconsultas escalares, de varias filas y correlacionadas.
- Combinar los resultados de varias consultas.
- Interpretar un plan de ejecución y aplicar criterios de optimización.

> [!TIP]
> Igual que en la UD06, ejecuta `ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY';` y trabaja sobre el esquema de referencia EDUGEST con los datos originales. Todos los resultados que aparecen aquí se han calculado sobre esos datos.

---

## 1. Consultas resumen

### 1.1 Funciones de agregado

Las funciones de agregado (o de grupo) reciben **muchas filas** y devuelven **un único valor**.

| Función | Devuelve | Trato de los `NULL` |
|---|---|---|
| `COUNT(*)` | Número de filas | Cuenta todas las filas |
| `COUNT(columna)` | Número de valores **no nulos** | Los ignora |
| `COUNT(DISTINCT columna)` | Número de valores distintos no nulos | Los ignora |
| `SUM(expr)` | Suma | Los ignora |
| `AVG(expr)` | Media aritmética | Los ignora (¡no cuentan como 0!) |
| `MIN(expr)` / `MAX(expr)` | Mínimo / máximo (también para textos y fechas) | Los ignora |

```sql
SELECT COUNT(*)                   AS matriculas,
       COUNT(nota_final)          AS calificadas,
       COUNT(DISTINCT id_alumno)  AS alumnos,
       ROUND(AVG(nota_final), 2)  AS media,
       MIN(nota_final)            AS minima,
       MAX(nota_final)            AS maxima
FROM   matricula;
```


| MATRICULAS | CALIFICADAS | ALUMNOS | MEDIA | MINIMA | MAXIMA |
|---|---|---|---|---|---|
| 143 | 137 | 29 | 6.36 | 1.5 | 10 |

*1 fila*


> [!WARNING]
> `AVG(nota_final)` calcula la media de las **137 matrículas calificadas**, no de las 143. Si quieres que las no calificadas cuenten como 0, debes decirlo explícitamente: `AVG(NVL(nota_final, 0))`. Son dos preguntas distintas.

### 1.2 Agrupar con GROUP BY

`GROUP BY` divide las filas en **grupos** que comparten el mismo valor en las columnas indicadas, y las funciones de agregado se calculan **para cada grupo**.

```sql
SELECT cod_ciclo, curso, COUNT(*) AS modulos, SUM(horas) AS horas
FROM   modulo
GROUP  BY cod_ciclo, curso
ORDER  BY cod_ciclo, curso;
```


| COD_CICLO | CURSO | MODULOS | HORAS |
|---|---|---|---|
| ASIR | 1 | 5 | 768 |
| DAM | 1 | 5 | 800 |
| DAM | 2 | 5 | 520 |
| DAW | 1 | 5 | 800 |
| DAW | 2 | 4 | 500 |

*5 filas*


> [!IMPORTANT]
> **Regla de oro del `GROUP BY`:** en el `SELECT` de una consulta agrupada solo pueden aparecer (1) las columnas del `GROUP BY` y (2) funciones de agregado. Si no, Oracle devuelve `ORA-00979: not a GROUP BY expression`. Si usas una función de agregado sin `GROUP BY` junto a una columna normal, el error es `ORA-00937: not a single-group group function`.

### 1.3 Filtrar grupos con HAVING

`WHERE` filtra **filas antes** de agrupar; `HAVING` filtra **grupos después** de agrupar, y puede usar funciones de agregado.

```sql
-- Matrículas con alguna falta y total de horas de falta, solo si superan 2 horas
SELECT id_matricula, COUNT(*) AS faltas, SUM(horas) AS horas_falta
FROM   falta_asistencia
WHERE  justificada = 'N'          -- antes de agrupar: solo las no justificadas
GROUP  BY id_matricula
HAVING SUM(horas) > 2             -- después de agrupar
ORDER  BY horas_falta DESC, id_matricula;
```


| ID_MATRICULA | FALTAS | HORAS_FALTA |
|---|---|---|
| 10003 | 1 | 3 |
| 10028 | 1 | 3 |
| 10034 | 1 | 3 |
| 10040 | 1 | 3 |
| 10044 | 1 | 3 |
| 10045 | 1 | 3 |
| 10051 | 1 | 3 |
| 10092 | 1 | 3 |
| 10102 | 2 | 3 |
| 10114 | 1 | 3 |
| 10133 | 1 | 3 |

*11 filas*


```mermaid
flowchart LR
    A[FROM<br/>todas las filas] --> B[WHERE<br/>filtra filas] --> C[GROUP BY<br/>forma grupos] --> D[HAVING<br/>filtra grupos] --> E[SELECT<br/>calcula columnas] --> F[ORDER BY]
```

> [!TIP]
> En **Oracle 23ai** y posteriores puedes usar en `GROUP BY` y `HAVING` el **alias** o la **posición** de una columna del `SELECT` (`GROUP BY 1, 2`). Es una extensión cómoda, pero no estándar: en 19c y en otros SGBD da error.

---

## 2. Composiciones internas (INNER JOIN)

### 2.1 Idea intuitiva

Una **composición** (*join*) combina filas de dos tablas que están relacionadas, normalmente a través de una **clave ajena**. Partimos de dos tablas pequeñas:

**GRUPO** (extracto)

| cod_grupo | turno | id_tutor |
|---|---|---|
| 1DAM | M | 103 |
| 1DAW | T | 106 |
| 2ASIR | M | (null) |

**PROFESOR** (extracto)

| id_profesor | nombre |
|---|---|
| 103 | Lucía |
| 106 | Raúl |
| 108 | Pablo |

La composición interna `GRUPO JOIN PROFESOR ON grupo.id_tutor = profesor.id_profesor` empareja cada grupo con el profesor cuyo identificador coincide con su tutor:

| cod_grupo | turno | id_tutor | id_profesor | nombre |
|---|---|---|---|---|
| 1DAM | M | 103 | 103 | Lucía |
| 1DAW | T | 106 | 106 | Raúl |

2ASIR **no aparece** (no tiene tutor) y Pablo **tampoco** (no tutoriza ningún grupo). Una composición interna solo devuelve las filas que **tienen pareja** en las dos tablas.

> [!NOTE]
> Sin condición de composición se obtiene el **producto cartesiano**: cada fila de una tabla combinada con **todas** las de la otra (3 × 3 = 9 filas). Casi nunca es lo que se quiere: si una consulta con varias tablas devuelve muchísimas filas, revisa si te falta una condición de composición.

### 2.2 Sintaxis

{{< sgbd "SQL estándar · Oracle 26ai" >}}

```sql
SELECT g.cod_grupo, g.turno, p.nombre, p.apellidos
FROM   grupo g
       INNER JOIN profesor p ON p.id_profesor = g.id_tutor
ORDER  BY g.cod_grupo;
```


| COD_GRUPO | TURNO | NOMBRE | APELLIDOS |
|---|---|---|---|
| 1ASIR | M | Elena | Brotons Sala |
| 1DAM | M | Lucía | Ferrándiz Mora |
| 1DAW | T | Raúl | Cano Vidal |
| 2DAM | M | Andrés | Navarro Ruiz |
| 2DAW | T | Nuria | Gómez Pérez |

*5 filas*


| Elemento | Significado |
|---|---|
| `grupo g` | `g` es un **alias de tabla**. Acorta la consulta y es obligatorio cuando una tabla aparece dos veces |
| `INNER JOIN` | Composición interna. `INNER` es opcional: `JOIN` a secas es lo mismo |
| `ON p.id_profesor = g.id_tutor` | Condición de composición: normalmente **clave ajena = clave primaria** |
| `g.cod_grupo` | Columna **cualificada** con el alias. Obligatorio si el nombre existe en ambas tablas (si no, `ORA-00918: column ambiguously defined`) |

Variantes:

```sql
-- USING: cuando la columna se llama igual en las dos tablas
SELECT cod_ciclo, c.nombre AS ciclo, m.nombre AS modulo
FROM   modulo m JOIN ciclo c USING (cod_ciclo);

-- Sintaxis antigua (anterior a SQL-92): la condición va en el WHERE
SELECT g.cod_grupo, p.nombre
FROM   grupo g, profesor p
WHERE  p.id_profesor = g.id_tutor;
```

> [!WARNING]
> Verás mucho código con la **sintaxis antigua**. Funciona, pero mezcla las condiciones de composición con los filtros y, si olvidas una, obtienes un producto cartesiano sin ningún aviso. Usa siempre `JOIN ... ON`. Evita también `NATURAL JOIN`: compone por **todas** las columnas que se llamen igual, y en EduGest `ALUMNO` y `MODULO` tienen las dos una columna `nombre`.

### 2.3 Composición de varias tablas

Cada `JOIN` añade una tabla al resultado. Para obtener el **acta** de un módulo necesitamos `MATRICULA`, `ALUMNO` y `MODULO`:

```sql
SELECT a.apellidos || ', ' || a.nombre AS alumno,
       mo.codigo, mo.nombre AS modulo, m.nota_final
FROM   matricula m
       JOIN alumno a  ON a.id_alumno  = m.id_alumno
       JOIN modulo mo ON mo.id_modulo = m.id_modulo
WHERE  mo.codigo = '0484' AND mo.cod_ciclo = 'DAW'
ORDER  BY alumno;
```


| ALUMNO | CODIGO | MODULO | NOTA_FINAL |
|---|---|---|---|
| Alemany Pérez, Daniel | 0484 | Bases de datos | 7.25 |
| Espí Marco, Julia | 0484 | Bases de datos | 5.5 |
| Iborra Alemany, Jorge | 0484 | Bases de datos | 6 |
| Soriano Domènech, Manuel | 0484 | Bases de datos | 6 |
| Torregrosa Planelles, Alba | 0484 | Bases de datos | 5.75 |
| Valero Cerdá, Carla | 0484 | Bases de datos | 5 |

*6 filas*


> [!TIP]
> **Método para componer muchas tablas.** Dibuja (o mira) el diagrama relacional y traza el **camino** de claves ajenas entre las tablas que necesitas. Cada flecha del camino es un `JOIN ... ON fk = pk`. Para ir de `FALTA_ASISTENCIA` al nombre del `CICLO`: falta → matrícula → módulo → ciclo.

### 2.4 Autocomposición

Una tabla puede componerse **consigo misma** usando dos alias. Ejemplo: módulos con el mismo código oficial en distintos ciclos.

```sql
SELECT m1.codigo, m1.nombre, m1.cod_ciclo AS ciclo_1, m2.cod_ciclo AS ciclo_2
FROM   modulo m1
       JOIN modulo m2 ON m2.codigo = m1.codigo
                     AND m2.cod_ciclo > m1.cod_ciclo   -- evita parejas repetidas e iguales
ORDER  BY m1.codigo, ciclo_1, ciclo_2;
```


| CODIGO | NOMBRE | CICLO_1 | CICLO_2 |
|---|---|---|---|
| 0373 | Lenguajes de marcas y sistemas de gestión de información | ASIR | DAM |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | ASIR | DAW |
| 0373 | Lenguajes de marcas y sistemas de gestión de información | DAM | DAW |
| 0483 | Sistemas informáticos | DAM | DAW |
| 0484 | Bases de datos | DAM | DAW |
| 0485 | Programación | DAM | DAW |
| 0487 | Entornos de desarrollo | DAM | DAW |

*7 filas*


### 2.5 Composición y agrupamiento

Las composiciones se combinan con `GROUP BY` para obtener resúmenes por entidades relacionadas:

```sql
-- Nota media por grupo
SELECT a.cod_grupo,
       COUNT(*)                     AS matriculas,
       ROUND(AVG(m.nota_final), 2)  AS nota_media,
       SUM(CASE WHEN m.nota_final >= 5 THEN 1 ELSE 0 END) AS aprobadas
FROM   matricula m
       JOIN alumno a ON a.id_alumno = m.id_alumno
GROUP  BY a.cod_grupo
ORDER  BY a.cod_grupo;
```


| COD_GRUPO | MATRICULAS | NOTA_MEDIA | APROBADAS |
|---|---|---|---|
| 1ASIR | 25 | 7.07 | 21 |
| 1DAM | 35 | 6.4 | 27 |
| 1DAW | 30 | 6.19 | 24 |
| 2DAM | 33 | 6.17 | 23 |
| 2DAW | 20 | 5.93 | 15 |

*5 filas*


> [!NOTE]
> `SUM(CASE WHEN condición THEN 1 ELSE 0 END)` es un patrón muy útil: **cuenta las filas que cumplen una condición** dentro de cada grupo, sin necesidad de otra consulta.

---

## 3. Composiciones externas (OUTER JOIN)

### 3.1 Cuándo se necesitan

Una composición interna **descarta** las filas sin pareja. Muchas preguntas, en cambio, necesitan conservarlas: «todos los departamentos **con** su número de profesores, **incluidos los que no tienen ninguno**».

| Tipo | Conserva |
|---|---|
| `LEFT [OUTER] JOIN` | Todas las filas de la tabla de la **izquierda**; las columnas de la derecha quedan a `NULL` si no hay pareja |
| `RIGHT [OUTER] JOIN` | Todas las filas de la tabla de la **derecha** |
| `FULL [OUTER] JOIN` | Todas las filas de **ambas** tablas |

Con el ejemplo del apartado 2.1:

| Composición | Filas resultantes |
|---|---|
| `grupo g JOIN profesor p` | 1DAM–Lucía, 1DAW–Raúl |
| `grupo g LEFT JOIN profesor p` | 1DAM–Lucía, 1DAW–Raúl, **2ASIR–(null)** |
| `grupo g RIGHT JOIN profesor p` | 1DAM–Lucía, 1DAW–Raúl, **(null)–Pablo** |
| `grupo g FULL JOIN profesor p` | 1DAM–Lucía, 1DAW–Raúl, 2ASIR–(null), (null)–Pablo |

### 3.2 Ejemplos

```sql
-- Todos los grupos con su tutor (aunque no tengan)
SELECT g.cod_grupo, g.turno,
       NVL2(p.id_profesor, p.nombre || ' ' || p.apellidos, '(sin tutor)') AS tutor
FROM   grupo g
       LEFT JOIN profesor p ON p.id_profesor = g.id_tutor
ORDER  BY g.cod_grupo;
```


| COD_GRUPO | TURNO | TUTOR |
|---|---|---|
| 1ASIR | M | Elena Brotons Sala |
| 1DAM | M | Lucía Ferrándiz Mora |
| 1DAW | T | Raúl Cano Vidal |
| 2ASIR | M | (sin tutor) |
| 2DAM | M | Andrés Navarro Ruiz |
| 2DAW | T | Nuria Gómez Pérez |

*6 filas*


> [!CAUTION]
> **Particularidad de Oracle:** al concatenar con `||`, Oracle trata `NULL` como cadena vacía. Sin el `NVL2`, la fila de 2ASIR mostraría un espacio en blanco (`NULL || ' ' || NULL` = `' '`), no `NULL`. En otros SGBD la concatenación con `NULL` da `NULL`.

```sql
-- Número de profesores por departamento, incluidos los que no tienen
SELECT d.id_departamento, d.nombre, COUNT(p.id_profesor) AS profesores
FROM   departamento d
       LEFT JOIN profesor p ON p.id_departamento = d.id_departamento
GROUP  BY d.id_departamento, d.nombre
ORDER  BY d.id_departamento;
```


| ID_DEPARTAMENTO | NOMBRE | PROFESORES |
|---|---|---|
| 1 | Informática y Comunicaciones | 8 |
| 2 | Formación y Orientación Laboral | 2 |
| 3 | Inglés | 1 |
| 4 | Matemáticas | 0 |
| 5 | Administración y Gestión | 1 |

*5 filas*


> [!IMPORTANT]
> Fíjate en `COUNT(p.id_profesor)` y **no** `COUNT(*)`. En la fila de Matemáticas, la composición externa genera una fila con `p.id_profesor` a `NULL`: `COUNT(*)` la contaría (1) y `COUNT(p.id_profesor)` no (0).

### 3.3 Buscar filas sin pareja (anti-composición)

Una composición externa seguida de `IS NULL` encuentra las filas que **no** tienen correspondencia:

```sql
-- Profesorado que no imparte ningún módulo
SELECT p.id_profesor, p.nombre, p.apellidos
FROM   profesor p
       LEFT JOIN imparte i ON i.id_profesor = p.id_profesor
WHERE  i.id_profesor IS NULL
ORDER  BY p.id_profesor;
```


| ID_PROFESOR | NOMBRE | APELLIDOS |
|---|---|---|
| 108 | Pablo | Lillo Martí |
| 109 | Carmen | Ortiz Llorca |
| 110 | Sergio | Ramos Climent |
| 111 | Laura | Vicent Ribes |
| 112 | David | Esteve Juan |

*5 filas*


> [!WARNING]
> **Error muy frecuente:** poner en el `WHERE` una condición sobre la tabla «opcional» de una composición externa. `... LEFT JOIN imparte i ON ... WHERE i.curso_academico = '2025-26'` elimina las filas en las que `i` es `NULL` y convierte la composición en interna. Las condiciones sobre la tabla opcional van **en el `ON`**: `LEFT JOIN imparte i ON i.id_profesor = p.id_profesor AND i.curso_academico = '2025-26'`.

{{% details title="Sintaxis antigua de Oracle para composiciones externas: (+)" %}}
En código antiguo de Oracle verás el operador `(+)` en el `WHERE`, colocado en el lado de la tabla **opcional**:

```sql
SELECT g.cod_grupo, p.nombre
FROM   grupo g, profesor p
WHERE  p.id_profesor (+) = g.id_tutor;    -- equivale a grupo LEFT JOIN profesor
```

Es propio de Oracle, no permite `FULL JOIN` y Oracle recomienda no usarlo. Reconócelo para poder mantener código heredado, pero escribe siempre `LEFT JOIN`.
{{% /details %}}

---

## 4. Subconsultas

Una **subconsulta** es una consulta escrita dentro de otra, entre paréntesis. Permite expresar preguntas que dependen de un valor que hay que calcular antes.

### 4.1 Subconsulta escalar (devuelve un valor)

```sql
-- Módulos con más horas que la media de todos los módulos
SELECT codigo, nombre, cod_ciclo, horas
FROM   modulo
WHERE  horas > (SELECT AVG(horas) FROM modulo)
ORDER  BY horas DESC, codigo, cod_ciclo;
```


| CODIGO | NOMBRE | COD_CICLO | HORAS |
|---|---|---|---|
| 0485 | Programación | DAM | 256 |
| 0485 | Programación | DAW | 256 |
| 0369 | Implantación de sistemas operativos | ASIR | 224 |
| 0370 | Planificación y administración de redes | ASIR | 192 |
| 0372 | Gestión de bases de datos | ASIR | 160 |
| 0483 | Sistemas informáticos | DAM | 160 |
| 0483 | Sistemas informáticos | DAW | 160 |
| 0484 | Bases de datos | DAM | 160 |
| 0484 | Bases de datos | DAW | 160 |
| 0613 | Desarrollo web en entorno servidor | DAW | 160 |

*10 filas*


La media de horas es `(SELECT AVG(horas) FROM modulo)` = 141.17. Si una subconsulta usada con `=`, `>`, `<`... devuelve **más de una fila**, Oracle da el error `ORA-01427: single-row subquery returns more than one row`.

### 4.2 Subconsultas de varias filas: IN, ANY, ALL

```sql
-- Alumnado matriculado en algún módulo impartido por Marta Soler (id 101)
SELECT nombre, apellidos, cod_grupo
FROM   alumno
WHERE  id_alumno IN (SELECT m.id_alumno
                     FROM   matricula m
                            JOIN imparte i ON i.id_modulo = m.id_modulo
                     WHERE  i.id_profesor = 101)
ORDER  BY cod_grupo, apellidos, nombre;
```


| NOMBRE | APELLIDOS | COD_GRUPO |
|---|---|---|
| Pablo | Amorós Carbonell | 1ASIR |
| Diego | Iborra Torregrosa | 1ASIR |
| Aitana | Pascual Brotons | 1ASIR |
| Víctor | Tomás Guillem | 1ASIR |
| Álex | Tomás Vidal | 1ASIR |
| Andrea | Brotons Soriano | 1DAM |
| Tomás | Cerdá Pérez | 1DAM |
| Adrián | Ferri Baeza | 1DAM |
| Paula | Ferri Baeza | 1DAM |
| Rubén | Iborra Ferri | 1DAM |
| Valeria | Quiles Marco | 1DAM |
| Noelia | Verdú Espí | 1DAM |
| Daniel | Alemany Pérez | 1DAW |
| Julia | Espí Marco | 1DAW |
| Jorge | Iborra Alemany | 1DAW |
| Manuel | Soriano Domènech | 1DAW |
| Alba | Torregrosa Planelles | 1DAW |
| Carla | Valero Cerdá | 1DAW |

*18 filas*


| Operador | Significado |
|---|---|
| `IN (subconsulta)` | Igual a alguno de los valores |
| `NOT IN (subconsulta)` | Distinto de todos (¡cuidado con los `NULL`!) |
| `> ANY (subconsulta)` | Mayor que **alguno** (mayor que el mínimo) |
| `> ALL (subconsulta)` | Mayor que **todos** (mayor que el máximo) |

> [!CAUTION]
> Si la subconsulta de un `NOT IN` devuelve **algún `NULL`**, la consulta exterior no devuelve **ninguna fila** (UD06, práctica 6.3). Ejemplo: `WHERE id_profesor NOT IN (SELECT id_tutor FROM grupo)` devuelve 0 filas porque 2ASIR tiene `id_tutor` a `NULL`. Usa `NOT EXISTS` o filtra los nulos en la subconsulta.

### 4.3 Subconsultas correlacionadas y EXISTS

Una subconsulta **correlacionada** hace referencia a una columna de la consulta exterior: se evalúa, conceptualmente, **una vez por cada fila** exterior.

```sql
-- Matrículas cuya nota supera la media de SU módulo
SELECT m.id_matricula, m.id_modulo, m.nota_final
FROM   matricula m
WHERE  m.nota_final > (SELECT AVG(m2.nota_final)
                       FROM   matricula m2
                       WHERE  m2.id_modulo = m.id_modulo)   -- correlación
AND    m.id_modulo = 2
ORDER  BY m.nota_final DESC, m.id_matricula;
```


| ID_MATRICULA | ID_MODULO | NOTA_FINAL |
|---|---|---|
| 10012 | 2 | 8 |
| 10017 | 2 | 6.5 |
| 10032 | 2 | 6.5 |

*3 filas*


`EXISTS` comprueba si una subconsulta devuelve **al menos una fila**. Es la forma más clara y segura de expresar «que tenga» o «que no tenga»:

```sql
-- Profesorado que no imparte nada (equivalente a la anti-composición del 3.3)
SELECT p.id_profesor, p.nombre, p.apellidos
FROM   profesor p
WHERE  NOT EXISTS (SELECT 1 FROM imparte i WHERE i.id_profesor = p.id_profesor)
ORDER  BY p.id_profesor;
```


| ID_PROFESOR | NOMBRE | APELLIDOS |
|---|---|---|
| 108 | Pablo | Lillo Martí |
| 109 | Carmen | Ortiz Llorca |
| 110 | Sergio | Ramos Climent |
| 111 | Laura | Vicent Ribes |
| 112 | David | Esteve Juan |

*5 filas*


### 4.4 Subconsultas en FROM y cláusula WITH

Una subconsulta en el `FROM` actúa como una tabla temporal (**vista en línea**). La cláusula `WITH` (*common table expression*, CTE) hace lo mismo con un nombre, y es más legible:

```sql
-- Grupos cuya nota media supera la media general
WITH medias AS (
    SELECT a.cod_grupo, AVG(m.nota_final) AS media
    FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
    GROUP  BY a.cod_grupo
)
SELECT cod_grupo, ROUND(media, 2) AS media
FROM   medias
WHERE  media > (SELECT AVG(nota_final) FROM matricula)
ORDER  BY media DESC;
```


| COD_GRUPO | MEDIA |
|---|---|
| 1ASIR | 7.07 |
| 1DAM | 6.4 |

*2 filas*


### 4.5 Subconsultas en el SELECT

```sql
-- Número de alumnos de cada grupo
SELECT g.cod_grupo,
       (SELECT COUNT(*) FROM alumno a WHERE a.cod_grupo = g.cod_grupo) AS alumnos
FROM   grupo g
ORDER  BY g.cod_grupo;
```


| COD_GRUPO | ALUMNOS |
|---|---|
| 1ASIR | 5 |
| 1DAM | 7 |
| 1DAW | 6 |
| 2ASIR | 0 |
| 2DAM | 6 |
| 2DAW | 5 |

*6 filas*


---

## 5. Múltiples selecciones: operadores de conjuntos

Los operadores de conjuntos combinan los **resultados** de dos o más consultas (RA3.g). Las consultas deben devolver el **mismo número de columnas** con **tipos compatibles**; los nombres de columna del resultado son los de la primera consulta.

| Operador | Resultado | Duplicados |
|---|---|---|
| `UNION` | Filas de una **o** de otra | Los elimina |
| `UNION ALL` | Filas de una **y** de otra, todas | Los conserva (más rápido) |
| `INTERSECT` | Filas que están en **las dos** | Los elimina |
| `MINUS` (Oracle) / `EXCEPT` (estándar, Oracle 21c+) | Filas de la primera que **no** están en la segunda | Los elimina |

```sql
-- Directorio de correos de todo el centro: profesorado y alumnado
SELECT 'Profesorado' AS colectivo, apellidos || ', ' || nombre AS persona, email
FROM   profesor WHERE id_departamento = 2
UNION ALL
SELECT 'Alumnado', apellidos || ', ' || nombre, email
FROM   alumno   WHERE cod_grupo = '2DAW'
ORDER  BY colectivo, persona;
```


| COLECTIVO | PERSONA | EMAIL |
|---|---|---|
| Alumnado | Amorós Guillem, Sara | saraamoros23@alu.edugest.es |
| Alumnado | Carbonell Soriano, Elena | elenacarbonell21@alu.edugest.es |
| Alumnado | Planelles Marco, Sofía | sofiaplanelles22@alu.edugest.es |
| Alumnado | Sala Brotons, Mateo | mateosala20@alu.edugest.es |
| Alumnado | Verdú Castelló, Nicolás | nicolasverdu24@alu.edugest.es |
| Profesorado | Ortiz Llorca, Carmen | cortiz@edugest.es |
| Profesorado | Ramos Climent, Sergio | sramos@edugest.es |

*7 filas*


```sql
-- Profesores que son tutores Y además imparten en 2º curso
SELECT id_tutor FROM grupo WHERE id_tutor IS NOT NULL
INTERSECT
SELECT i.id_profesor FROM imparte i JOIN grupo g ON g.cod_grupo = i.cod_grupo WHERE g.curso = 2
ORDER  BY 1;
```


| ID_TUTOR |
|---|
| 103 |
| 104 |
| 105 |
| 106 |
| 107 |

*5 filas*


```sql
-- Localidades donde vive alumnado pero que no tienen ningún alumno de DAM
SELECT localidad FROM alumno
MINUS
SELECT a.localidad FROM alumno a JOIN grupo g ON g.cod_grupo = a.cod_grupo WHERE g.cod_ciclo = 'DAM'
ORDER  BY 1;
```


| LOCALIDAD |
|---|
| El Campello |

*1 fila*


> [!NOTE]
> `ORDER BY` solo puede aparecer **una vez, al final** de toda la combinación, y afecta al resultado completo.

---

## 6. Funciones analíticas (ampliación)

Las funciones analíticas calculan valores **sobre un conjunto de filas relacionadas sin agruparlas**: cada fila conserva su detalle. Son muy útiles para rankings y comparaciones.

```sql
-- Ranking de notas dentro de cada módulo de 1DAM (el módulo 2 es Bases de datos de DAM)
SELECT m.id_modulo, m.id_alumno, m.nota_final,
       RANK()       OVER (PARTITION BY m.id_modulo ORDER BY m.nota_final DESC) AS puesto,
       ROUND(AVG(m.nota_final) OVER (PARTITION BY m.id_modulo), 2)            AS media_modulo
FROM   matricula m
WHERE  m.id_modulo = 2 AND m.nota_final IS NOT NULL
ORDER  BY puesto, m.id_alumno;
```


| ID_MODULO | ID_ALUMNO | NOTA_FINAL | PUESTO | MEDIA_MODULO |
|---|---|---|---|---|
| 2 | 3 | 8 | 1 | 5.93 |
| 2 | 4 | 6.5 | 2 | 5.93 |
| 2 | 7 | 6.5 | 2 | 5.93 |
| 2 | 5 | 5.75 | 4 | 5.93 |
| 2 | 6 | 5.25 | 5 | 5.93 |
| 2 | 1 | 4.75 | 6 | 5.93 |
| 2 | 2 | 4.75 | 6 | 5.93 |

*7 filas*


| Función | Uso |
|---|---|
| `ROW_NUMBER()` | Número de fila consecutivo (sin empates) |
| `RANK()` / `DENSE_RANK()` | Puesto con empates (con o sin huecos) |
| `SUM(...) OVER (...)`, `AVG(...) OVER (...)` | Totales y medias por partición, o acumulados con `ORDER BY` |
| `LAG(col)` / `LEAD(col)` | Valor de la fila anterior o siguiente |

---

## 7. Vistas con composiciones

Las consultas complejas que se usan a menudo se guardan como **vistas** (RA2.f). Así, quien consulta no necesita conocer los `JOIN`:

```sql
CREATE OR REPLACE VIEW v_acta AS
SELECT mo.cod_ciclo, mo.codigo AS cod_modulo, mo.nombre AS modulo,
       m.curso_academico, a.cod_grupo, a.nia,
       a.apellidos || ', ' || a.nombre AS alumno,
       m.convocatoria, m.nota_final,
       CASE WHEN m.nota_final IS NULL THEN 'NC'
            WHEN m.nota_final >= 5    THEN 'APTO'
            ELSE 'NO APTO' END AS calificacion
FROM   matricula m
       JOIN alumno a  ON a.id_alumno  = m.id_alumno
       JOIN modulo mo ON mo.id_modulo = m.id_modulo;

SELECT alumno, nota_final, calificacion
FROM   v_acta
WHERE  cod_modulo = '0484' AND cod_ciclo = 'DAM'
ORDER  BY alumno;
```

---

## 8. Optimización de consultas

### 8.1 Cómo ejecuta Oracle una consulta

Cuando envías una consulta, el **optimizador** de Oracle genera varios **planes de ejecución** posibles (qué índices usar, en qué orden componer las tablas, con qué algoritmo) y elige el de menor **coste estimado**, basándose en las **estadísticas** de las tablas (número de filas, valores distintos...).

### 8.2 Ver el plan de ejecución

{{< tabs >}}
{{% tab "SQL" %}}
```sql
EXPLAIN PLAN FOR
SELECT * FROM alumno WHERE apellidos = 'Belda Iborra';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```
{{% /tab %}}
{{% tab "SQL Developer" %}}
Escribe la consulta en la hoja de trabajo y pulsa **F10** (*Explicar plan*) o el botón de *Autotrace* (**F6**), que además ejecuta la consulta y muestra las estadísticas reales (bloques leídos, filas).
{{% /tab %}}
{{< /tabs >}}

Operaciones más habituales que verás en un plan:

| Operación | Significado | ¿Es mala? |
|---|---|---|
| `TABLE ACCESS FULL` | Lee **todos** los bloques de la tabla | En tablas pequeñas o si se devuelve gran parte de la tabla, es lo correcto. En tablas grandes con filtros muy selectivos, indica que falta un índice o que no se puede usar |
| `INDEX UNIQUE SCAN` | Busca un valor en un índice único (PK, UNIQUE) | Ideal para obtener una fila |
| `INDEX RANGE SCAN` | Recorre un rango de un índice | Eficiente para filtros selectivos |
| `TABLE ACCESS BY INDEX ROWID` | Lee la fila a partir del `ROWID` obtenido en el índice | Normal tras un acceso por índice |
| `NESTED LOOPS` | Para cada fila de una tabla, busca sus parejas en la otra | Bueno con pocas filas y un índice en la columna de composición |
| `HASH JOIN` | Construye una tabla *hash* con una tabla y recorre la otra | Bueno para composiciones de muchas filas |
| `SORT ORDER BY`, `HASH GROUP BY` | Ordenaciones y agrupaciones | Consumen memoria; evita las innecesarias |

### 8.3 Criterios de optimización

| # | Criterio | Mal | Mejor |
|---|---|---|---|
| 1 | Pide solo las columnas necesarias | `SELECT *` | `SELECT nia, apellidos` |
| 2 | Filtra lo antes posible y con condiciones **selectivas** | Filtrar en la aplicación | `WHERE` en la consulta |
| 3 | No apliques funciones a columnas indexadas en el `WHERE` | `WHERE UPPER(apellidos) = 'BELDA IBORRA'` | `WHERE apellidos = 'Belda Iborra'`, o un índice basado en función |
| 4 | Evita conversiones implícitas | `WHERE nia = 10450037` (`nia` es `CHAR`) | `WHERE nia = '10450037'` |
| 5 | `LIKE` con comodín al principio no usa el índice | `LIKE '%Iborra'` | `LIKE 'Iborra%'` |
| 6 | Indexa las claves ajenas usadas en `JOIN` | Sin índice en `matricula.id_modulo` | `CREATE INDEX ix_matricula_modulo ...` |
| 7 | `UNION ALL` si no hay duplicados que eliminar | `UNION` | `UNION ALL` |
| 8 | `EXISTS` en lugar de `IN` con subconsultas que devuelven muchas filas, y `NOT EXISTS` en lugar de `NOT IN` | `NOT IN (subconsulta)` | `NOT EXISTS (...)` |
| 9 | Evita `DISTINCT` para «arreglar» duplicados de un `JOIN` mal hecho | `SELECT DISTINCT ...` | Revisa la condición de composición |
| 10 | Mantén las estadísticas actualizadas | — | `EXEC DBMS_STATS.GATHER_TABLE_STATS(USER, 'MATRICULA');` |

> [!IMPORTANT]
> **Optimizar es medir.** Con los pocos datos de EduGest, casi todos los planes serán `TABLE ACCESS FULL` porque leer una tabla de 32 filas es más barato que usar un índice. Para comparar de verdad, la [práctica 7.6](/ud07-consultas-avanzadas/ud07-practicas#práctica-76--optimización-medir-antes-y-después) genera una tabla con cientos de miles de filas y compara el plan y el tiempo **antes y después** de cada mejora.

---

## 9. Errores frecuentes

| Error | Causa | Solución |
|---|---|---|
| `ORA-00979: not a GROUP BY expression` | Columna en el `SELECT` que no está en el `GROUP BY` | Añádela al `GROUP BY` o usa una función de agregado |
| `ORA-00934: group function is not allowed here` | Función de agregado en el `WHERE` | Usa `HAVING` |
| `ORA-00918: column ambiguously defined` | Columna que existe en dos tablas sin alias | Cualifícala: `a.nombre` |
| `ORA-01427: single-row subquery returns more than one row` | Subconsulta con `=` que devuelve varias filas | Usa `IN` o revisa la subconsulta |
| Demasiadas filas | Falta una condición de composición (producto cartesiano) | Comprueba que hay un `JOIN ... ON` por cada tabla añadida |
| Faltan filas | `JOIN` interno donde hacía falta uno externo, o condición sobre la tabla opcional en el `WHERE` | `LEFT JOIN` con la condición en el `ON` |
| Recuentos de 1 en lugar de 0 | `COUNT(*)` con composición externa | `COUNT(columna_de_la_tabla_opcional)` |

---

## 10. Resumen

- Las **funciones de agregado** resumen filas; `GROUP BY` forma grupos; `HAVING` filtra grupos y `WHERE` filtra filas.
- Las **composiciones internas** devuelven solo las filas con pareja; las **externas** conservan también las que no la tienen.
- Las **subconsultas** pueden devolver un valor, varias filas o actuar como tabla. Las **correlacionadas** dependen de la fila exterior. `EXISTS` y `NOT EXISTS` son la forma segura de comprobar existencia.
- `UNION`, `UNION ALL`, `INTERSECT` y `MINUS` combinan resultados de varias consultas.
- El **plan de ejecución** muestra cómo se ejecuta una consulta. Optimizar significa leer menos datos: buenos índices, condiciones selectivas y sin funciones sobre columnas indexadas.

---

## 11. Autoevaluación

{{< quiz >}}
- q: "Una tabla tiene 10 filas y la columna `nota` vale NULL en 2 de ellas. ¿Qué devuelven `COUNT(*)` y `COUNT(nota)`?"
  options: ["10 y 10", "10 y 8", "8 y 8", "8 y 10"]
  answer: 1
  explain: "`COUNT(*)` cuenta filas; `COUNT(columna)` solo cuenta los valores no nulos."
- q: "¿Dónde se escribe la condición «grupos con más de 5 alumnos»?"
  options: ["En el WHERE", "En el HAVING", "En el ON", "En el ORDER BY"]
  answer: 1
  explain: "Es una condición sobre el resultado de una función de agregado (`COUNT(*) > 5`), que solo existe después de agrupar."
- q: "¿Qué devuelve `departamento d JOIN profesor p ON p.id_departamento = d.id_departamento` para el departamento de Matemáticas, que no tiene profesores?"
  options: ["Una fila con los datos del profesor a NULL", "Ninguna fila", "Un error", "Una fila por cada profesor del centro"]
  answer: 1
  explain: "La composición interna descarta las filas sin pareja. Para conservarlo hace falta `LEFT JOIN`."
- q: "En la consulta anterior con LEFT JOIN y GROUP BY, ¿qué función da 0 profesores para Matemáticas?"
  options: ["COUNT(*)", "COUNT(p.id_profesor)", "SUM(1)", "MAX(p.id_profesor)"]
  answer: 1
  explain: "La fila de Matemáticas tiene `p.id_profesor` a NULL. `COUNT(*)` contaría esa fila (1); `COUNT(p.id_profesor)` no cuenta los nulos (0)."
- q: "¿Qué caracteriza a una subconsulta correlacionada?"
  options: ["Devuelve siempre una sola fila", "Usa columnas de la consulta exterior", "Va siempre en el FROM", "Solo se puede usar con UNION"]
  answer: 1
  explain: "Hace referencia a columnas de la consulta exterior y, conceptualmente, se evalúa para cada fila de esta."
- q: "`WHERE id_profesor NOT IN (SELECT id_tutor FROM grupo)` devuelve 0 filas. ¿Por qué?"
  options: ["Porque todos los profesores son tutores", "Porque la subconsulta devuelve un NULL (2ASIR no tiene tutor)", "Porque NOT IN no existe en Oracle", "Porque falta un JOIN"]
  answer: 1
  explain: "Si la lista contiene un NULL, `x NOT IN (...)` nunca es verdadero. Usa NOT EXISTS o añade `WHERE id_tutor IS NOT NULL`."
- q: "¿Qué operador devuelve las filas de la primera consulta que no están en la segunda?"
  options: ["UNION", "INTERSECT", "MINUS", "UNION ALL"]
  answer: 2
  explain: "MINUS (o EXCEPT en el estándar y en Oracle 21c+) es la diferencia de conjuntos."
- q: "Hay un índice sobre `apellidos`. ¿Qué condición **impide** usarlo de forma normal?"
  options: ["`apellidos = 'Belda Iborra'`", "`apellidos LIKE 'Bel%'`", "`UPPER(apellidos) = 'BELDA IBORRA'`", "`apellidos BETWEEN 'A' AND 'C'`"]
  answer: 2
  explain: "Aplicar una función a la columna indexada impide usar el índice normal: haría falta un índice basado en la función UPPER(apellidos)."
- q: "En un plan de ejecución aparece `TABLE ACCESS FULL` sobre una tabla de 30 filas. ¿Es un problema?"
  options: ["Sí, siempre hay que evitarlo", "No necesariamente: en tablas pequeñas suele ser el acceso más barato", "Sí, indica que la tabla no tiene clave primaria", "Indica que las estadísticas están corruptas"]
  answer: 1
  explain: "El optimizador elige el plan de menor coste. Leer unos pocos bloques completos es más barato que pasar por un índice."
{{< /quiz >}}

## Referencias

- [Oracle AI Database 26ai: SQL Language Reference, *Joins*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Joins.html).
- [Oracle AI Database 26ai: SQL Language Reference, *Using Subqueries*](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Using-Subqueries.html).
- [Oracle AI Database 26ai: SQL Tuning Guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/tgsql/).
- [Curso de Bases de Datos de F. M. García: módulos 29 a 33](https://fmgarcia.github.io/CursosGithubIO/CursoBasesDatos/).
