---
title: "Escape room UD02 + UD03"
weight: 3
bookToc: false
---

# Escape room · El caso del esquema desaparecido

{{< ra "RA6:a,b,c,d,e,h" "RA2:e" >}}

Un juego para **repasar antes del examen** (o para jugar en clase por parejas) con todo lo que has visto en la [UD02](/ud02-modelo-er/) y en la [UD03](/ud03-modelo-relacional/). Eres el inspector Codd, estás encerrado en el edificio de una aerolínea y solo saldrás si abres **diez cerraduras**, reúnes las pistas de tu libreta y descubres quién borró el modelo de datos.

| Acto | Cerraduras | Qué practicas |
|---|---|---|
| I · La planta de diseño (UD02) | 5 | Cardinalidades de una ternaria, entidades débiles, jerarquías parciales y solapadas, tipos de atributos, relaciones reflexivas con roles |
| II · La cámara acorazada (UD03) | 5 | Políticas de borrado, clave primaria de una N:M, orden de creación de tablas, recuento de tablas, restricciones que el esquema no expresa |
| III · La puerta de salida | 1 + acusación | De la ternaria a la tabla y deducción del culpable con las pistas |

> [!TIP]
> Cada sala te deja una **pista** en la libreta y, al resolverla, te explica **por qué** es correcta y a qué apartado de la teoría debes volver. Aunque aciertes a la primera, léela: es donde está lo que se pregunta en el examen.

> [!NOTE]
> Una pista cuesta 20 puntos y cada fallo, 10. No es un examen: úsalas cuando las necesites, pero intenta antes razonar con el esquema delante. Si juegas en clase, comparad las puntuaciones **después** de comentar las respuestas, no antes.

{{< escape-room >}}

## Para el profesorado

- **Duración:** 30-45 minutos por parejas. Funciona bien como cierre de la UD03.
- **Pistas clave:** tres de las pistas descartan a dos de los tres sospechosos. Pide al alumnado que justifique la acusación **con las pistas**, no por intuición.
- **Progreso:** se guarda en el navegador de cada alumno; el botón *Empezar de nuevo* lo borra.
- **Contenido:** los textos están en `data/escape_ud02_ud03.json` (castellano y valenciano). Para añadir una sala basta con añadir un elemento a `puzzles`, con uno de los cinco tipos (`choice`, `multi`, `match`, `order`, `number`).
