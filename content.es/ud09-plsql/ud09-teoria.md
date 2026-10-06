---
title: "Programación con PL/SQL"
weight: 1
bookToc: true
---

# UD09 · Programación de la base de datos con PL/SQL

## Resumen del tema

SQL dice **qué** datos queremos, pero no permite expresar fácilmente **procesos**: «para cada alumno de primero, si tiene como máximo un módulo pendiente, promociónalo; si no, avisa». Para eso los SGBD incorporan un **lenguaje procedimental** que se ejecuta **dentro del servidor**. En Oracle es **PL/SQL**.

En esta unidad aprenderás a automatizar tareas con guiones y bloques PL/SQL, a usar variables y estructuras de control, a crear **funciones** y **procedimientos almacenados**, a recorrer resultados con **cursores**, a tratar errores con **excepciones**, a implementar reglas de negocio con **disparadores** (*triggers*) y a programar tareas periódicas con el **planificador**.

{{< ra "RA5:a,b,c,d,e,f,g,h,i,j" "RA4:d,h" "RA6:h" >}}

> [!IMPORTANT]
> **PL/SQL es específico de Oracle.** Otros SGBD tienen lenguajes parecidos pero **distintos**: T-SQL (SQL Server), PL/pgSQL (PostgreSQL) o el lenguaje de procedimientos de MySQL/MariaDB. Los conceptos (variables, cursores, excepciones, triggers) son comunes; la sintaxis no. El apartado 13 compara las diferencias principales.

### Objetivos de aprendizaje

Al terminar esta unidad serás capaz de:

- Identificar las formas de automatizar tareas y las herramientas para escribir y ejecutar guiones.
- Escribir bloques PL/SQL con variables, estructuras de control y funciones del sistema gestor.
- Crear procedimientos y funciones de usuario con parámetros.
- Recorrer conjuntos de filas con cursores.
- Controlar errores con excepciones predefinidas y de usuario.
- Implementar reglas de negocio y auditoría con disparadores.
- Programar tareas periódicas (eventos) con el planificador.

---

## 1. Formas de automatizar tareas

| Mecanismo | Qué es | Dónde se guarda | Cómo se ejecuta | Ejemplo en EduGest |
|---|---|---|---|---|
| **Consulta SQL** | Una única sentencia | En ningún sitio (o en una vista) | A mano | `SELECT` de las notas de un grupo |
| **Guion (script)** | Fichero con varias sentencias SQL y órdenes del cliente | Fichero `.sql` en el disco del cliente | `@guion.sql` en SQLcl | Promoción de curso (UD08) |
| **Bloque anónimo PL/SQL** | Código procedimental sin nombre | No se guarda en la BD | Se envía y se ejecuta una vez | Comprobación previa de un guion |
| **Función** | Subprograma con nombre que **devuelve un valor** | En la BD (compilado) | Dentro de expresiones y de consultas SQL | `fn_calificacion(nota)` |
| **Procedimiento** | Subprograma con nombre que **realiza una acción** | En la BD (compilado) | `EXECUTE` / `CALL` / desde otro bloque | `pr_matricular(alumno, módulo)` |
| **Paquete** | Agrupa procedimientos, funciones, tipos y variables relacionados | En la BD | `paquete.procedimiento(...)` | `pkg_secretaria` |
| **Disparador (trigger)** | Código que se ejecuta **automáticamente** ante un evento | En la BD | Lo dispara el SGBD (un `INSERT`, un `UPDATE`, un inicio de sesión...) | Auditoría de cambios de nota |
| **Tarea programada (job)** | Ejecución periódica de un programa | En la BD (`DBMS_SCHEDULER`) | Según un calendario | Recalcular estadísticas cada noche |
| **Tarea del sistema operativo** | Programa externo (cron, Programador de tareas) que lanza SQLcl | En el servidor | Según el calendario del SO | Copia de seguridad con Data Pump |

> [!TIP]
> **¿Dónde poner la lógica?** La lógica que protege la **integridad** de los datos (reglas que deben cumplirse venga de donde venga la modificación) debe estar **en la base de datos**: restricciones y, si no basta, triggers o procedimientos. La lógica de **presentación** y de interacción con el usuario va en la aplicación.

---

## 2. Herramientas y ejecución de guiones

### 2.1 Herramientas para editar (RA5.c)

| Herramienta | Ventajas para PL/SQL |
|---|---|
| **SQL Developer** | Editor de procedimientos con compilación, marcado de errores, **depurador** (puntos de ruptura, inspección de variables) y panel de salida `DBMS_OUTPUT` |
| **SQL Developer para VS Code** | Edición, compilación y ejecución integradas con Git |
| **SQLcl** | Ejecución de guiones desde la terminal o desde tareas programadas; `SHOW ERRORS` |

### 2.2 Métodos de ejecución (RA5.b)

```sql
-- En SQLcl o SQL*Plus
SET SERVEROUTPUT ON           -- muestra lo que escribe DBMS_OUTPUT.PUT_LINE
@crear_procedimientos.sql     -- ejecuta un guion
EXECUTE pr_informe_grupo('1DAM')   -- ejecuta un procedimiento (abreviado EXEC)
SHOW ERRORS PROCEDURE pr_matricular -- muestra los errores de compilación
```

```bash
# Desde el sistema operativo (por ejemplo, en una tarea cron)
sql -S edugest/Edugest_2026@//localhost:1521/FREEPDB1 @informe_diario.sql
```

> [!WARNING]
> Un bloque PL/SQL o un `CREATE PROCEDURE` en un guion debe terminar con una **barra `/` sola en una línea**. Sin ella, el cliente no envía el bloque y parece que «no pasa nada».

Si un subprograma tiene errores de compilación, Oracle lo crea igualmente en estado **INVALID** y muestra `Warning: Procedure created with compilation errors`. Consulta los errores con `SHOW ERRORS` o en la vista `USER_ERRORS`.

---

## 3. Bloques PL/SQL

### 3.1 Estructura

```sql
[DECLARE
    -- declaraciones: variables, constantes, cursores, excepciones]
BEGIN
    -- sentencias ejecutables (obligatorio)
[EXCEPTION
    -- tratamiento de errores]
END;
/
```

### 3.2 Primer bloque

```sql
SET SERVEROUTPUT ON

DECLARE
    v_total   NUMBER;
    v_ciclo   CONSTANT VARCHAR2(5) := 'DAM';
BEGIN
    SELECT COUNT(*) INTO v_total
    FROM   modulo
    WHERE  cod_ciclo = v_ciclo;

    DBMS_OUTPUT.PUT_LINE('El ciclo ' || v_ciclo || ' tiene ' || v_total || ' módulos.');
END;
/
```

```text
El ciclo DAM tiene 10 módulos.
```

| Elemento | Significado |
|---|---|
| `v_total NUMBER;` | Declaración de una variable. Sin valor inicial vale `NULL` |
| `CONSTANT ... := 'DAM'` | Constante: debe inicializarse y no puede cambiar |
| `SELECT ... INTO v_total` | Guarda el resultado de la consulta en la variable. Debe devolver **exactamente una fila** |
| `DBMS_OUTPUT.PUT_LINE` | Procedimiento del paquete `DBMS_OUTPUT` que escribe una línea en el búfer de salida |

---

## 4. Variables y tipos

### 4.1 Declaración

```sql
DECLARE
    v_nombre      VARCHAR2(40);
    v_nota        NUMBER(4,2) := 0;
    v_hoy         DATE := SYSDATE;
    v_aprobado    BOOLEAN := FALSE;
    v_email       alumno.email%TYPE;           -- mismo tipo que la columna
    r_alumno      alumno%ROWTYPE;              -- un registro con todas las columnas
BEGIN
    SELECT * INTO r_alumno FROM alumno WHERE id_alumno = 1;
    DBMS_OUTPUT.PUT_LINE(r_alumno.nombre || ' vive en ' || r_alumno.localidad);
END;
/
```

> [!TIP]
> Usa `%TYPE` y `%ROWTYPE` siempre que una variable vaya a guardar datos de una tabla. Si mañana el `email` pasa de 100 a 150 caracteres, tu código seguirá funcionando sin cambios.

### 4.2 Variables del sistema y de usuario

| Tipo | Ejemplos | Ámbito |
|---|---|---|
| **Funciones y variables del sistema** | `SYSDATE`, `SYSTIMESTAMP`, `USER`, `SYS_CONTEXT('USERENV', 'SESSION_USER')`, `SYS_CONTEXT('USERENV', 'IP_ADDRESS')`, `SQL%ROWCOUNT` | Las proporciona el SGBD |
| **Variables de sustitución** (del cliente SQLcl/SQL\*Plus) | `DEFINE grupo = '1DAM'` y `&grupo` en una consulta | El cliente sustituye el texto **antes** de enviar la sentencia |
| **Variables de enlace** (*bind*) | `VARIABLE v_total NUMBER` y `:v_total` | Viven en la sesión del cliente; se usan en SQL y PL/SQL |
| **Variables PL/SQL** | Las declaradas en `DECLARE` | Solo dentro del bloque |

```sql
-- Variable de sustitución: SQLcl pregunta el valor si no está definida
SELECT nombre, apellidos FROM alumno WHERE cod_grupo = '&grupo';

-- Variable de enlace
VARIABLE v_media NUMBER
BEGIN
    SELECT AVG(nota_final) INTO :v_media FROM matricula;
END;
/
PRINT v_media
```

> [!NOTE]
> En MySQL las **variables de usuario** se escriben `@variable` y las del sistema `@@variable`. En Oracle no existe esa sintaxis: el equivalente son las variables de sustitución y de enlace del cliente y las variables de sesión que se leen con `SYS_CONTEXT`.

---

## 5. Estructuras de control

### 5.1 Condicionales

```sql
DECLARE
    v_nota  matricula.nota_final%TYPE;
    v_texto VARCHAR2(20);
BEGIN
    SELECT nota_final INTO v_nota FROM matricula WHERE id_matricula = 10002;

    IF v_nota IS NULL THEN
        v_texto := 'Sin calificar';
    ELSIF v_nota < 5 THEN
        v_texto := 'Suspenso';
    ELSIF v_nota < 9 THEN
        v_texto := 'Aprobado';
    ELSE
        v_texto := 'Sobresaliente';
    END IF;

    DBMS_OUTPUT.PUT_LINE('Nota ' || v_nota || ': ' || v_texto);
END;
/
```

```text
Nota 4.75: Suspenso
```

También existe `CASE` como sentencia (y como expresión, igual que en SQL):

```sql
v_texto := CASE WHEN v_nota >= 5 THEN 'Apto' ELSE 'No apto' END;
```

### 5.2 Bucles

{{< tabs >}}
{{% tab "LOOP ... EXIT WHEN" %}}
```sql
DECLARE
    i PLS_INTEGER := 1;
BEGIN
    LOOP
        DBMS_OUTPUT.PUT_LINE('Iteración ' || i);
        i := i + 1;
        EXIT WHEN i > 3;
    END LOOP;
END;
/
```
Se ejecuta al menos una vez. La condición de salida puede ir en cualquier punto.
{{% /tab %}}
{{% tab "WHILE" %}}
```sql
DECLARE
    v_saldo NUMBER := 1000;
    v_anios PLS_INTEGER := 0;
BEGIN
    WHILE v_saldo < 2000 LOOP          -- ¿cuántos años al 5 % para duplicar?
        v_saldo := v_saldo * 1.05;
        v_anios := v_anios + 1;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE(v_anios || ' años');   -- 15 años
END;
/
```
Comprueba la condición **antes** de cada iteración.
{{% /tab %}}
{{% tab "FOR numérico" %}}
```sql
BEGIN
    FOR curso IN 1 .. 2 LOOP
        DBMS_OUTPUT.PUT_LINE('Curso ' || curso);
    END LOOP;

    FOR i IN REVERSE 1 .. 3 LOOP       -- 3, 2, 1
        DBMS_OUTPUT.PUT_LINE(i);
    END LOOP;
END;
/
```
La variable del bucle se declara sola y no se puede modificar dentro.
{{% /tab %}}
{{< /tabs >}}

`CONTINUE` salta a la siguiente iteración y `CONTINUE WHEN condición` lo hace solo si se cumple la condición.

---

## 6. Funciones del sistema gestor en PL/SQL

Dentro de PL/SQL se pueden usar casi todas las funciones de fila de SQL (UD06): `UPPER`, `SUBSTR`, `ROUND`, `TO_CHAR`, `ADD_MONTHS`, `NVL`... Además, Oracle proporciona **paquetes** con funcionalidad adicional (RA5.e):

| Paquete | Para qué |
|---|---|
| `DBMS_OUTPUT` | Mostrar mensajes de depuración |
| `DBMS_RANDOM` | Generar números y cadenas aleatorias (datos de prueba) |
| `DBMS_SCHEDULER` | Programar tareas (apartado 12) |
| `DBMS_STATS` | Recopilar estadísticas para el optimizador |
| `DBMS_LOCK.SLEEP` / `DBMS_SESSION.SLEEP` | Esperar unos segundos (pruebas de concurrencia) |
| `UTL_FILE` | Leer y escribir ficheros en el servidor |
| `DBMS_CRYPTO` | Funciones criptográficas (hash, cifrado) |

---

## 7. Procedimientos almacenados

### 7.1 Sintaxis

```sql
CREATE [OR REPLACE] PROCEDURE nombre
    (parametro1 [IN | OUT | IN OUT] tipo [DEFAULT valor], ...)
IS
    -- declaraciones locales
BEGIN
    -- código
[EXCEPTION
    -- tratamiento de errores]
END [nombre];
/
```

| Modo | Significado |
|---|---|
| `IN` (por defecto) | El valor entra en el procedimiento y no se puede modificar dentro |
| `OUT` | El procedimiento devuelve un valor en el parámetro |
| `IN OUT` | Entra un valor y el procedimiento puede devolver otro |

> [!NOTE]
> En la declaración de parámetros **no** se indica el tamaño: `p_cod_grupo VARCHAR2`, no `VARCHAR2(10)`. O mejor, `p_cod_grupo grupo.cod_grupo%TYPE`.

### 7.2 Ejemplo: informe de un grupo

```sql
CREATE OR REPLACE PROCEDURE pr_resumen_grupo (
    p_cod_grupo  IN  grupo.cod_grupo%TYPE,
    p_alumnos    OUT NUMBER,
    p_media      OUT NUMBER
) IS
BEGIN
    SELECT COUNT(DISTINCT a.id_alumno), ROUND(AVG(m.nota_final), 2)
    INTO   p_alumnos, p_media
    FROM   alumno a
           LEFT JOIN matricula m ON m.id_alumno = a.id_alumno
    WHERE  a.cod_grupo = p_cod_grupo;
END pr_resumen_grupo;
/

-- Llamada desde un bloque anónimo
DECLARE
    v_n NUMBER;
    v_m NUMBER;
BEGIN
    pr_resumen_grupo('1DAM', v_n, v_m);
    DBMS_OUTPUT.PUT_LINE('1DAM: ' || v_n || ' alumnos, media ' || v_m);
END;
/
```

```text
1DAM: 7 alumnos, media 6.4
```

Formas de llamar a un procedimiento:

```sql
EXEC pr_saludar;                                  -- SQLcl / SQL*Plus
CALL pr_saludar();                                -- SQL estándar
BEGIN pr_saludar; END;                            -- desde PL/SQL
BEGIN pr_resumen_grupo(p_cod_grupo => '1DAW',     -- notación nominal
                       p_alumnos   => :n,
                       p_media     => :m); END;
```

---

## 8. Funciones de usuario

Una función **devuelve un valor** con `RETURN` y puede usarse **dentro de una consulta SQL** (si no modifica datos).

```sql
CREATE OR REPLACE FUNCTION fn_calificacion (p_nota IN NUMBER)
RETURN VARCHAR2
DETERMINISTIC          -- mismo resultado para la misma entrada: Oracle puede optimizarla
IS
BEGIN
    RETURN CASE
               WHEN p_nota IS NULL THEN 'NC'
               WHEN p_nota < 5     THEN 'Insuficiente'
               WHEN p_nota < 6     THEN 'Suficiente'
               WHEN p_nota < 7     THEN 'Bien'
               WHEN p_nota < 9     THEN 'Notable'
               ELSE                     'Sobresaliente'
           END;
END fn_calificacion;
/

CREATE OR REPLACE FUNCTION fn_edad (
    p_fecha_nac IN DATE,
    p_fecha_ref IN DATE DEFAULT SYSDATE
) RETURN NUMBER
IS
BEGIN
    RETURN TRUNC(MONTHS_BETWEEN(p_fecha_ref, p_fecha_nac) / 12);
END fn_edad;
/

-- Uso en SQL
SELECT nombre, fn_edad(fecha_nacimiento, DATE '2026-10-06') AS edad
FROM   alumno WHERE cod_grupo = '2DAW' ORDER BY edad DESC;

SELECT id_matricula, nota_final, fn_calificacion(nota_final) AS calificacion
FROM   matricula WHERE id_alumno = 1;
```

| ID_MATRICULA | NOTA_FINAL | CALIFICACION |
|---|---|---|
| 10001 | 8.75 | Notable |
| 10002 | 4.75 | Insuficiente |
| 10003 | 7.25 | Notable |
| 10004 | 4.75 | Insuficiente |
| 10005 | 6.75 | Bien |

| | Procedimiento | Función |
|---|---|---|
| Devuelve | Nada (o valores por parámetros `OUT`) | Un valor con `RETURN` |
| Se usa en | Sentencias PL/SQL, `EXEC`, `CALL` | Expresiones PL/SQL y **consultas SQL** |
| Uso típico | Realizar una acción (matricular, promocionar) | Calcular un valor (edad, calificación) |

---

## 9. Cursores

Un **cursor** es un área de trabajo que permite recorrer, **fila a fila**, el resultado de una consulta que devuelve varias filas.

### 9.1 Cursores implícitos

Oracle crea uno automáticamente para cada `SELECT INTO`, `INSERT`, `UPDATE`, `DELETE` y `MERGE`. Sus atributos se consultan con el prefijo `SQL`:

| Atributo | Significado |
|---|---|
| `SQL%ROWCOUNT` | Número de filas afectadas por la última sentencia |
| `SQL%FOUND` / `SQL%NOTFOUND` | Si afectó a alguna fila o a ninguna |

```sql
BEGIN
    UPDATE alumno SET localidad = 'Alicante' WHERE localidad = 'Alacant';
    DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' filas corregidas');
END;
/
```

### 9.2 Cursores explícitos

{{< tabs >}}
{{% tab "FOR de cursor (recomendado)" %}}
```sql
DECLARE
    CURSOR c_alumnos (p_grupo VARCHAR2) IS
        SELECT a.id_alumno, a.nombre, a.apellidos
        FROM   alumno a
        WHERE  a.cod_grupo = p_grupo
        ORDER  BY a.apellidos, a.nombre;
BEGIN
    FOR r IN c_alumnos('2DAW') LOOP
        DBMS_OUTPUT.PUT_LINE(r.apellidos || ', ' || r.nombre);
    END LOOP;
END;
/
```
El bucle `FOR` abre el cursor, declara el registro `r`, lee cada fila y cierra el cursor automáticamente, incluso si hay un error.
{{% /tab %}}
{{% tab "OPEN / FETCH / CLOSE" %}}
```sql
DECLARE
    CURSOR c_alumnos IS
        SELECT nombre, apellidos FROM alumno WHERE cod_grupo = '2DAW' ORDER BY apellidos;
    v_nombre    alumno.nombre%TYPE;
    v_apellidos alumno.apellidos%TYPE;
BEGIN
    OPEN c_alumnos;
    LOOP
        FETCH c_alumnos INTO v_nombre, v_apellidos;
        EXIT WHEN c_alumnos%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(c_alumnos%ROWCOUNT || '. ' || v_apellidos || ', ' || v_nombre);
    END LOOP;
    CLOSE c_alumnos;
END;
/
```
Control manual: útil cuando hay que procesar las filas de forma no uniforme. Atributos: `%ISOPEN`, `%FOUND`, `%NOTFOUND`, `%ROWCOUNT`.
{{% /tab %}}
{{< /tabs >}}

```text
Amorós Guillem, Sara
Carbonell Soriano, Elena
Planelles Marco, Sofía
Sala Brotons, Mateo
Verdú Castelló, Nicolás
```

### 9.3 Cursores para modificar: FOR UPDATE y WHERE CURRENT OF

```sql
DECLARE
    CURSOR c_rescate IS
        SELECT nota_final FROM matricula
        WHERE  nota_final >= 4.75 AND nota_final < 5
        FOR UPDATE OF nota_final;                  -- bloquea las filas al abrir
BEGIN
    FOR r IN c_rescate LOOP
        UPDATE matricula SET nota_final = 5
        WHERE  CURRENT OF c_rescate;              -- la fila actual del cursor
    END LOOP;
END;
/
```

> [!TIP]
> **Primero piensa en SQL.** Si una tarea se puede hacer con **una** sentencia SQL (`UPDATE ... WHERE ...`), es más rápida y sencilla que un cursor que recorre las filas una a una. Los cursores son para cuando cada fila requiere una **lógica distinta**: mensajes, decisiones, llamadas a otros procedimientos.

---

## 10. Excepciones

Una **excepción** es un error que se produce durante la ejecución. Cuando ocurre, el control salta a la sección `EXCEPTION` del bloque. Si no hay un manejador para ella, se **propaga** al bloque que lo llamó y, si nadie la trata, la ejecución termina con el error.

### 10.1 Excepciones predefinidas

| Excepción | Error | Cuándo |
|---|---|---|
| `NO_DATA_FOUND` | ORA-01403 | `SELECT INTO` que no devuelve filas |
| `TOO_MANY_ROWS` | ORA-01422 | `SELECT INTO` que devuelve varias filas |
| `DUP_VAL_ON_INDEX` | ORA-00001 | Valor duplicado en una clave primaria o única |
| `ZERO_DIVIDE` | ORA-01476 | División por cero |
| `VALUE_ERROR` | ORA-06502 | Error de conversión o de tamaño |
| `INVALID_NUMBER` | ORA-01722 | Conversión de texto a número no válida en SQL |

```sql
DECLARE
    v_nombre alumno.nombre%TYPE;
BEGIN
    SELECT nombre INTO v_nombre FROM alumno WHERE nia = '99999999';
    DBMS_OUTPUT.PUT_LINE(v_nombre);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No existe ningún alumno con ese NIA');
    WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE('Hay más de un alumno con ese NIA: revisa los datos');
END;
/
```

### 10.2 Excepciones de usuario y RAISE_APPLICATION_ERROR

```sql
DECLARE
    e_nota_invalida EXCEPTION;                       -- excepción propia
    v_nota NUMBER := 12;
BEGIN
    IF v_nota NOT BETWEEN 0 AND 10 THEN
        RAISE e_nota_invalida;
    END IF;
EXCEPTION
    WHEN e_nota_invalida THEN
        DBMS_OUTPUT.PUT_LINE('La nota debe estar entre 0 y 10');
END;
/
```

Para devolver un error **con código y mensaje propios** a quien llamó (la aplicación, otro procedimiento, un `INSERT` que disparó un trigger) se usa `RAISE_APPLICATION_ERROR` con un código entre **-20000 y -20999**:

```sql
RAISE_APPLICATION_ERROR(-20010, 'El alumno no pertenece a un grupo del ciclo del módulo');
```

### 10.3 Asociar un nombre a un error de Oracle

```sql
DECLARE
    e_hijos EXCEPTION;
    PRAGMA EXCEPTION_INIT(e_hijos, -2292);     -- ORA-02292: child record found
BEGIN
    DELETE FROM grupo WHERE cod_grupo = '1DAM';
EXCEPTION
    WHEN e_hijos THEN
        DBMS_OUTPUT.PUT_LINE('No se puede borrar: el grupo tiene alumnado');
END;
/
```

### 10.4 WHEN OTHERS, SQLCODE y SQLERRM

```sql
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error ' || SQLCODE || ': ' || SQLERRM);
        ROLLBACK;
        RAISE;          -- vuelve a lanzar el error: no lo ocultes
```

> [!CAUTION]
> Un `WHEN OTHERS THEN NULL;` **oculta todos los errores**: el programa parece funcionar, pero los datos quedan mal y nadie se entera. Si usas `WHEN OTHERS`, registra el error y vuelve a lanzarlo con `RAISE`.

### 10.5 Ejemplo completo: procedimiento de matrícula

```sql
CREATE OR REPLACE PROCEDURE pr_matricular (
    p_id_alumno  IN alumno.id_alumno%TYPE,
    p_id_modulo  IN modulo.id_modulo%TYPE,
    p_curso      IN matricula.curso_academico%TYPE
) IS
    v_ciclo_grupo   ciclo.cod_ciclo%TYPE;
    v_ciclo_modulo  ciclo.cod_ciclo%TYPE;
    v_conv          matricula.convocatoria%TYPE;
BEGIN
    -- 1. Ciclo del grupo del alumno (NO_DATA_FOUND si el alumno no existe)
    SELECT g.cod_ciclo INTO v_ciclo_grupo
    FROM   alumno a JOIN grupo g ON g.cod_grupo = a.cod_grupo
    WHERE  a.id_alumno = p_id_alumno;

    -- 2. Ciclo del módulo
    SELECT cod_ciclo INTO v_ciclo_modulo FROM modulo WHERE id_modulo = p_id_modulo;

    -- 3. Regla de negocio R2 (no representable en el modelo lógico)
    IF v_ciclo_grupo <> v_ciclo_modulo THEN
        RAISE_APPLICATION_ERROR(-20010,
            'El módulo es de ' || v_ciclo_modulo || ' y el alumno está en ' || v_ciclo_grupo);
    END IF;

    -- 4. Convocatoria: la siguiente a la última en la que se matriculó
    SELECT NVL(MAX(convocatoria), 0) + 1 INTO v_conv
    FROM   matricula
    WHERE  id_alumno = p_id_alumno AND id_modulo = p_id_modulo;

    IF v_conv > 4 THEN
        RAISE_APPLICATION_ERROR(-20011, 'Ha agotado las cuatro convocatorias del módulo');
    END IF;

    INSERT INTO matricula (id_alumno, id_modulo, curso_academico, convocatoria)
    VALUES (p_id_alumno, p_id_modulo, p_curso, v_conv);

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20012, 'Alumno sin grupo, o alumno o módulo inexistente');
    WHEN DUP_VAL_ON_INDEX THEN
        RAISE_APPLICATION_ERROR(-20013, 'El alumno ya está matriculado de ese módulo en ' || p_curso);
END pr_matricular;
/

EXEC pr_matricular(1, 2, '2026-27');    -- correcto: convocatoria 2 (4,75 en 2025-26)
EXEC pr_matricular(1, 12, '2026-27');   -- ORA-20010: el módulo es de DAW y el alumno está en DAM
EXEC pr_matricular(30, 2, '2026-27');   -- ORA-20012: alumno sin grupo
```

> [!NOTE]
> El procedimiento **no** hace `COMMIT`. Es una buena práctica: quien lo llama (la aplicación o un guion) decide cuándo termina la transacción, por ejemplo después de matricular al alumno en **todos** sus módulos.

---

## 11. Disparadores (triggers)

Un **disparador** es un bloque PL/SQL asociado a una tabla (o a un evento) que el SGBD ejecuta **automáticamente** cuando se produce el evento.

### 11.1 Tipos de disparadores DML

| Característica | Opciones |
|---|---|
| **Evento** | `INSERT`, `UPDATE` (opcionalmente `OF columna`), `DELETE`, o varios con `OR` |
| **Momento** | `BEFORE` (antes de la modificación: permite validar o cambiar valores) o `AFTER` (después: auditoría, acciones derivadas) |
| **Nivel** | De **sentencia** (una vez por sentencia) o de **fila** (`FOR EACH ROW`: una vez por cada fila afectada) |
| **Condición** | `WHEN (condición)` en disparadores de fila |

En los disparadores de fila, `:OLD` y `:NEW` dan acceso a los valores **anteriores** y **nuevos** de la fila:

| Evento | `:OLD` | `:NEW` |
|---|---|---|
| `INSERT` | `NULL` | Valores insertados |
| `UPDATE` | Valores anteriores | Valores nuevos (modificables en `BEFORE`) |
| `DELETE` | Valores borrados | `NULL` |

### 11.2 Auditoría de cambios de nota

```sql
CREATE TABLE auditoria_nota (
    id_auditoria  NUMBER GENERATED ALWAYS AS IDENTITY CONSTRAINT pk_auditoria_nota PRIMARY KEY,
    id_matricula  NUMBER(8)    NOT NULL,
    nota_anterior NUMBER(4,2),
    nota_nueva    NUMBER(4,2),
    usuario       VARCHAR2(128) DEFAULT USER NOT NULL,
    momento       TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL
);

CREATE OR REPLACE TRIGGER trg_auditoria_nota
AFTER UPDATE OF nota_final ON matricula
FOR EACH ROW
WHEN (NVL(OLD.nota_final, -1) <> NVL(NEW.nota_final, -1))   -- solo si cambia de verdad
BEGIN
    INSERT INTO auditoria_nota (id_matricula, nota_anterior, nota_nueva)
    VALUES (:OLD.id_matricula, :OLD.nota_final, :NEW.nota_final);
END;
/

UPDATE matricula SET nota_final = 5 WHERE id_matricula IN (10002, 10004);
SELECT id_matricula, nota_anterior, nota_nueva, usuario FROM auditoria_nota;
```

| ID_MATRICULA | NOTA_ANTERIOR | NOTA_NUEVA | USUARIO |
|---|---|---|---|
| 10002 | 4.75 | 5 | EDUGEST |
| 10004 | 4.75 | 5 | EDUGEST |

> [!NOTE]
> En la cláusula `WHEN` se escribe `OLD` y `NEW` **sin** los dos puntos; en el cuerpo, con ellos (`:OLD`, `:NEW`).

### 11.3 Implementar una regla de negocio (RA6.h)

La restricción R1 de EduGest, «el jefe de un departamento debe pertenecer a él», no se podía declarar con una clave ajena:

```sql
CREATE OR REPLACE TRIGGER trg_jefe_departamento
BEFORE INSERT OR UPDATE OF id_jefe ON departamento
FOR EACH ROW
WHEN (NEW.id_jefe IS NOT NULL)
DECLARE
    v_dpto profesor.id_departamento%TYPE;
BEGIN
    SELECT id_departamento INTO v_dpto FROM profesor WHERE id_profesor = :NEW.id_jefe;
    IF v_dpto <> :NEW.id_departamento THEN
        RAISE_APPLICATION_ERROR(-20020,
            'El profesor ' || :NEW.id_jefe || ' no pertenece al departamento ' || :NEW.id_departamento);
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        NULL;   -- el profesor no existe: lo rechazará la clave ajena fk_departamento_jefe
END;
/

UPDATE departamento SET id_jefe = 111 WHERE id_departamento = 1;
-- ORA-20020: El profesor 111 no pertenece al departamento 1
```

> [!WARNING]
> Esta regla tiene **dos** lados: también se incumple si se **cambia de departamento** a un profesor que es jefe. Una implementación completa necesita un segundo trigger sobre `PROFESOR` (práctica 9.5).

### 11.4 Valores automáticos con BEFORE

Un disparador `BEFORE` de fila puede **modificar** `:NEW` antes de que se guarde:

```sql
CREATE OR REPLACE TRIGGER trg_alumno_normaliza
BEFORE INSERT OR UPDATE ON alumno
FOR EACH ROW
BEGIN
    :NEW.email     := LOWER(TRIM(:NEW.email));
    :NEW.nombre    := INITCAP(TRIM(:NEW.nombre));
    :NEW.apellidos := INITCAP(TRIM(:NEW.apellidos));
END;
/
```

### 11.5 La tabla mutante

Un disparador **de fila** no puede **consultar ni modificar la tabla que lo ha disparado**: Oracle lanza `ORA-04091: table ... is mutating, trigger/function may not see it`, porque la tabla está a medio modificar. Por ejemplo, para comprobar que un profesor no supera 20 horas en `IMPARTE` hay que **sumar** las filas de `IMPARTE`.

La solución es un **disparador compuesto**, que tiene secciones para cada momento y comprueba la regla **después de la sentencia**, cuando la tabla ya es estable:

```sql
CREATE OR REPLACE TRIGGER trg_imparte_max_horas
FOR INSERT OR UPDATE ON imparte
COMPOUND TRIGGER

    TYPE t_ids IS TABLE OF imparte.id_profesor%TYPE;
    g_profesores t_ids := t_ids();
    v_horas      NUMBER;

    AFTER EACH ROW IS
    BEGIN
        g_profesores.EXTEND;
        g_profesores(g_profesores.LAST) := :NEW.id_profesor;   -- solo apunta quién ha cambiado
    END AFTER EACH ROW;

    AFTER STATEMENT IS
    BEGIN
        FOR i IN 1 .. g_profesores.COUNT LOOP
            SELECT SUM(horas_semanales) INTO v_horas
            FROM   imparte
            WHERE  id_profesor = g_profesores(i)
            AND    curso_academico = '2025-26';
            IF v_horas > 20 THEN
                RAISE_APPLICATION_ERROR(-20030,
                    'El profesor ' || g_profesores(i) || ' tendría ' || v_horas || ' horas semanales');
            END IF;
        END LOOP;
    END AFTER STATEMENT;

END trg_imparte_max_horas;
/
```

> [!NOTE]
> Para simplificar, el ejemplo comprueba solo el curso 2025-26. En la práctica 9.6 lo generalizarás guardando también el curso académico de cada fila modificada.

### 11.6 Otros disparadores

| Tipo | Se dispara | Ejemplo |
|---|---|---|
| `INSTEAD OF` | En lugar de un DML sobre una **vista** | Permitir `INSERT` en una vista con `JOIN` repartiendo los datos entre las tablas |
| **De sistema / DDL** | `AFTER LOGON`, `BEFORE DROP`, `AFTER CREATE`... | Registrar los inicios de sesión o impedir borrar tablas en horario lectivo |

### 11.7 Gestión de disparadores

```sql
ALTER TRIGGER trg_alumno_normaliza DISABLE;
ALTER TRIGGER trg_alumno_normaliza ENABLE;
ALTER TABLE alumno DISABLE ALL TRIGGERS;
DROP TRIGGER trg_alumno_normaliza;
SELECT trigger_name, triggering_event, status FROM user_triggers;
```

> [!WARNING]
> **Usa los disparadores con moderación.** Son invisibles para quien ejecuta un `UPDATE`: hacen cosas «por detrás», pueden encadenarse y ralentizan las modificaciones masivas. Úsalos para reglas de integridad que no pueden expresarse con restricciones y para auditoría; no para la lógica general de la aplicación.

---

## 12. Eventos: tareas programadas

Oracle programa tareas periódicas con el paquete **`DBMS_SCHEDULER`** (en MySQL, el equivalente es `CREATE EVENT`). El usuario necesita el privilegio `CREATE JOB` (incluido en el script 00 de EduGest).

```sql
-- Tabla de resumen que consultará el cuadro de mando
CREATE TABLE resumen_grupo (
    cod_grupo   VARCHAR2(10),
    matriculas  NUMBER,
    aprobadas   NUMBER,
    media       NUMBER(4,2),
    calculado   DATE
);

-- Procedimiento que se ejecutará cada noche
CREATE OR REPLACE PROCEDURE pr_recalcular_resumen IS
BEGIN
    DELETE FROM resumen_grupo;
    INSERT INTO resumen_grupo (cod_grupo, matriculas, aprobadas, media, calculado)
    SELECT a.cod_grupo, COUNT(*), SUM(CASE WHEN m.nota_final >= 5 THEN 1 ELSE 0 END),
           ROUND(AVG(m.nota_final), 2), SYSDATE
    FROM   matricula m JOIN alumno a ON a.id_alumno = m.id_alumno
    GROUP  BY a.cod_grupo;
    COMMIT;
END;
/

BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_RESUMEN_NOCTURNO',
        job_type        => 'STORED_PROCEDURE',
        job_action      => 'PR_RECALCULAR_RESUMEN',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0',
        enabled         => TRUE,
        comments        => 'Recalcula el resumen de notas por grupo cada noche a las 2:00');
END;
/

-- Ejecutarla ahora para probarla y ver su historial
EXEC DBMS_SCHEDULER.RUN_JOB('JOB_RESUMEN_NOCTURNO');
SELECT job_name, enabled, state, next_run_date FROM user_scheduler_jobs;
SELECT log_date, status, error# FROM user_scheduler_job_run_details
WHERE  job_name = 'JOB_RESUMEN_NOCTURNO' ORDER BY log_date DESC;

-- Detenerla o eliminarla
EXEC DBMS_SCHEDULER.DISABLE('JOB_RESUMEN_NOCTURNO');
EXEC DBMS_SCHEDULER.DROP_JOB('JOB_RESUMEN_NOCTURNO');
```

> [!TIP]
> La sintaxis de `repeat_interval` permite calendarios muy precisos: `FREQ=WEEKLY; BYDAY=MON,WED,FRI; BYHOUR=8`, `FREQ=MINUTELY; INTERVAL=15`, `FREQ=MONTHLY; BYMONTHDAY=-1` (último día del mes).

---

## 13. PL/SQL frente a otros lenguajes de SGBD

| Concepto | Oracle PL/SQL | MySQL / MariaDB | PostgreSQL (PL/pgSQL) |
|---|---|---|---|
| Bloque anónimo | `BEGIN ... END; /` | No existe (solo dentro de procedimientos) | `DO $$ BEGIN ... END $$;` |
| Delimitador en scripts | `/` | `DELIMITER //` | `$$` |
| Variable | `v NUMBER;` en `DECLARE` | `DECLARE v INT;` o `@v` | `DECLARE v integer;` |
| Asignación | `v := 1;` | `SET v = 1;` | `v := 1;` |
| Mensajes | `DBMS_OUTPUT.PUT_LINE` | `SELECT 'texto';` | `RAISE NOTICE '...'` |
| Error propio | `RAISE_APPLICATION_ERROR(-20001, '...')` | `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'` | `RAISE EXCEPTION '...'` |
| Trigger de fila | `FOR EACH ROW` con `:NEW`/`:OLD` | `FOR EACH ROW` con `NEW`/`OLD` | Función `RETURNS trigger` + `CREATE TRIGGER ... EXECUTE FUNCTION` |
| Tareas programadas | `DBMS_SCHEDULER` | `CREATE EVENT` | Extensión `pg_cron` |

---

## 14. Errores frecuentes

| Error | Mensaje | Causa |
|---|---|---|
| No se ve la salida | — | Falta `SET SERVEROUTPUT ON` |
| El bloque no se ejecuta en un script | — | Falta la `/` final |
| `PLS-00201: identifier must be declared` | | Variable o tabla mal escrita, o falta de privilegios **directos** (no por rol) sobre una tabla de otro esquema |
| `ORA-01403: no data found` | | `SELECT INTO` sin filas: trátalo con `NO_DATA_FOUND` |
| `ORA-01422: exact fetch returns more than requested number of rows` | | `SELECT INTO` con varias filas: usa un cursor |
| `ORA-04091: table is mutating` | | Un trigger de fila consulta su propia tabla: usa un trigger compuesto |
| `ORA-06502: numeric or value error` | | Valor demasiado grande para la variable |
| Objeto `INVALID` | | Errores de compilación o cambió una tabla de la que depende: `ALTER PROCEDURE ... COMPILE;` |

## 15. Buenas prácticas

- Prefijos claros: `v_` variables, `p_` parámetros, `c_` cursores, `e_` excepciones, `pr_`/`fn_`/`trg_`/`pkg_` objetos.
- `%TYPE` y `%ROWTYPE` para enlazar los tipos con las tablas.
- Los subprogramas no hacen `COMMIT`: lo hace quien controla la transacción.
- Trata las excepciones que esperas y deja que las demás se propaguen.
- Una sentencia SQL es mejor que un bucle cuando ambas resuelven el problema.
- Agrupa los subprogramas relacionados en **paquetes** cuando el proyecto crezca.

---

## 16. Resumen

- Las tareas pueden automatizarse con guiones, bloques PL/SQL, funciones, procedimientos, paquetes, disparadores y tareas programadas.
- Un bloque PL/SQL tiene secciones `DECLARE`, `BEGIN` y `EXCEPTION`. Las variables se tipan con `%TYPE`/`%ROWTYPE`.
- `IF`, `CASE`, `LOOP`, `WHILE` y `FOR` controlan el flujo.
- Los **procedimientos** realizan acciones; las **funciones** devuelven un valor y se pueden usar en SQL.
- Los **cursores** recorren resultados de varias filas; el bucle `FOR` de cursor es la forma más segura.
- Las **excepciones** tratan errores; `RAISE_APPLICATION_ERROR` devuelve errores propios.
- Los **disparadores** ejecutan código ante eventos y permiten implementar auditoría y reglas no representables en el modelo lógico.
- `DBMS_SCHEDULER` programa tareas periódicas.

---

## 17. Autoevaluación

{{< quiz >}}
- q: "¿Qué diferencia principal hay entre un procedimiento y una función?"
  options: ["El procedimiento se guarda en la base de datos y la función no", "La función devuelve un valor con RETURN y puede usarse en una consulta SQL", "La función no admite parámetros", "El procedimiento solo puede tener parámetros OUT"]
  answer: 1
  explain: "Una función devuelve un valor y, si no modifica datos, se puede llamar desde SELECT. Un procedimiento realiza una acción y devuelve valores, si acaso, mediante parámetros OUT."
- q: "Un `SELECT ... INTO` no encuentra ninguna fila. ¿Qué ocurre?"
  options: ["La variable queda a NULL sin error", "Se lanza NO_DATA_FOUND", "Se lanza TOO_MANY_ROWS", "Se lanza ZERO_DIVIDE"]
  answer: 1
  explain: "SELECT INTO debe devolver exactamente una fila: con ninguna lanza NO_DATA_FOUND (ORA-01403) y con varias TOO_MANY_ROWS (ORA-01422)."
- q: "¿Para qué sirve `alumno.email%TYPE`?"
  options: ["Para obtener el email de un alumno", "Para declarar una variable con el mismo tipo que la columna email", "Para convertir un texto en email", "Para crear un índice"]
  answer: 1
  explain: "%TYPE enlaza el tipo de la variable con el de la columna: si la columna cambia, la variable se adapta."
- q: "¿Qué rango de códigos admite RAISE_APPLICATION_ERROR?"
  options: ["0 a 999", "-1 a -19999", "-20000 a -20999", "Cualquier número"]
  answer: 2
  explain: "Los códigos de error de usuario van de -20000 a -20999, para no confundirse con los errores de Oracle."
- q: "En un trigger BEFORE UPDATE FOR EACH ROW, ¿qué contiene `:OLD.nota_final`?"
  options: ["La nota nueva", "La nota antes del UPDATE", "NULL siempre", "La media de las notas"]
  answer: 1
  explain: "`:OLD` contiene los valores anteriores a la modificación y `:NEW` los nuevos, que en BEFORE todavía se pueden cambiar."
- q: "Un trigger de fila sobre IMPARTE hace un SELECT SUM(...) FROM imparte. ¿Qué error aparece al actualizar IMPARTE?"
  options: ["ORA-00001", "ORA-01403", "ORA-04091 tabla mutante", "Ninguno"]
  answer: 2
  explain: "Un trigger de fila no puede consultar la tabla que lo dispara. La solución es un trigger compuesto que compruebe la regla en AFTER STATEMENT."
- q: "¿Por qué es mala práctica escribir `EXCEPTION WHEN OTHERS THEN NULL;`?"
  options: ["Porque no compila", "Porque oculta todos los errores y el programa parece funcionar aunque falle", "Porque hace COMMIT", "Porque solo captura NO_DATA_FOUND"]
  answer: 1
  explain: "Silencia cualquier error. Si se captura OTHERS, hay que registrar el error y volver a lanzarlo con RAISE."
- q: "¿Qué cursor abre, recorre y cierra automáticamente el resultado de una consulta?"
  options: ["El cursor implícito de un UPDATE", "El bucle FOR de cursor", "OPEN ... FETCH sin CLOSE", "SQL%ROWCOUNT"]
  answer: 1
  explain: "`FOR r IN cursor LOOP` gestiona la apertura, la lectura y el cierre, incluso si se produce una excepción."
- q: "¿Qué paquete de Oracle permite programar la ejecución periódica de un procedimiento?"
  options: ["DBMS_OUTPUT", "DBMS_STATS", "DBMS_SCHEDULER", "UTL_FILE"]
  answer: 2
  explain: "DBMS_SCHEDULER crea y gestiona tareas (jobs) con calendarios. En MySQL el equivalente es CREATE EVENT."
{{< /quiz >}}

## Referencias

- [Oracle AI Database 26ai: PL/SQL Language Reference](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/).
- [Oracle AI Database 26ai: PL/SQL Packages and Types Reference (*DBMS_SCHEDULER*, *DBMS_OUTPUT*)](https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/).
- [Oracle AI Database 26ai: Administrator's Guide, *Scheduling Jobs with Oracle Scheduler*](https://docs.oracle.com/en/database/oracle/oracle-database/26/admin/).
- [MySQL 8.4: *Stored Objects*](https://dev.mysql.com/doc/refman/8.4/en/stored-objects.html) y [PostgreSQL: *PL/pgSQL*](https://www.postgresql.org/docs/current/plpgsql.html), para la comparación.
