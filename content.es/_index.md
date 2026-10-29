---
title: "Bases de Datos"
bookToc: true
---

# Bases de Datos · Módulo 0484

Apuntes del módulo profesional **0484. Bases de datos**, común a los ciclos formativos de grado superior **Desarrollo de Aplicaciones Multiplataforma (DAM)** y **Desarrollo de Aplicaciones Web (DAW)**. Curso **2026/27**.

| Característica | Valor |
|---|---|
| **Referencia curricular** | Real Decreto 405/2023, de 29 de mayo (actualiza los títulos de DAM y DAW) |
| **Duración** | 105 horas (enseñanzas mínimas) · 12 créditos ECTS · 166 horas de aula en el centro (144 hasta la FE y 22 en junio) |
| **Resultados de aprendizaje** | 7 (RA1 a RA7) con 57 criterios de evaluación |
| **SGBD relacional** | Oracle AI Database 26ai Free (23.26) |
| **SGBD no relacional** | MongoDB Community Server 8.0 |
| **Proyecto común** | [EduGest: gestión de un centro educativo](/guia/proyecto-edugest) |

> [!NOTE]
> Estos apuntes **no son un manual de SQL**. Están organizados para que alcances los resultados de aprendizaje oficiales del módulo. Recorren el ciclo de vida completo de una base de datos:
> **análisis → modelo conceptual → modelo lógico → normalización → diseño físico → implementación → consultas → modificación → programación → optimización → NoSQL.**

## El ciclo de trabajo con una base de datos

```mermaid
flowchart LR
    A[Requisitos] --> B[Modelo E/R<br/>UD02]
    B --> C[Modelo relacional<br/>UD03]
    C --> D[Normalización<br/>UD04]
    D --> E[DDL / DCL<br/>UD05]
    E --> F[Consultas<br/>UD06]
    F --> G[DML y transacciones<br/>UD07]
    G --> H[PL/SQL<br/>UD08]
    C -.comparación.-> I[NoSQL<br/>UD09]
    H -.-> I
```

## Guía didáctica del curso 2026/27

El módulo se imparte con una carga de **166 horas de aula** (5 horas semanales, una por día lectivo). **144 horas** se imparten entre el **9 de septiembre de 2026** y el **30 de abril de 2027**: el **3 de mayo** el alumnado se incorpora a la Formación en Empresa (FE) por ser de primer curso presencial. Las **22 horas restantes** se imparten en **junio**, como refuerzo de consultas y proyecto EduGest, con fechas por concretar con el centro. Las horas se reparten en tres evaluaciones y se han ajustado al calendario escolar y a las fechas de pruebas comunicadas por el centro.

> [!NOTE]
> Las enseñanzas mínimas del RD 405/2023 fijan 105 horas para el módulo. Las 166 horas son las de **horario del centro** (144 hasta el inicio de la FE y 22 en junio); el exceso sobre el mínimo se dedica a la práctica guiada, al proyecto EduGest y al refuerzo. Todos los criterios de evaluación se cubren en las unidades; el reparto de horas es orientativo y puede ajustarse a cada grupo.

{{< calendario >}}

### Reparto de horas por evaluación

| Evaluación | Unidad | Horas | Del | Al | RA principal |
|---|---|:-:|---|---|---|
| **1ª** (65 h) | UD01 · Almacenamiento de la información | 3 | 09/09/2026 | 11/09/2026 | RA1 |
|  | UD02 · Diseño conceptual (Entidad/Relación) | 26 | 14/09/2026 | 21/10/2026 | RA6 |
|  | UD03 · Modelo relacional | 20 | 22/10/2026 | 18/11/2026 | RA6 · RA2 |
|  | UD04 · Normalización | 2 | 19/11/2026 | 20/11/2026 | RA6 |
|  | UD05 · DDL: lenguaje de definición de datos (parte 1) | 14 | 23/11/2026 | 11/12/2026 | RA2 |
| **2ª** (43 h) | UD05 · DDL: lenguaje de definición de datos (parte 2) | 21 | 14/12/2026 | 27/01/2027 | RA2 |
|  | UD06 · Consultas (DML) (parte 1) | 22 | 28/01/2027 | 26/02/2027 | RA3 · RA5 |
| **3ª** (36 h) | UD06 · Consultas (DML) (parte 2) | 18 | 01/03/2027 | 06/04/2027 | RA3 · RA5 |
| | *Vacaciones de Pascua* | | 25/03/2027 | 05/04/2027 | |
|  | UD07 · DML, transacciones y concurrencia | 3 | 07/04/2027 | 09/04/2027 | RA4 |
|  | UD08 · Programación en PL/SQL (parte 1) | 15 | 12/04/2027 | 30/04/2027 | RA5 |
| | *Formación en Empresa (FE)* | | 03/05/2027 | 18/06/2027 | |
| **Junio** (22 h) | UD08 · Programación en PL/SQL (parte 2) | 20 | 21/06/2027 | 30/06/2027 (por concretar) | RA5 |
| | UD09 · Bases de datos no relacionales | 2 | | | RA7 |
| | **Total** | **166** | | | |

La evaluación extraordinaria está prevista para el **21 de junio de 2027**. Como la FE ocupa de mayo a junio, la prueba de la 3ª evaluación se adelanta a la última semana de abril (del 28 al 30).

### Criterios de la planificación

- **Prioridades.** El tiempo del módulo se concentra en el diseño conceptual (UD02), el modelo relacional (UD03), el DDL (UD05), las consultas y la manipulación de datos (UD06, 40 horas de aula) y PL/SQL (UD08). Normalización (UD04), transacciones (UD07) y NoSQL (UD09) se reducen a lo esencial; sus apuntes se mantienen completos como material de estudio y de ampliación. Las pruebas de evaluación cuentan dentro de las horas de la unidad que se esté impartiendo.
- **Teoría y práctica en la misma unidad.** Cada unidad indica en su página de teoría una *temporalización* con el reparto de sesiones entre teoría (T) y práctica (P). La suma de horas de cada unidad coincide con la de esta tabla.
- **Práctica guiada en el aula, práctica autónoma fuera de ella.** Las prácticas guiadas y la tarea del proyecto EduGest se hacen en clase. Las prácticas autónomas, los retos y las ampliaciones son trabajo personal, y las dudas se trabajan en las sesiones de práctica.
- **Pruebas de evaluación.** Cada evaluación reserva 3 horas a la prueba y a su revisión, en la semana indicada por el centro para los ciclos de grado superior.
- **Un día lectivo equivale a una hora.** Los festivos y los días sin docencia no cuentan. No hay semana de refuerzo: los días que se pierdan por fiestas locales o actividades del centro se recuperan recortando las sesiones de práctica de la última unidad impartida.

> [!WARNING]
> **La Formación en Empresa empieza el 3 de mayo.** El alumnado de primer curso presencial se marcha a la FE el 3 de mayo, por lo que la 3ª evaluación **se comprime en abril** y las unidades finales se reparten así: UD07 con 3 horas, UD08 con 15 horas antes de la FE y 20 en junio, y UD09 (2 horas) en junio. Eso obliga a que una parte de las prácticas de esas unidades se haga como **trabajo autónomo**; cada página de teoría indica qué prácticas se hacen en el aula y cuáles fuera de ella. Si el calendario cambia, el archivo `data/planificacion.json` y las tablas de *temporalización* de cada unidad deben ajustarse a la vez.

> [!CAUTION]
> **Calendario provisional.** Las fechas proceden del calendario escolar provisional 2026/27 y de las fechas de evaluación comunicadas por el centro. Los festivos locales y los tres días no lectivos que fije el centro **no están descontados**: como no queda margen antes de la FE, habrá que recortar sesiones de práctica de UD08 y de las unidades finales. Cuando se publique el calendario definitivo debe revisarse el archivo `data/planificacion.json`; la tabla y el calendario se actualizan solos y la compilación falla si las horas de una unidad dejan de sumar.

## Unidades didácticas

Cada unidad tiene dos páginas: **teoría** (conceptos, ejemplos y autoevaluación) y **prácticas** (prácticas guiadas, autónomas, retos y la tarea del proyecto EduGest).

<div class="bd-cards">
  <div class="bd-card"><span class="bd-card-ra">RA1</span><h3>UD01 · Sistemas de almacenamiento y SGBD</h3><p>Ficheros frente a bases de datos, arquitectura y funciones de un SGBD, tipos de bases de datos, distribución, Big Data y protección de datos.</p><div class="bd-card-links"><a href="ud01-introduccion/ud01-teoria/">Teoría</a> · <a href="ud01-introduccion/ud01-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6</span><h3>UD02 · Modelo Entidad/Relación</h3><p>Análisis de requisitos, entidades, atributos, relaciones, cardinalidades, entidades débiles y extensiones EER.</p><div class="bd-card-links"><a href="ud02-modelo-er/ud02-teoria/">Teoría</a> · <a href="ud02-modelo-er/ud02-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6 · RA2</span><h3>UD03 · Modelo relacional</h3><p>Relaciones, claves, restricciones, integridad y transformación del modelo E/R al modelo relacional.</p><div class="bd-card-links"><a href="ud03-modelo-relacional/ud03-teoria/">Teoría</a> · <a href="ud03-modelo-relacional/ud03-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6</span><h3>UD04 · Normalización</h3><p>Anomalías, dependencias funcionales, 1FN, 2FN, 3FN y FNBC. Restricciones que el diseño lógico no puede expresar.</p><div class="bd-card-links"><a href="ud04-normalizacion/ud04-teoria/">Teoría</a> · <a href="ud04-normalizacion/ud04-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA2</span><h3>UD05 · DDL: definición de datos</h3><p>DDL en Oracle: tablas, tipos, restricciones, índices, vistas y secuencias. DCL: usuarios, roles y privilegios.</p><div class="bd-card-links"><a href="ud05-ddl-dcl/ud05-teoria/">Teoría</a> · <a href="ud05-ddl-dcl/ud05-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA3</span><h3>UD06 · Consultas (DML)</h3><p>SELECT, valores nulos, funciones de fila, composiciones, agrupamientos, subconsultas y optimización. Dos partes: una tabla y varias tablas.</p><div class="bd-card-links"><a href="ud06-consultas/ud06-teoria/">Teoría I</a> · <a href="ud06-consultas/ud06-practicas/">Prácticas I</a> · <a href="ud06-consultas/ud06-teoria-avanzada/">Teoría II</a> · <a href="ud06-consultas/ud06-practicas-avanzadas/">Prácticas II</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA4</span><h3>UD07 · Manipulación de datos y transacciones</h3><p>INSERT, UPDATE, DELETE, MERGE, transacciones, ACID, concurrencia y bloqueos.</p><div class="bd-card-links"><a href="ud07-dml-transacciones/ud07-teoria/">Teoría</a> · <a href="ud07-dml-transacciones/ud07-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA5</span><h3>UD08 · Programación con PL/SQL</h3><p>Bloques, variables, control de flujo, procedimientos, funciones, cursores, excepciones, triggers y tareas programadas.</p><div class="bd-card-links"><a href="ud08-plsql/ud08-teoria/">Teoría</a> · <a href="ud08-plsql/ud08-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA7</span><h3>UD09 · Bases de datos NoSQL</h3><p>Tipos de bases de datos no relacionales, modelado documental y operaciones CRUD y de agregación con MongoDB.</p><div class="bd-card-links"><a href="ud09-nosql/ud09-teoria/">Teoría</a> · <a href="ud09-nosql/ud09-practicas/">Prácticas</a></div></div>
</div>

## Relación entre unidades y resultados de aprendizaje

| Unidad | RA1 | RA2 | RA3 | RA4 | RA5 | RA6 | RA7 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| UD01 Sistemas de almacenamiento y SGBD | ● | ○ | | | | | ○ |
| UD02 Modelo Entidad/Relación | | | | | | ● | |
| UD03 Modelo relacional | | ○ | | | | ● | |
| UD04 Normalización | | | | | | ● | |
| UD05 DDL: definición de datos | | ● | | | | ○ | |
| UD06 Consultas (DML) | | ○ | ● | | ○ | | |
| UD07 Manipulación y transacciones | | | | ● | | ○ | |
| UD08 Programación PL/SQL | | | | ○ | ● | ○ | |
| UD09 Bases de datos NoSQL | ○ | | | | | | ● |

● contribución principal · ○ contribución secundaria. El detalle por criterio de evaluación está en [Resultados de aprendizaje y criterios de evaluación](/guia/ra-ce).

## Cómo leer estos apuntes

Los apuntes usan cuadros de colores para destacar información:

> [!TIP]
> **Consejo.** Una forma más cómoda o profesional de hacer algo.

> [!WARNING]
> **Atención.** Un error habitual o algo que puede dar problemas.

> [!IMPORTANT]
> **Clave.** Un concepto imprescindible para el resultado de aprendizaje.

> [!CAUTION]
> **Peligro.** Una operación que puede destruir o exponer datos.

{{% details title="Pista (despliégame)" %}}
Las pistas y las **soluciones** de los ejercicios aparecen plegadas. Intenta resolver el ejercicio antes de abrirlas.
{{% /details %}}

Los fragmentos de código indican siempre el gestor al que corresponden, por ejemplo {{< sgbd "Oracle 26ai" >}}, {{< sgbd "MongoDB 8.0" >}} o {{< sgbd "SQL estándar" >}}.

Consulta también la [guía del módulo](/guia): el proyecto EduGest, la instalación del entorno y las convenciones de las prácticas.

## Fuentes

- [Real Decreto 405/2023, de 29 de mayo](https://www.boe.es/buscar/act.php?id=BOE-A-2023-13221). Texto consolidado en el BOE.
- [Documentación de Oracle AI Database 26ai](https://docs.oracle.com/en/database/oracle/oracle-database/26/).
- [Manual de MongoDB](https://www.mongodb.com/docs/manual/).
