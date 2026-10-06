-- =====================================================================
-- EduGest · Script 00 · Creación del usuario/esquema EDUGEST
-- SGBD: Oracle AI Database 26ai Free (contenedor o instalación local)
-- Ejecutar conectado como SYSTEM a la base de datos conectable FREEPDB1:
--     sql system/<contraseña>@//localhost:1521/FREEPDB1
-- =====================================================================

-- En Oracle un USUARIO y su ESQUEMA son lo mismo: todos los objetos
-- que cree EDUGEST (tablas, vistas, índices...) pertenecen a su esquema.
-- Si el usuario ya existía y quieres empezar de cero:
-- DROP USER edugest CASCADE;

CREATE USER edugest IDENTIFIED BY "Edugest_2026"
    DEFAULT TABLESPACE users
    QUOTA UNLIMITED ON users;

-- Rol pensado para desarrolladores (Oracle 23ai y posteriores).
-- Incluye CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE,
-- CREATE PROCEDURE, CREATE TRIGGER, CREATE TYPE, etc.
GRANT DB_DEVELOPER_ROLE TO edugest;

-- Alternativa para Oracle 19c/21c (sin DB_DEVELOPER_ROLE):
-- GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE,
--       CREATE PROCEDURE, CREATE TRIGGER, CREATE SYNONYM TO edugest;

-- Necesario más adelante (UD09) para programar tareas con DBMS_SCHEDULER
GRANT CREATE JOB TO edugest;

-- Comprobación
SELECT username, default_tablespace, account_status
FROM   dba_users
WHERE  username = 'EDUGEST';
