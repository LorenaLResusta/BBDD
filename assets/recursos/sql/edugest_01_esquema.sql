-- =====================================================================
-- EduGest · Script 01 · Esquema relacional
-- Proyecto transversal del módulo 0484 Bases de datos (DAM/DAW)
-- SGBD: Oracle AI Database 26ai Free (compatible con 19c / 21c / 23ai)
-- Ejecutar conectado como el usuario EDUGEST (ver script 00).
--
-- Este script es la SOLUCIÓN DE REFERENCIA del diseño que se construye
-- en las unidades 2 a 5. A partir de la UD06 todo el grupo trabaja con
-- este esquema para que los resultados de las consultas coincidan.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 0. Limpieza (permite relanzar el script). El orden importa: primero
--    las tablas que dependen de otras. CASCADE CONSTRAINTS elimina las
--    claves ajenas que apuntan a la tabla borrada.
-- ---------------------------------------------------------------------
DROP TABLE falta_asistencia CASCADE CONSTRAINTS PURGE;
DROP TABLE imparte          CASCADE CONSTRAINTS PURGE;
DROP TABLE matricula        CASCADE CONSTRAINTS PURGE;
DROP TABLE alumno           CASCADE CONSTRAINTS PURGE;
DROP TABLE grupo            CASCADE CONSTRAINTS PURGE;
DROP TABLE modulo           CASCADE CONSTRAINTS PURGE;
DROP TABLE ciclo            CASCADE CONSTRAINTS PURGE;
DROP TABLE profesor         CASCADE CONSTRAINTS PURGE;
DROP TABLE departamento     CASCADE CONSTRAINTS PURGE;
-- La primera vez aparecerá ORA-00942 (la tabla no existe): es normal.
-- En Oracle 23ai/26ai puede usarse: DROP TABLE IF EXISTS departamento ...

-- ---------------------------------------------------------------------
-- 1. DEPARTAMENTO
-- ---------------------------------------------------------------------
CREATE TABLE departamento (
    id_departamento  NUMBER(3)     CONSTRAINT pk_departamento PRIMARY KEY,
    nombre           VARCHAR2(60)  CONSTRAINT nn_departamento_nombre NOT NULL,
    id_jefe          NUMBER(5),    -- FK a PROFESOR: se añade más abajo
    CONSTRAINT uq_departamento_nombre UNIQUE (nombre)
);

-- ---------------------------------------------------------------------
-- 2. PROFESOR
-- ---------------------------------------------------------------------
CREATE TABLE profesor (
    id_profesor      NUMBER(5)     CONSTRAINT pk_profesor PRIMARY KEY,
    dni              CHAR(9)       CONSTRAINT nn_profesor_dni NOT NULL,
    nombre           VARCHAR2(40)  CONSTRAINT nn_profesor_nombre NOT NULL,
    apellidos        VARCHAR2(80)  CONSTRAINT nn_profesor_apellidos NOT NULL,
    email            VARCHAR2(100) CONSTRAINT nn_profesor_email NOT NULL,
    fecha_alta       DATE          DEFAULT SYSDATE CONSTRAINT nn_profesor_alta NOT NULL,
    especialidad     VARCHAR2(60),
    id_departamento  NUMBER(3)     CONSTRAINT nn_profesor_dpto NOT NULL,
    CONSTRAINT uq_profesor_dni   UNIQUE (dni),
    CONSTRAINT uq_profesor_email UNIQUE (email),
    CONSTRAINT ck_profesor_email CHECK (email LIKE '%_@_%._%'),
    CONSTRAINT fk_profesor_departamento FOREIGN KEY (id_departamento)
        REFERENCES departamento (id_departamento)
);

-- Dependencia circular DEPARTAMENTO <-> PROFESOR: la FK del jefe se
-- crea cuando ambas tablas existen.
ALTER TABLE departamento ADD CONSTRAINT fk_departamento_jefe
    FOREIGN KEY (id_jefe) REFERENCES profesor (id_profesor);

-- ---------------------------------------------------------------------
-- 3. CICLO
-- ---------------------------------------------------------------------
CREATE TABLE ciclo (
    cod_ciclo      VARCHAR2(5)   CONSTRAINT pk_ciclo PRIMARY KEY,
    nombre         VARCHAR2(100) CONSTRAINT nn_ciclo_nombre NOT NULL,
    grado          VARCHAR2(8)   CONSTRAINT nn_ciclo_grado NOT NULL,
    horas_totales  NUMBER(4)     CONSTRAINT nn_ciclo_horas NOT NULL,
    CONSTRAINT ck_ciclo_grado CHECK (grado IN ('BASICO', 'MEDIO', 'SUPERIOR')),
    CONSTRAINT ck_ciclo_horas CHECK (horas_totales > 0)
);

-- ---------------------------------------------------------------------
-- 4. MODULO
--    El mismo código oficial (p. ej. 0484) existe en varios ciclos, por
--    eso la clave primaria es un identificador artificial y la pareja
--    (codigo, cod_ciclo) es una clave alternativa (UNIQUE).
-- ---------------------------------------------------------------------
CREATE TABLE modulo (
    id_modulo   NUMBER(5)     CONSTRAINT pk_modulo PRIMARY KEY,
    codigo      CHAR(4)       CONSTRAINT nn_modulo_codigo NOT NULL,
    nombre      VARCHAR2(100) CONSTRAINT nn_modulo_nombre NOT NULL,
    cod_ciclo   VARCHAR2(5)   CONSTRAINT nn_modulo_ciclo NOT NULL,
    curso       NUMBER(1)     CONSTRAINT nn_modulo_curso NOT NULL,
    horas       NUMBER(3)     CONSTRAINT nn_modulo_horas NOT NULL,
    CONSTRAINT uq_modulo_codigo_ciclo UNIQUE (codigo, cod_ciclo),
    CONSTRAINT ck_modulo_curso CHECK (curso IN (1, 2)),
    CONSTRAINT ck_modulo_horas CHECK (horas > 0),
    CONSTRAINT fk_modulo_ciclo FOREIGN KEY (cod_ciclo) REFERENCES ciclo (cod_ciclo)
);

-- ---------------------------------------------------------------------
-- 5. GRUPO
--    Un profesor solo puede ser tutor de un grupo (UNIQUE sobre id_tutor;
--    UNIQUE admite varios NULL: grupos todavía sin tutor).
-- ---------------------------------------------------------------------
CREATE TABLE grupo (
    cod_grupo  VARCHAR2(10) CONSTRAINT pk_grupo PRIMARY KEY,
    cod_ciclo  VARCHAR2(5)  CONSTRAINT nn_grupo_ciclo NOT NULL,
    curso      NUMBER(1)    CONSTRAINT nn_grupo_curso NOT NULL,
    turno      CHAR(1)      CONSTRAINT nn_grupo_turno NOT NULL,
    id_tutor   NUMBER(5),
    CONSTRAINT ck_grupo_curso CHECK (curso IN (1, 2)),
    CONSTRAINT ck_grupo_turno CHECK (turno IN ('M', 'T')),
    CONSTRAINT uq_grupo_tutor UNIQUE (id_tutor),
    CONSTRAINT fk_grupo_ciclo FOREIGN KEY (cod_ciclo) REFERENCES ciclo (cod_ciclo),
    CONSTRAINT fk_grupo_tutor FOREIGN KEY (id_tutor) REFERENCES profesor (id_profesor)
        ON DELETE SET NULL
);

-- ---------------------------------------------------------------------
-- 6. ALUMNO
--    Columna identidad: si no se indica id_alumno, Oracle lo genera
--    a partir de 1001 (los datos de ejemplo usan 1..32).
-- ---------------------------------------------------------------------
CREATE TABLE alumno (
    id_alumno         NUMBER(6) GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH 1001)
                      CONSTRAINT pk_alumno PRIMARY KEY,
    nia               CHAR(8)       CONSTRAINT nn_alumno_nia NOT NULL,
    dni               CHAR(9),
    nombre            VARCHAR2(40)  CONSTRAINT nn_alumno_nombre NOT NULL,
    apellidos         VARCHAR2(80)  CONSTRAINT nn_alumno_apellidos NOT NULL,
    fecha_nacimiento  DATE          CONSTRAINT nn_alumno_fnac NOT NULL,
    email             VARCHAR2(100),
    telefono          VARCHAR2(15),
    localidad         VARCHAR2(50),
    cod_grupo         VARCHAR2(10),
    CONSTRAINT uq_alumno_nia   UNIQUE (nia),
    CONSTRAINT uq_alumno_dni   UNIQUE (dni),
    CONSTRAINT uq_alumno_email UNIQUE (email),
    CONSTRAINT fk_alumno_grupo FOREIGN KEY (cod_grupo) REFERENCES grupo (cod_grupo)
);

-- ---------------------------------------------------------------------
-- 7. MATRICULA  (relación N:M ALUMNO-MODULO con atributos)
-- ---------------------------------------------------------------------
CREATE TABLE matricula (
    id_matricula     NUMBER(8) GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH 20001)
                     CONSTRAINT pk_matricula PRIMARY KEY,
    id_alumno        NUMBER(6)    CONSTRAINT nn_matricula_alumno NOT NULL,
    id_modulo        NUMBER(5)    CONSTRAINT nn_matricula_modulo NOT NULL,
    curso_academico  CHAR(7)      CONSTRAINT nn_matricula_curso NOT NULL,
    fecha_matricula  DATE         DEFAULT SYSDATE CONSTRAINT nn_matricula_fecha NOT NULL,
    convocatoria     NUMBER(1)    DEFAULT 1 CONSTRAINT nn_matricula_conv NOT NULL,
    nota_final       NUMBER(4,2),
    CONSTRAINT uq_matricula UNIQUE (id_alumno, id_modulo, curso_academico),
    CONSTRAINT ck_matricula_curso CHECK (REGEXP_LIKE(curso_academico, '^[0-9]{4}-[0-9]{2}$')),
    CONSTRAINT ck_matricula_conv  CHECK (convocatoria BETWEEN 1 AND 4),
    CONSTRAINT ck_matricula_nota  CHECK (nota_final BETWEEN 0 AND 10),
    CONSTRAINT fk_matricula_alumno FOREIGN KEY (id_alumno) REFERENCES alumno (id_alumno)
        ON DELETE CASCADE,
    CONSTRAINT fk_matricula_modulo FOREIGN KEY (id_modulo) REFERENCES modulo (id_modulo)
);

-- ---------------------------------------------------------------------
-- 8. IMPARTE  (qué docente imparte cada módulo a cada grupo y curso)
-- ---------------------------------------------------------------------
CREATE TABLE imparte (
    id_modulo        NUMBER(5)    ,
    cod_grupo        VARCHAR2(10) ,
    curso_academico  CHAR(7)      ,
    id_profesor      NUMBER(5)    CONSTRAINT nn_imparte_profesor NOT NULL,
    horas_semanales  NUMBER(2)    CONSTRAINT nn_imparte_horas NOT NULL,
    CONSTRAINT pk_imparte PRIMARY KEY (id_modulo, cod_grupo, curso_academico),
    CONSTRAINT ck_imparte_horas CHECK (horas_semanales BETWEEN 1 AND 12),
    CONSTRAINT fk_imparte_modulo   FOREIGN KEY (id_modulo)   REFERENCES modulo (id_modulo),
    CONSTRAINT fk_imparte_grupo    FOREIGN KEY (cod_grupo)   REFERENCES grupo (cod_grupo),
    CONSTRAINT fk_imparte_profesor FOREIGN KEY (id_profesor) REFERENCES profesor (id_profesor)
);

-- ---------------------------------------------------------------------
-- 9. FALTA_ASISTENCIA
-- ---------------------------------------------------------------------
CREATE TABLE falta_asistencia (
    id_falta      NUMBER(8) GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH 1001)
                  CONSTRAINT pk_falta PRIMARY KEY,
    id_matricula  NUMBER(8)  CONSTRAINT nn_falta_matricula NOT NULL,
    fecha         DATE       CONSTRAINT nn_falta_fecha NOT NULL,
    horas         NUMBER(1)  CONSTRAINT nn_falta_horas NOT NULL,
    justificada   CHAR(1)    DEFAULT 'N' CONSTRAINT nn_falta_just NOT NULL,
    CONSTRAINT uq_falta UNIQUE (id_matricula, fecha),
    CONSTRAINT ck_falta_horas CHECK (horas BETWEEN 1 AND 6),
    CONSTRAINT ck_falta_just  CHECK (justificada IN ('S', 'N')),
    CONSTRAINT fk_falta_matricula FOREIGN KEY (id_matricula) REFERENCES matricula (id_matricula)
        ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- 10. Índices sobre claves ajenas
--     Oracle crea índices automáticamente para PRIMARY KEY y UNIQUE,
--     pero NO para FOREIGN KEY. Indexarlas acelera los JOIN y evita
--     bloqueos de tabla al borrar en la tabla padre.
-- ---------------------------------------------------------------------
CREATE INDEX ix_profesor_dpto     ON profesor (id_departamento);
CREATE INDEX ix_modulo_ciclo      ON modulo (cod_ciclo);
CREATE INDEX ix_alumno_grupo      ON alumno (cod_grupo);
CREATE INDEX ix_matricula_modulo  ON matricula (id_modulo);
CREATE INDEX ix_imparte_profesor  ON imparte (id_profesor);
CREATE INDEX ix_imparte_grupo     ON imparte (cod_grupo);
-- matricula(id_alumno) y falta_asistencia(id_matricula) ya quedan
-- cubiertas por la parte inicial de sus índices UNIQUE.

-- ---------------------------------------------------------------------
-- 11. Comentarios en el diccionario de datos (documentación del diseño)
-- ---------------------------------------------------------------------
COMMENT ON TABLE matricula IS 'Matrícula de un alumno en un módulo para un curso académico';
COMMENT ON COLUMN matricula.nota_final IS 'NULL = sin calificar / no presentado';
COMMENT ON COLUMN matricula.convocatoria IS 'Número de convocatoria (1 a 4)';
COMMENT ON TABLE imparte IS 'Asignación docente: profesor que imparte un módulo a un grupo en un curso';

-- Comprobación: tablas y restricciones creadas
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT table_name, constraint_name, constraint_type
FROM   user_constraints
WHERE  constraint_name NOT LIKE 'SYS%' AND constraint_name NOT LIKE 'BIN$%'
ORDER  BY table_name, constraint_type, constraint_name;
