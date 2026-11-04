---
title: "Jocs UD03"
weight: 3
bookToc: true
aliases:
  - /ud03-modelo-relacional/ud03-escape-room/
---

# Jocs · UD03 Model relacional

{{< ra "RA6:b,c,d,e,f,h" "RA2:a,d,e" >}}

Cinc jocs per a dominar el model relacional i la transformació des de l'E/R, de menys a més difícils. El **memory** i el **duel** es poden jugar **per equips**.

| Joc | Format | Durada |
|---|---|---|
| 🏦 Escape room | Quatre sales; l'última, amb superclaus, cadenes de febles i esborrats combinats | 40-50 min |
| 🔤 Rosco | Passaparaula de claus, integritat i transformació, a contrarellotge | 2,5 min |
| 🔍 Caça d'errors | Cinc errors en un esquema transformat | 5-10 min |
| 🃏 Memory | 18 parelles diagrama ↔ esquema que només canvien en les cardinalitats | 15-20 min |
| ⚔️ Duel per equips | Dotze rondes per a transformar un cas EER complet en 13 taules | 40-50 min |

## 1. Escape room · Bloqueig en el Banc Codd

El sistema de seguretat del Banc Codd t'ha deixat tancat al soterrani i només obri les portes a qui demostra que entén la seua base de dades relacional.

| Sala | Cadenat | Què repasses |
|---|---|---|
| 📚 Arxiu | 4 dígits | Grau i cardinalitat, claus candidates, valors nuls, restriccions inherents |
| 🖥️ Sala de servidors | 3 dígits + corrent | Integritat referencial, VNN, polítiques d'esborrat, esborrat en cascada, FK compostes |
| 🏦 Cambra cuirassada | 3 dígits + clau | Transformació de N:M, 1:N i 1:1, nombre de taules, pèrdues semàntiques |
| 🗄️ Despatx del director | 3 dígits, sense adhesius | Superclaus, cadena d'entitats febles, esborrat amb cascada i posada a nuls, jerarquies parcials |

> [!TIP]
> En la sala de servidors, **llig primer la pissarra**. En el despatx del director no hi ha adhesius: l'ordre està en la història de la sala.

{{< escape-click data="escape_ud03" >}}

## 2. Rosco del model relacional

> [!TIP]
> **Per equips:** projecteu-lo i que cada equip conteste una lletra per torn; qui diu *passaparaula* cedix el torn.

{{< rosco data="rosco_ud03" >}}

## 3. Caça d'errors en un esquema

> [!TIP]
> Abans de buscar errors, **transforma tu el diagrama** amb les regles de la unitat i compara el teu esquema amb el del becari.

{{< caza data="caza_ud03" >}}

## 4. Memory de parelles

> [!WARNING]
> Moltes cartes usen les mateixes entitats (EMPLEAT, DEPARTAMENT, ALUMNE, EXAMEN, AULA…) i només canvien les cardinalitats o una restricció: VNN, UK, nuls… Llig-les senceres.

{{< memory data="memory_ud03" >}}

## 5. Duel per equips

> [!TIP]
> És el mateix cas del duel de la UD02, ja resolt. Les rondes obertes es contesten escrivint l'esquema en la pissarra.

{{< duelo data="duelo_ud03" >}}

## Instruccions

- **Ordre recomanat:** rosco i caça en acabar la teoria; escape room i memory en la sessió de repàs; duel com a activitat final de la unitat.
- **Dificultat:** el rosco va a contrarellotge (140 s), el memory obliga a fixar-se en cada cardinalitat i el duel exigix transformar un cas amb jerarquia solapada, ternària, feble, agregació i dos FK cap a la mateixa taula.
- **En acabar** cada joc apareix el repàs del que ha costat més, amb enllaços a la teoria.
- **Progrés:** l'escape room i la millor marca del rosco es guarden en el navegador.
- **Més:** l'[escape room final del trimestre](/escape-rooms/trimestre-1) mescla la UD02 i la UD03.
