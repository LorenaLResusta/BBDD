---
title: "Escape room UD08"
weight: 3
bookToc: false
---

# Escape room · Apagón en la estación Kepler

{{< ra "RA5:a,b,c,d,e,f,g,h,i" >}}

Un escape room de **escenas clicables** para cerrar la [UD08](/ud08-plsql/). Las compuertas de una estación espacial las controlan bloques PL/SQL: para llegar a la nave de rescate tienes que **leer y ejecutar el código mentalmente**.

| Sala | Candado | Qué repasas |
|---|---|---|
| 🛰️ Puente de mando | 3 dígitos + calefacción | Partes de un bloque, `FOR` y `WHILE` (con **diagrama de flujo**), `IF` con variables nulas |
| 🧪 Laboratorio | 4 dígitos + cursores | Cursor `FOR`, `SQL%ROWCOUNT`, `SELECT … INTO` y `TOO_MANY_ROWS`, pasos de un cursor explícito |
| 🚀 Esclusa | 3 dígitos + revisión | Funciones en un `SELECT`, parámetros `IN`/`OUT`/`IN OUT`, disparadores de sentencia y de fila, `:NEW` y `:OLD`, qué herramienta usar |

> [!TIP]
> Para cada bloque, **apunta en un papel** el valor de las variables vuelta a vuelta. Los diagramas (flujo del bucle, paso de parámetros, orden de disparo) te ayudan a seguir el código.

> [!WARNING]
> Las pistas suman un minuto al cronómetro y cada fallo, unos segundos. En el laboratorio, cada reto parte de los datos originales de la tabla, sin los cambios de los demás.

{{< escape-click data="escape_ud08" >}}

## Instrucciones

- **Duración:** 35-45 minutos por parejas. Tres estrellas si salís en menos de 45 minutos, contando penalizaciones.
- **Cómo jugar:** resolved los retos de cada sala, guardad los resultados en la mochila y combinadlos en el candado. Algunas puertas exigen además haber resuelto ciertos objetos (🔒).
- **Para comprobarlo en Oracle:** todos los bloques son ejecutables con `SET SERVEROUTPUT ON` si creáis las tablas TRIPULANTE y SENSOR con los datos de las notas.
- **Al terminar:** la pantalla final muestra el tiempo, las estrellas y los retos que más os han costado, con el enlace a la teoría.
- **Contenido:** `data/escape_ud08.yaml`, escenas en `assets/escape/ud08-*.svg` y diagramas en `assets/escape/fig/ud08-*.svg`.
