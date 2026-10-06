---
title: "Bases de Datos"
bookToc: true
---

# Bases de Datos · Módulo 0484

Apuntes del módulo profesional **0484. Bases de datos**, común a los ciclos formativos de grado superior **Desarrollo de Aplicaciones Multiplataforma (DAM)** y **Desarrollo de Aplicaciones Web (DAW)**. Curso **2026/27**.

| Característica | Valor |
|---|---|
| **Referencia curricular** | Real Decreto 405/2023, de 29 de mayo (actualiza los títulos de DAM y DAW) |
| **Duración (enseñanzas mínimas)** | 105 horas · 12 créditos ECTS |
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
    E --> F[Consultas<br/>UD06-UD07]
    F --> G[DML y transacciones<br/>UD08]
    G --> H[PL/SQL<br/>UD09]
    C -.comparación.-> I[NoSQL<br/>UD10]
    H -.-> I
```

## Unidades didácticas

Cada unidad tiene dos páginas: **teoría** (conceptos, ejemplos y autoevaluación) y **prácticas** (prácticas guiadas, autónomas, retos y la tarea del proyecto EduGest).

<div class="bd-cards">
  <div class="bd-card"><span class="bd-card-ra">RA1</span><h3>UD01 · Sistemas de almacenamiento y SGBD</h3><p>Ficheros frente a bases de datos, arquitectura y funciones de un SGBD, tipos de bases de datos, distribución, Big Data y protección de datos.</p><div class="bd-card-links"><a href="ud01-introduccion/ud01-teoria/">Teoría</a> · <a href="ud01-introduccion/ud01-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6</span><h3>UD02 · Modelo Entidad/Relación</h3><p>Análisis de requisitos, entidades, atributos, relaciones, cardinalidades, entidades débiles y extensiones EER.</p><div class="bd-card-links"><a href="ud02-modelo-er/ud02-teoria/">Teoría</a> · <a href="ud02-modelo-er/ud02-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6 · RA2</span><h3>UD03 · Modelo relacional</h3><p>Relaciones, claves, restricciones, integridad y transformación del modelo E/R al modelo relacional.</p><div class="bd-card-links"><a href="ud03-modelo-relacional/ud03-teoria/">Teoría</a> · <a href="ud03-modelo-relacional/ud03-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA6</span><h3>UD04 · Normalización</h3><p>Anomalías, dependencias funcionales, 1FN, 2FN, 3FN y FNBC. Restricciones que el diseño lógico no puede expresar.</p><div class="bd-card-links"><a href="ud04-normalizacion/ud04-teoria/">Teoría</a> · <a href="ud04-normalizacion/ud04-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA2</span><h3>UD05 · Definición y control de datos</h3><p>DDL en Oracle: tablas, tipos, restricciones, índices, vistas y secuencias. DCL: usuarios, roles y privilegios.</p><div class="bd-card-links"><a href="ud05-ddl-dcl/ud05-teoria/">Teoría</a> · <a href="ud05-ddl-dcl/ud05-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA3</span><h3>UD06 · Consultas sobre una tabla</h3><p>SELECT, proyección, selección, ordenación, operadores, valores nulos y funciones de fila.</p><div class="bd-card-links"><a href="ud06-consultas-basicas/ud06-teoria/">Teoría</a> · <a href="ud06-consultas-basicas/ud06-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA3</span><h3>UD07 · Consultas avanzadas</h3><p>Agrupamiento, composiciones internas y externas, subconsultas, operadores de conjuntos y optimización.</p><div class="bd-card-links"><a href="ud07-consultas-avanzadas/ud07-teoria/">Teoría</a> · <a href="ud07-consultas-avanzadas/ud07-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA4</span><h3>UD08 · Manipulación de datos y transacciones</h3><p>INSERT, UPDATE, DELETE, MERGE, transacciones, ACID, concurrencia y bloqueos.</p><div class="bd-card-links"><a href="ud08-dml-transacciones/ud08-teoria/">Teoría</a> · <a href="ud08-dml-transacciones/ud08-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA5</span><h3>UD09 · Programación con PL/SQL</h3><p>Bloques, variables, control de flujo, procedimientos, funciones, cursores, excepciones, triggers y tareas programadas.</p><div class="bd-card-links"><a href="ud09-plsql/ud09-teoria/">Teoría</a> · <a href="ud09-plsql/ud09-practicas/">Prácticas</a></div></div>
  <div class="bd-card"><span class="bd-card-ra">RA7</span><h3>UD10 · Bases de datos NoSQL</h3><p>Tipos de bases de datos no relacionales, modelado documental y operaciones CRUD y de agregación con MongoDB.</p><div class="bd-card-links"><a href="ud10-nosql/ud10-teoria/">Teoría</a> · <a href="ud10-nosql/ud10-practicas/">Prácticas</a></div></div>
</div>

## Relación entre unidades y resultados de aprendizaje

| Unidad | RA1 | RA2 | RA3 | RA4 | RA5 | RA6 | RA7 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| UD01 Sistemas de almacenamiento y SGBD | ● | ○ | | | | | ○ |
| UD02 Modelo Entidad/Relación | | | | | | ● | |
| UD03 Modelo relacional | | ○ | | | | ● | |
| UD04 Normalización | | | | | | ● | |
| UD05 Definición y control de datos | | ● | | | | ○ | |
| UD06 Consultas sobre una tabla | | | ● | | ○ | | |
| UD07 Consultas avanzadas | | ○ | ● | | | | |
| UD08 Manipulación y transacciones | | | | ● | | ○ | |
| UD09 Programación PL/SQL | | | | ○ | ● | ○ | |
| UD10 Bases de datos NoSQL | ○ | | | | | | ● |

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
- [Curso de Bases de Datos de Francisco Miguel García](https://fmgarcia.github.io/CursosGithubIO/CursoBasesDatos/). Referencia didáctica complementaria.
- [Documentación de Oracle AI Database 26ai](https://docs.oracle.com/en/database/oracle/oracle-database/26/).
- [Manual de MongoDB](https://www.mongodb.com/docs/manual/).
