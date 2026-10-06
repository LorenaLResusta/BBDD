-- =====================================================================
-- EduGest · Script 02 · Datos de ejemplo (curso 2025-26)
-- SGBD: Oracle AI Database 26ai Free (compatible con 19c / 21c / 23ai)
-- Ejecutar conectado como EDUGEST después del script 01.
-- Datos ficticios generados para los apuntes del módulo 0484.
-- =====================================================================
SET DEFINE OFF

-- Departamentos (los jefes se asignan al final: dependencia circular)
INSERT INTO departamento (id_departamento, nombre) VALUES (1, 'Informática y Comunicaciones');
INSERT INTO departamento (id_departamento, nombre) VALUES (2, 'Formación y Orientación Laboral');
INSERT INTO departamento (id_departamento, nombre) VALUES (3, 'Inglés');
INSERT INTO departamento (id_departamento, nombre) VALUES (4, 'Matemáticas');
INSERT INTO departamento (id_departamento, nombre) VALUES (5, 'Administración y Gestión');

-- Profesorado
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (101, '21456789C', 'Marta', 'Soler Ivars', 'msoler@edugest.es', DATE '2009-09-01', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (102, '48765432G', 'Javier', 'Pastor Gil', 'jpastor@edugest.es', DATE '2012-09-01', 'Sistemas y Aplicaciones Informáticas', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (103, '74123658V', 'Lucía', 'Ferrándiz Mora', 'lferrandiz@edugest.es', DATE '2015-09-01', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (104, '20987456P', 'Andrés', 'Navarro Ruiz', 'anavarro@edugest.es', DATE '2018-09-03', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (105, '33658741N', 'Elena', 'Brotons Sala', 'ebrotons@edugest.es', DATE '2020-09-01', 'Sistemas y Aplicaciones Informáticas', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (106, '45874123W', 'Raúl', 'Cano Vidal', 'rcano@edugest.es', DATE '2021-09-01', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (107, '52147896L', 'Nuria', 'Gómez Pérez', 'ngomez@edugest.es', DATE '2023-09-01', 'Informática', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (108, '48963214D', 'Pablo', 'Lillo Martí', 'plillo@edugest.es', DATE '2025-09-01', 'Sistemas y Aplicaciones Informáticas', 1);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (109, '21369874E', 'Carmen', 'Ortiz Llorca', 'cortiz@edugest.es', DATE '2010-09-01', 'Formación y Orientación Laboral', 2);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (110, '74589632W', 'Sergio', 'Ramos Climent', 'sramos@edugest.es', DATE '2019-09-02', 'Formación y Orientación Laboral', 2);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (111, '29874563R', 'Laura', 'Vicent Ribes', 'lvicent@edugest.es', DATE '2016-09-01', 'Inglés', 3);
INSERT INTO profesor (id_profesor, dni, nombre, apellidos, email, fecha_alta, especialidad, id_departamento) VALUES (112, '53214789B', 'David', 'Esteve Juan', 'desteve@edugest.es', DATE '2024-09-02', 'Administración de Empresas', 5);

-- Jefaturas de departamento
UPDATE departamento SET id_jefe = 101 WHERE id_departamento = 1;
UPDATE departamento SET id_jefe = 109 WHERE id_departamento = 2;
UPDATE departamento SET id_jefe = 111 WHERE id_departamento = 3;
UPDATE departamento SET id_jefe = 112 WHERE id_departamento = 5;

-- Ciclos formativos
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('DAM', 'Desarrollo de Aplicaciones Multiplataforma', 'SUPERIOR', 2000);
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('DAW', 'Desarrollo de Aplicaciones Web', 'SUPERIOR', 2000);
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('ASIR', 'Administración de Sistemas Informáticos en Red', 'SUPERIOR', 2000);
INSERT INTO ciclo (cod_ciclo, nombre, grado, horas_totales) VALUES ('SMR', 'Sistemas Microinformáticos y Redes', 'MEDIO', 2000);

-- Módulos profesionales (las horas son orientativas)
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (1, '0483', 'Sistemas informáticos', 'DAM', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (2, '0484', 'Bases de datos', 'DAM', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (3, '0485', 'Programación', 'DAM', 1, 256);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (4, '0487', 'Entornos de desarrollo', 'DAM', 1, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (5, '0373', 'Lenguajes de marcas y sistemas de gestión de información', 'DAM', 1, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (6, '0486', 'Acceso a datos', 'DAM', 2, 120);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (7, '0488', 'Desarrollo de interfaces', 'DAM', 2, 120);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (8, '0489', 'Programación multimedia y dispositivos móviles', 'DAM', 2, 100);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (9, '0490', 'Programación de servicios y procesos', 'DAM', 2, 80);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (10, '0491', 'Sistemas de gestión empresarial', 'DAM', 2, 100);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (11, '0483', 'Sistemas informáticos', 'DAW', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (12, '0484', 'Bases de datos', 'DAW', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (13, '0485', 'Programación', 'DAW', 1, 256);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (14, '0487', 'Entornos de desarrollo', 'DAW', 1, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (15, '0373', 'Lenguajes de marcas y sistemas de gestión de información', 'DAW', 1, 128);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (16, '0612', 'Desarrollo web en entorno cliente', 'DAW', 2, 140);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (17, '0613', 'Desarrollo web en entorno servidor', 'DAW', 2, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (18, '0614', 'Despliegue de aplicaciones web', 'DAW', 2, 80);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (19, '0615', 'Diseño de interfaces web', 'DAW', 2, 120);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (20, '0369', 'Implantación de sistemas operativos', 'ASIR', 1, 224);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (21, '0370', 'Planificación y administración de redes', 'ASIR', 1, 192);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (22, '0371', 'Fundamentos de hardware', 'ASIR', 1, 96);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (23, '0372', 'Gestión de bases de datos', 'ASIR', 1, 160);
INSERT INTO modulo (id_modulo, codigo, nombre, cod_ciclo, curso, horas) VALUES (24, '0373', 'Lenguajes de marcas y sistemas de gestión de información', 'ASIR', 1, 96);

-- Grupos
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('1DAM', 'DAM', 1, 'M', 103);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('2DAM', 'DAM', 2, 'M', 104);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('1DAW', 'DAW', 1, 'T', 106);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('2DAW', 'DAW', 2, 'T', 107);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('1ASIR', 'ASIR', 1, 'M', 105);
INSERT INTO grupo (cod_grupo, cod_ciclo, curso, turno, id_tutor) VALUES ('2ASIR', 'ASIR', 2, 'M', NULL);

-- Alumnado (id explícito; los nuevos alumnos recibirán id >= 1001 por la identidad)
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (1, '10450037', '55568986C', 'Adrián', 'Ferri Baeza', DATE '2006-10-18', 'adrianferri1@alu.edugest.es', '610608088', 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (2, '10450074', '44154098D', 'Rubén', 'Iborra Ferri', DATE '2005-11-01', 'rubeniborra2@alu.edugest.es', '699695434', 'Elche', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (3, '10450111', '50814806D', 'Noelia', 'Verdú Espí', DATE '2004-06-25', 'noeliaverdu3@alu.edugest.es', '660587809', 'Sant Joan d''Alacant', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (4, '10450148', '36608302F', 'Paula', 'Ferri Baeza', DATE '2005-01-10', 'paulaferri4@alu.edugest.es', NULL, 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (5, '10450185', NULL, 'Andrea', 'Brotons Soriano', DATE '2006-02-19', 'andreabrotons5@alu.edugest.es', '639572864', 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (6, '10450222', '76096799B', 'Tomás', 'Cerdá Pérez', DATE '2006-04-03', 'tomascerda6@alu.edugest.es', '659376353', 'Alicante', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (7, '10450259', '63874840E', 'Valeria', 'Quiles Marco', DATE '2004-01-20', 'valeriaquiles7@alu.edugest.es', '661054227', 'Sant Joan d''Alacant', '1DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (8, '10450296', '75326361G', 'Iván', 'Ripoll Agulló', DATE '2003-05-01', NULL, '645665668', 'Sant Joan d''Alacant', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (9, '10450333', '73361397E', 'Martina', 'Alemany Vidal', DATE '2005-04-18', 'martinaalemany9@alu.edugest.es', '686052214', 'Mutxamel', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (10, '10450370', '72926056W', 'Nerea', 'Cerdá Tomás', DATE '2005-08-04', 'nereacerda10@alu.edugest.es', NULL, 'San Vicente del Raspeig', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (11, '10450407', '35988837R', 'Hugo', 'Brotons Iborra', DATE '2005-12-17', 'hugobrotons11@alu.edugest.es', '678897218', 'Mutxamel', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (12, '10450444', '76691674Z', 'Lucía', 'Belda Quiles', DATE '2003-11-07', 'luciabelda12@alu.edugest.es', '630313272', 'San Vicente del Raspeig', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (13, '10450481', '27663211F', 'María', 'Domènech Quiles', DATE '2005-01-25', 'mariadomenech13@alu.edugest.es', '675664399', 'Alicante', '2DAM');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (14, '10450518', NULL, 'Carla', 'Valero Cerdá', DATE '2004-07-08', 'carlavalero14@alu.edugest.es', '676159146', 'Alicante', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (15, '10450555', '75229754C', 'Manuel', 'Soriano Domènech', DATE '2006-12-25', 'manuelsoriano15@alu.edugest.es', '621760503', 'Alicante', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (16, '10450592', '72901124W', 'Julia', 'Espí Marco', DATE '2006-12-01', 'juliaespi16@alu.edugest.es', NULL, 'Alicante', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (17, '10450629', '62431102V', 'Jorge', 'Iborra Alemany', DATE '2001-06-01', 'jorgeiborra17@alu.edugest.es', '674289054', 'El Campello', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (18, '10450666', '38842718L', 'Daniel', 'Alemany Pérez', DATE '2001-08-22', 'danielalemany18@alu.edugest.es', '664181554', 'El Campello', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (19, '10450703', '76182503V', 'Alba', 'Torregrosa Planelles', DATE '2006-12-21', NULL, '618940629', 'Mutxamel', '1DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (20, '10450740', '44338976J', 'Mateo', 'Sala Brotons', DATE '2003-04-09', 'mateosala20@alu.edugest.es', '628385636', 'Alicante', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (21, '10450777', '57150988J', 'Elena', 'Carbonell Soriano', DATE '2005-06-21', 'elenacarbonell21@alu.edugest.es', '633510324', 'El Campello', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (22, '10450814', '79846783Y', 'Sofía', 'Planelles Marco', DATE '2004-07-13', 'sofiaplanelles22@alu.edugest.es', NULL, 'Elche', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (23, '10450851', NULL, 'Sara', 'Amorós Guillem', DATE '2000-08-07', 'saraamoros23@alu.edugest.es', '631556041', 'Mutxamel', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (24, '10450888', '41037327Z', 'Nicolás', 'Verdú Castelló', DATE '2005-05-11', 'nicolasverdu24@alu.edugest.es', '622738887', 'Alicante', '2DAW');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (25, '10450925', '70931220W', 'Diego', 'Iborra Torregrosa', DATE '2005-09-04', 'diegoiborra25@alu.edugest.es', '646908920', 'San Vicente del Raspeig', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (26, '10450962', '64974513L', 'Víctor', 'Tomás Guillem', DATE '2006-12-06', 'victortomas26@alu.edugest.es', '627804543', 'Elche', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (27, '10450999', '65790137V', 'Álex', 'Tomás Vidal', DATE '2006-09-20', 'alextomas27@alu.edugest.es', '657158423', 'Mutxamel', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (28, '10451036', '48929967C', 'Pablo', 'Amorós Carbonell', DATE '2006-10-21', 'pabloamoros28@alu.edugest.es', NULL, 'Alicante', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (29, '10451073', '65878726X', 'Aitana', 'Pascual Brotons', DATE '2006-07-10', 'aitanapascual29@alu.edugest.es', '686824567', 'Alicante', '1ASIR');
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (30, '10451110', '24667071P', 'Zoe', 'Iborra Valero', DATE '2006-06-22', NULL, '639706969', 'Sant Joan d''Alacant', NULL);
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (31, '10451147', '69382434J', 'Lucas', 'Agulló Cerdá', DATE '2006-04-18', 'lucasagullo31@alu.edugest.es', '627202308', 'Alicante', NULL);
INSERT INTO alumno (id_alumno, nia, dni, nombre, apellidos, fecha_nacimiento, email, telefono, localidad, cod_grupo) VALUES (32, '10451184', NULL, 'Irene', 'Belda Iborra', DATE '2006-07-28', 'irenebelda32@alu.edugest.es', '642961184', 'Mutxamel', NULL);

-- Matrículas
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10001, 1, 1, '2025-26', DATE '2025-09-03', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10002, 1, 2, '2025-26', DATE '2025-09-12', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10003, 1, 3, '2025-26', DATE '2025-09-01', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10004, 1, 4, '2025-26', DATE '2025-09-05', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10005, 1, 5, '2025-26', DATE '2025-09-12', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10006, 2, 1, '2025-26', DATE '2025-09-05', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10007, 2, 2, '2025-26', DATE '2025-09-05', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10008, 2, 3, '2025-26', DATE '2025-09-06', 1, 4.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10009, 2, 4, '2025-26', DATE '2025-09-12', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10010, 2, 5, '2025-26', DATE '2025-09-04', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10011, 3, 1, '2025-26', DATE '2025-09-12', 1, 3.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10012, 3, 2, '2025-26', DATE '2025-09-09', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10013, 3, 3, '2025-26', DATE '2025-09-08', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10014, 3, 4, '2025-26', DATE '2025-09-09', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10015, 3, 5, '2025-26', DATE '2025-09-03', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10016, 4, 1, '2025-26', DATE '2025-09-04', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10017, 4, 2, '2025-26', DATE '2025-09-03', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10018, 4, 3, '2025-26', DATE '2025-09-10', 1, 3.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10019, 4, 4, '2025-26', DATE '2025-09-04', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10020, 4, 5, '2025-26', DATE '2025-09-05', 1, 9.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10021, 5, 1, '2025-26', DATE '2025-09-06', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10022, 5, 2, '2025-26', DATE '2025-09-10', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10023, 5, 3, '2025-26', DATE '2025-09-01', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10024, 5, 4, '2025-26', DATE '2025-09-02', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10025, 5, 5, '2025-26', DATE '2025-09-02', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10026, 6, 1, '2025-26', DATE '2025-09-10', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10027, 6, 2, '2025-26', DATE '2025-09-06', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10028, 6, 3, '2025-26', DATE '2025-09-02', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10029, 6, 4, '2025-26', DATE '2025-09-06', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10030, 6, 5, '2025-26', DATE '2025-09-05', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10031, 7, 1, '2025-26', DATE '2025-09-02', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10032, 7, 2, '2025-26', DATE '2025-09-10', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10033, 7, 3, '2025-26', DATE '2025-09-07', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10034, 7, 4, '2025-26', DATE '2025-09-12', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10035, 7, 5, '2025-26', DATE '2025-09-08', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10036, 8, 6, '2025-26', DATE '2025-09-01', 1, 7.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10037, 8, 7, '2025-26', DATE '2025-09-03', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10038, 8, 8, '2025-26', DATE '2025-09-01', 1, 4);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10039, 8, 9, '2025-26', DATE '2025-09-04', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10040, 8, 10, '2025-26', DATE '2025-09-02', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10041, 9, 6, '2025-26', DATE '2025-09-03', 1, 9);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10042, 9, 7, '2025-26', DATE '2025-09-05', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10043, 9, 8, '2025-26', DATE '2025-09-07', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10044, 9, 9, '2025-26', DATE '2025-09-04', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10045, 9, 10, '2025-26', DATE '2025-09-07', 1, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10046, 10, 6, '2025-26', DATE '2025-09-02', 1, 9);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10047, 10, 7, '2025-26', DATE '2025-09-08', 1, 2.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10048, 10, 8, '2025-26', DATE '2025-09-06', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10049, 10, 9, '2025-26', DATE '2025-09-12', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10050, 10, 10, '2025-26', DATE '2025-09-02', 1, 3.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10051, 10, 1, '2025-26', DATE '2025-09-15', 2, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10052, 11, 6, '2025-26', DATE '2025-09-07', 1, 4.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10053, 11, 7, '2025-26', DATE '2025-09-11', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10054, 11, 8, '2025-26', DATE '2025-09-08', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10055, 11, 9, '2025-26', DATE '2025-09-04', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10056, 11, 10, '2025-26', DATE '2025-09-08', 1, 3.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10057, 11, 5, '2025-26', DATE '2025-09-15', 2, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10058, 12, 6, '2025-26', DATE '2025-09-05', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10059, 12, 7, '2025-26', DATE '2025-09-03', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10060, 12, 8, '2025-26', DATE '2025-09-02', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10061, 12, 9, '2025-26', DATE '2025-09-12', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10062, 12, 10, '2025-26', DATE '2025-09-06', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10063, 12, 3, '2025-26', DATE '2025-09-15', 2, 2.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10064, 13, 6, '2025-26', DATE '2025-09-10', 1, 2.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10065, 13, 7, '2025-26', DATE '2025-09-08', 1, 2.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10066, 13, 8, '2025-26', DATE '2025-09-08', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10067, 13, 9, '2025-26', DATE '2025-09-02', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10068, 13, 10, '2025-26', DATE '2025-09-12', 1, 7.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10069, 14, 11, '2025-26', DATE '2025-09-03', 1, 3.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10070, 14, 12, '2025-26', DATE '2025-09-05', 1, 5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10071, 14, 13, '2025-26', DATE '2025-09-07', 1, 4.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10072, 14, 14, '2025-26', DATE '2025-09-12', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10073, 14, 15, '2025-26', DATE '2025-09-08', 1, 4);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10074, 15, 11, '2025-26', DATE '2025-09-10', 1, 3);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10075, 15, 12, '2025-26', DATE '2025-09-10', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10076, 15, 13, '2025-26', DATE '2025-09-08', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10077, 15, 14, '2025-26', DATE '2025-09-09', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10078, 15, 15, '2025-26', DATE '2025-09-09', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10079, 16, 11, '2025-26', DATE '2025-09-12', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10080, 16, 12, '2025-26', DATE '2025-09-07', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10081, 16, 13, '2025-26', DATE '2025-09-03', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10082, 16, 14, '2025-26', DATE '2025-09-10', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10083, 16, 15, '2025-26', DATE '2025-09-12', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10084, 17, 11, '2025-26', DATE '2025-09-04', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10085, 17, 12, '2025-26', DATE '2025-09-07', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10086, 17, 13, '2025-26', DATE '2025-09-12', 1, 4);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10087, 17, 14, '2025-26', DATE '2025-09-05', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10088, 17, 15, '2025-26', DATE '2025-09-02', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10089, 18, 11, '2025-26', DATE '2025-09-04', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10090, 18, 12, '2025-26', DATE '2025-09-08', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10091, 18, 13, '2025-26', DATE '2025-09-09', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10092, 18, 14, '2025-26', DATE '2025-09-12', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10093, 18, 15, '2025-26', DATE '2025-09-09', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10094, 19, 11, '2025-26', DATE '2025-09-12', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10095, 19, 12, '2025-26', DATE '2025-09-08', 1, 5.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10096, 19, 13, '2025-26', DATE '2025-09-05', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10097, 19, 14, '2025-26', DATE '2025-09-12', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10098, 19, 15, '2025-26', DATE '2025-09-11', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10099, 20, 16, '2025-26', DATE '2025-09-05', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10100, 20, 17, '2025-26', DATE '2025-09-10', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10101, 20, 18, '2025-26', DATE '2025-09-11', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10102, 20, 19, '2025-26', DATE '2025-09-10', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10103, 21, 16, '2025-26', DATE '2025-09-08', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10104, 21, 17, '2025-26', DATE '2025-09-08', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10105, 21, 18, '2025-26', DATE '2025-09-02', 1, 1.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10106, 21, 19, '2025-26', DATE '2025-09-10', 1, 4.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10107, 22, 16, '2025-26', DATE '2025-09-03', 1, 5.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10108, 22, 17, '2025-26', DATE '2025-09-09', 1, 5.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10109, 22, 18, '2025-26', DATE '2025-09-11', 1, 4.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10110, 22, 19, '2025-26', DATE '2025-09-01', 1, 7);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10111, 23, 16, '2025-26', DATE '2025-09-11', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10112, 23, 17, '2025-26', DATE '2025-09-04', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10113, 23, 18, '2025-26', DATE '2025-09-06', 1, 3);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10114, 23, 19, '2025-26', DATE '2025-09-05', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10115, 24, 16, '2025-26', DATE '2025-09-04', 1, 5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10116, 24, 17, '2025-26', DATE '2025-09-11', 1, 5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10117, 24, 18, '2025-26', DATE '2025-09-04', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10118, 24, 19, '2025-26', DATE '2025-09-09', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10119, 25, 20, '2025-26', DATE '2025-09-07', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10120, 25, 21, '2025-26', DATE '2025-09-05', 1, 8.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10121, 25, 22, '2025-26', DATE '2025-09-02', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10122, 25, 23, '2025-26', DATE '2025-09-11', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10123, 25, 24, '2025-26', DATE '2025-09-03', 1, 3);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10124, 26, 20, '2025-26', DATE '2025-09-11', 1, 8.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10125, 26, 21, '2025-26', DATE '2025-09-08', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10126, 26, 22, '2025-26', DATE '2025-09-08', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10127, 26, 23, '2025-26', DATE '2025-09-04', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10128, 26, 24, '2025-26', DATE '2025-09-07', 1, 8.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10129, 27, 20, '2025-26', DATE '2025-09-10', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10130, 27, 21, '2025-26', DATE '2025-09-06', 1, 6.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10131, 27, 22, '2025-26', DATE '2025-09-02', 1, 4.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10132, 27, 23, '2025-26', DATE '2025-09-08', 1, 9.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10133, 27, 24, '2025-26', DATE '2025-09-06', 1, 6.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10134, 28, 20, '2025-26', DATE '2025-09-12', 1, 6);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10135, 28, 21, '2025-26', DATE '2025-09-01', 1, NULL);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10136, 28, 22, '2025-26', DATE '2025-09-06', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10137, 28, 23, '2025-26', DATE '2025-09-04', 1, 1.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10138, 28, 24, '2025-26', DATE '2025-09-07', 1, 6.75);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10139, 29, 20, '2025-26', DATE '2025-09-02', 1, 7.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10140, 29, 21, '2025-26', DATE '2025-09-09', 1, 9.25);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10141, 29, 22, '2025-26', DATE '2025-09-02', 1, 7.5);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10142, 29, 23, '2025-26', DATE '2025-09-08', 1, 8);
INSERT INTO matricula (id_matricula, id_alumno, id_modulo, curso_academico, fecha_matricula, convocatoria, nota_final) VALUES (10143, 29, 24, '2025-26', DATE '2025-09-04', 1, 10);

-- Asignación docente
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (1, '1DAM', '2025-26', 102, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (2, '1DAM', '2025-26', 101, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (3, '1DAM', '2025-26', 103, 8);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (4, '1DAM', '2025-26', 104, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (5, '1DAM', '2025-26', 107, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (6, '2DAM', '2025-26', 103, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (7, '2DAM', '2025-26', 104, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (8, '2DAM', '2025-26', 106, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (9, '2DAM', '2025-26', 103, 2);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (10, '2DAM', '2025-26', 102, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (11, '1DAW', '2025-26', 102, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (12, '1DAW', '2025-26', 101, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (13, '1DAW', '2025-26', 106, 8);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (14, '1DAW', '2025-26', 104, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (15, '1DAW', '2025-26', 107, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (16, '2DAW', '2025-26', 106, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (17, '2DAW', '2025-26', 104, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (18, '2DAW', '2025-26', 105, 2);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (19, '2DAW', '2025-26', 107, 4);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (20, '1ASIR', '2025-26', 105, 7);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (21, '1ASIR', '2025-26', 105, 6);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (22, '1ASIR', '2025-26', 102, 3);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (23, '1ASIR', '2025-26', 101, 5);
INSERT INTO imparte (id_modulo, cod_grupo, curso_academico, id_profesor, horas_semanales) VALUES (24, '1ASIR', '2025-26', 107, 3);

-- Faltas de asistencia
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (1, 10060, DATE '2025-10-31', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (2, 10045, DATE '2026-02-25', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (3, 10053, DATE '2026-01-21', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (4, 10109, DATE '2026-02-19', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (5, 10129, DATE '2026-03-03', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (6, 10003, DATE '2026-02-04', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (7, 10092, DATE '2026-03-25', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (8, 10121, DATE '2026-01-01', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (9, 10114, DATE '2026-01-06', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (10, 10103, DATE '2025-10-14', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (11, 10139, DATE '2026-04-02', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (12, 10044, DATE '2026-04-29', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (13, 10119, DATE '2026-02-25', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (14, 10084, DATE '2026-02-11', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (15, 10057, DATE '2026-03-18', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (16, 10004, DATE '2026-05-08', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (17, 10136, DATE '2025-10-10', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (18, 10109, DATE '2026-03-12', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (19, 10003, DATE '2026-03-19', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (20, 10127, DATE '2025-11-20', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (21, 10033, DATE '2025-09-25', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (22, 10040, DATE '2025-10-21', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (23, 10102, DATE '2025-10-31', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (24, 10073, DATE '2026-05-04', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (25, 10072, DATE '2026-01-14', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (26, 10029, DATE '2025-12-03', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (27, 10102, DATE '2026-04-17', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (28, 10101, DATE '2026-03-26', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (29, 10108, DATE '2025-09-23', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (30, 10034, DATE '2025-09-22', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (31, 10143, DATE '2025-10-29', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (32, 10051, DATE '2025-11-25', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (33, 10044, DATE '2026-03-11', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (34, 10033, DATE '2026-02-13', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (35, 10065, DATE '2025-12-08', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (36, 10129, DATE '2025-09-29', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (37, 10068, DATE '2026-02-26', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (38, 10051, DATE '2026-02-27', 2, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (39, 10099, DATE '2025-09-18', 1, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (40, 10087, DATE '2026-04-08', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (41, 10028, DATE '2026-03-10', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (42, 10070, DATE '2025-11-28', 2, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (43, 10048, DATE '2025-11-21', 3, 'S');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (44, 10015, DATE '2025-10-09', 1, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (45, 10133, DATE '2026-01-21', 3, 'N');
INSERT INTO falta_asistencia (id_falta, id_matricula, fecha, horas, justificada) VALUES (46, 10080, DATE '2026-03-05', 1, 'N');

COMMIT;

-- Comprobación rápida: número de filas por tabla
SELECT 'departamento' AS tabla, COUNT(*) AS filas FROM departamento UNION ALL
SELECT 'profesor', COUNT(*) FROM profesor UNION ALL
SELECT 'ciclo', COUNT(*) FROM ciclo UNION ALL
SELECT 'modulo', COUNT(*) FROM modulo UNION ALL
SELECT 'grupo', COUNT(*) FROM grupo UNION ALL
SELECT 'alumno', COUNT(*) FROM alumno UNION ALL
SELECT 'matricula', COUNT(*) FROM matricula UNION ALL
SELECT 'imparte', COUNT(*) FROM imparte UNION ALL
SELECT 'falta_asistencia', COUNT(*) FROM falta_asistencia;
