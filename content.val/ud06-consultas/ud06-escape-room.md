---
title: "Escape room UD06"
weight: 5
bookToc: false
---

# Escape room · Spoiler: qui va filtrar el final?

{{< ra "RA3:a,b,c,d,e,f" "RA5:e" >}}

Un escape room d'**escenes clicables** per a tancar la [UD06](/ud06-consultas/). Algú ha filtrat l'últim capítol d'una sèrie i tu tens les dades: cada consulta ben llegida obri una porta i t'acosta al culpable.

| Sala | Cadenat | Què repasses |
|---|---|---|
| 🎥 Sala de visionat | 3 dígits + targeta | Precedència d'`AND` i `OR`, `LIKE`, `NULL` en `WHERE`, `ORDER BY` i `FETCH FIRST` |
| 📊 Sala de dades | 4 dígits | `COUNT(*)` enfront de `COUNT(columna)`, `GROUP BY` i `HAVING` a partir d'un **gràfic**, `AVG` amb nuls, ORA-00979 |
| 🕵️ Despatx de direcció | Nom del culpable | `JOIN`, `LEFT JOIN` amb `COUNT`, la trampa de `NOT IN` amb nuls, subconsultes d'una fila |

> [!TIP]
> Les dades estan en notes de la mateixa sala (la pantalla, el monitor, l'expedient): **obri-les primer**. Totes les consultes es resolen a mà amb eixes files.

> [!WARNING]
> Les pistes sumen un minut al cronòmetre i cada error, uns segons. Compte amb els `NULL`: apareixen a propòsit en les tres sales.

{{< escape-click data="escape_ud06" >}}

## Instruccions

- **Durada:** 35-45 minuts per parelles. Tres estreles si eixiu en menys de 45 minuts, comptant penalitzacions.
- **Com jugar:** obriu primer les notes amb les dades, calculeu a mà el que torna cada consulta i combineu els resultats de la motxilla en el cadenat. En l'última sala, el cadenat demana el **nom** del culpable.
- **Per a comprovar-ho en Oracle:** les dades són menudes; podeu crear les taules i executar les consultes per a veure que el resultat coincidix.
- **En acabar:** la pantalla final mostra el temps, les estreles i els reptes que més us han costat, amb l'enllaç a la teoria.
- **Contingut:** `data/escape_ud06.yaml`, escenes en `assets/escape/ud06-*.svg` i diagrames (gràfic de barres, `LEFT JOIN`, línia de temps) en `assets/escape/fig/ud06-*.svg`.
