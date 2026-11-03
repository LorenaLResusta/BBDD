---
title: "Escape room UD06"
weight: 5
bookToc: false
---

# Escape room · Spoiler: ¿quién filtró el final?

{{< ra "RA3:a,b,c,d,e,f" "RA5:e" >}}

Un escape room de **escenas clicables** para cerrar la [UD06](/ud06-consultas/). Alguien ha filtrado el último capítulo de una serie y tú tienes los datos: cada consulta bien leída abre una puerta y te acerca al culpable.

| Sala | Candado | Qué repasas |
|---|---|---|
| 🎥 Sala de visionado | 3 dígitos + tarjeta | Precedencia de `AND` y `OR`, `LIKE`, `NULL` en `WHERE`, `ORDER BY` y `FETCH FIRST` |
| 📊 Sala de datos | 4 dígitos | `COUNT(*)` frente a `COUNT(columna)`, `GROUP BY` y `HAVING` a partir de un **gráfico**, `AVG` con nulos, ORA-00979 |
| 🕵️ Despacho de dirección | Nombre del culpable | `JOIN`, `LEFT JOIN` con `COUNT`, la trampa de `NOT IN` con nulos, subconsultas de una fila |

> [!TIP]
> Los datos están en notas de la propia sala (la pantalla, el monitor, el expediente): **ábrelas primero**. Todas las consultas se resuelven a mano con esas filas.

> [!WARNING]
> Las pistas suman un minuto al cronómetro y cada fallo, unos segundos. Ojo con los `NULL`: aparecen a propósito en las tres salas.

{{< escape-click data="escape_ud06" >}}

## Instrucciones

- **Duración:** 35-45 minutos por parejas. Tres estrellas si salís en menos de 45 minutos, contando penalizaciones.
- **Cómo jugar:** abrid primero las notas con los datos, calculad a mano lo que devuelve cada consulta y combinad los resultados de la mochila en el candado. En la última sala, el candado pide el **nombre** del culpable.
- **Para comprobarlo en Oracle:** los datos son pequeños; podéis crear las tablas y ejecutar las consultas para ver que el resultado coincide.
- **Al terminar:** la pantalla final muestra el tiempo, las estrellas y los retos que más os han costado, con el enlace a la teoría.
