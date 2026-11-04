---
title: "Jocs UD08"
weight: 3
bookToc: true
aliases:
  - /ud08-plsql/ud08-escape-room/
---

# Jocs · UD08

{{< ra "RA5:a,b,c,d,e,f,g,h,i" >}}

## Escape room · Apagada en l'estació Kepler

Un escape room d'**escenes clicables** per a tancar la [UD08](/ud08-plsql/). Les comportes d'una estació espacial les controlen blocs PL/SQL: per a arribar a la nau de rescat has de **llegir i executar el codi mentalment**.

| Sala | Cadenat | Què repasses |
|---|---|---|
| 🛰️ Pont de comandament | 3 dígits + calefacció | Parts d'un bloc, `FOR` i `WHILE` (amb **diagrama de flux**), `IF` amb variables nul·les |
| 🧪 Laboratori | 4 dígits + cursors | Cursor `FOR`, `SQL%ROWCOUNT`, `SELECT … INTO` i `TOO_MANY_ROWS`, passos d'un cursor explícit |
| 🚀 Resclosa | 3 dígits + revisió | Funcions en un `SELECT`, paràmetres `IN`/`OUT`/`IN OUT`, disparadors de sentència i de fila, `:NEW` i `:OLD`, quina eina usar |

> [!TIP]
> Per a cada bloc, **anota en un paper** el valor de les variables volta a volta. Els diagrames (flux del bucle, pas de paràmetres, ordre de disparament) t'ajuden a seguir el codi.

> [!WARNING]
> Les pistes sumen un minut al cronòmetre i cada error, uns segons. En el laboratori, cada repte partix de les dades originals de la taula, sense els canvis dels altres.

{{< escape-click data="escape_ud08" >}}

### Instruccions

- **Durada:** 35-45 minuts per parelles. Tres estreles si eixiu en menys de 45 minuts, comptant penalitzacions.
- **Com jugar:** resoleu els reptes de cada sala, guardeu els resultats en la motxilla i combineu-los en el cadenat. Algunes portes exigixen a més haver resolt certs objectes (🔒).
- **Per a comprovar-ho en Oracle:** tots els blocs són executables amb `SET SERVEROUTPUT ON` si creeu les taules TRIPULANTE i SENSOR amb les dades de les notes.
- **En acabar:** la pantalla final mostra el temps, les estreles i els reptes que més us han costat, amb l'enllaç a la teoria.
