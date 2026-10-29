---
title: "Escape room UD02 + UD03"
weight: 3
bookToc: false
---

# Escape room · El cas de l'esquema desaparegut

{{< ra "RA6:a,b,c,d,e,h" "RA2:e" >}}

Un joc per a **repassar abans de l'examen** (o per a jugar a classe per parelles) amb tot el que has vist a la [UD02](/ud02-modelo-er/) i a la [UD03](/ud03-modelo-relacional/). Eres l'inspector Codd, estàs tancat a l'edifici d'una aerolínia i només eixiràs si obris **deu panys**, reuneixes les pistes de la teua llibreta i descobreixes qui va esborrar el model de dades.

| Acte | Panys | Què practiques |
|---|---|---|
| I · La planta de disseny (UD02) | 5 | Cardinalitats d'una ternària, entitats febles, jerarquies parcials i solapades, tipus d'atributs, relacions reflexives amb rols |
| II · La cambra cuirassada (UD03) | 5 | Polítiques d'esborrat, clau primària d'una N:M, ordre de creació de taules, recompte de taules, restriccions que l'esquema no expressa |
| III · La porta d'eixida | 1 + acusació | De la ternària a la taula i deducció del culpable amb les pistes |

> [!TIP]
> Cada sala et deixa una **pista** a la llibreta i, en resoldre-la, t'explica **per què** és correcta i a quin apartat de la teoria has de tornar. Encara que encertes a la primera, llig-la: és on està el que es pregunta a l'examen.

> [!NOTE]
> Una pista costa 20 punts i cada error, 10. No és un examen: usa-les quan les necessites, però intenta abans raonar amb l'esquema davant. Si jugues a classe, compareu les puntuacions **després** de comentar les respostes, no abans.

{{< escape-room >}}

## Per al professorat

- **Durada:** 30-45 minuts per parelles. Funciona bé com a tancament de la UD03.
- **Pistes clau:** tres de les pistes descarten dos dels tres sospitosos. Demana a l'alumnat que justifique l'acusació **amb les pistes**, no per intuïció.
- **Progrés:** es guarda al navegador de cada alumne; el botó *Començar de nou* l'esborra.
- **Contingut:** els textos estan a `data/escape_ud02_ud03.json` (castellà i valencià). Per a afegir una sala basta afegir un element a `puzzles`, amb un dels cinc tipus (`choice`, `multi`, `match`, `order`, `number`).
