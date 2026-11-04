---
title: "Jocs UD05"
weight: 3
bookToc: true
aliases:
  - /ud05-ddl-dcl/ud05-escape-room/
---

# Jocs · UD05

{{< ra "RA2:a,b,c,d,e,g,h" "RA3:h" >}}

## Escape room · Backstage: que comence el festival

Un escape room d'**escenes clicables** per a tancar la [UD05](/ud05-ddl-dcl/). Muntes la base de dades del Brisa Fest en Oracle i, quan el recinte es bloqueja, només pots eixir demostrant que domines el DDL i el DCL.

| Sala | Cadenat | Què repasses |
|---|---|---|
| 📦 Magatzem de producció | 4 dígits | Tipus d'Oracle, `NUMBER(p,s)`, ordre de creació de les taules, errors de sintaxi en `CREATE TABLE` |
| 🎤 Escenari principal | 5 lletres | `PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `CHECK` amb nuls, `ON DELETE`, `ALTER TABLE`, `TRUNCATE` enfront de `DELETE` i `DROP` |
| 🎟️ Taquilla | 4 dígits + control de seguretat | Privilegis de sistema i d'objecte, rols, vistes, mínim privilegi, `WITH GRANT OPTION`, seqüències i índexs |

> [!TIP]
> Fes clic en l'escena o usa la **llista d'objectes** de davall. Els reptes inclouen **diagrames** (taules i claus alienes, precisió de `NUMBER`, cadena de privilegis): mira'ls abans de respondre.

> [!WARNING]
> Les pistes sumen un minut al cronòmetre i cada error, uns segons. La sintaxi és la d'**Oracle**: algunes opcions són vàlides en altres gestors, però no ací.

{{< escape-click data="escape_ud05" >}}

### Instruccions

- **Durada:** 30-40 minuts per parelles. Tres estreles si eixiu en menys de 40 minuts, comptant penalitzacions.
- **Com jugar:** exploreu cada sala, resoleu els reptes dels objectes i combineu el que guardeu en la motxilla per a obrir el cadenat de la porta. Si un objecte està tancat (🔒), un altre de la mateixa sala té el que falta.
- **En acabar:** la pantalla final mostra el temps, les estreles i els reptes que més us han costat, amb l'enllaç a l'apartat de la teoria que cal repassar.
- **Progrés:** es guarda en el navegador; *Tornar a començar* l'esborra.
