## 4. Regles de transformació del model EER al model relacional

Per a transformar de manera metòdica un diagrama EER conceptual en un esquema relacional lògic, s'apliquen les regles d'este apartat. Cada regla va acompanyada d'**un exemple complet**, amb la mateixa estructura que veuràs en tots:

1. el **diagrama de Chen** de partida;
2. l'**esquema relacional** resultant, escrit amb la notació de les pràctiques (PK, FK, UK, VNN);
3. el **patró general** amb entitats abstractes `A`, `B`, `C` i atributs `a0`, `a1`, `b0`… (`a0` és sempre l'identificador d'`A`);
4. unes **files d'exemple** per a comprovar que les restriccions fan el que han de fer.

> [!NOTE]
> **Notació de l'esquema.** Cada taula s'escriu amb les seues columnes i, davall, les seues restriccions:
> **PK** = clau primària · **FK** = clau aliena (`columna → TAULA`) · **UK** = clau alternativa (*unique*) · **VNN** = valor no nul (obligatori).
> És la mateixa notació de les [tasques de transformació](/ud03-modelo-relacional/ud03-practicas#ANCLA_TASQUES).

---

### 4.1 Transformació d'entitats fortes

- **Regla:** Cada entitat forta del diagrama EER es convertix en una **taula (relació)** independent.
  - Els atributs simples de l'entitat passen a ser **columnes** de la taula.
  - L'atribut identificador principal de l'entitat passa a ser la **Clau Primària (PK)** de la taula.
  - Els identificadors candidats (claus alternatives) passen a ser **UK**. Com que identifiquen, a més porten **VNN**.

#### Exemple 4.1 · L'entitat ALUMNO

En el centre, cada alumne té un NIA (número d'identificació de l'alumnat) que assigna la Conselleria. També té DNI, que no es repetix, però es tria el NIA com a identificador principal.

{{< figura src="ud03/teo-41-alumno.svg" alt="Entitat ALUMNO amb els atributs nia (identificador, subratllat), dni (clau alternativa, subratllat de punts), nombre i fecha_nac" caption="Entitat forta amb identificador (nia) i clau alternativa (dni)" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
ALUMNO (nia, dni, nombre, fecha_nac)
   PK:  nia
   UK:  dni
   VNN: dni
```
- `nia` és la **PK**: no es repetix i no pot ser nul·la.
- `dni` és **UK** perquè també identifica, i **VNN** perquè una clau candidata sense valor no identificaria ningú.
- `nombre` i `fecha_nac` són columnes normals. Si l'enunciat diguera que són obligatòries, portarien també VNN.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0 identificador, a1, a2, a3 clau alternativa)

A (a0, a1, a2, a3)
   PK:  a0
   UK:  a3
   VNN: a3
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| nia (PK) | dni (UK) | nombre | fecha_nac |
|---|---|---|---|
| 10234567 | 48123456P | Paula Ortiz | 2006-03-14 |
| 10234568 | 21456789K | Izan Pastor | 2005-11-02 |
| 10234569 | 74222333B | Lucía Sempere | 2006-07-29 |

Una quarta fila amb el DNI `48123456P` seria rebutjada per la **UK**, encara que el seu NIA fora diferent.
{{% /tab %}}
{{< /tabs >}}

---

### 4.2 Transformació d'entitats febles (per identificació i existència)

- **Regla:** Una entitat feble es convertix en una **taula independent**.
  - **Feble per identificació (ID):** La clau primària de la taula resultant és una **clau composta** formada per la clau primària de l'entitat forta propietària (que es propaga com a `FK`) combinada amb el discriminador parcial de l'entitat feble.
  - **Feble per existència (E):** Si l'entitat feble té el seu propi identificador únic, este és la seua PK. La clau primària de l'entitat forta es propaga com a **FK obligatòria (VNN)**. És el cas habitual d'una relació 1:N amb participació obligatòria, que es veu amb més detall en l'apartat 4.4.

#### Exemple 4.2-a · Feble per identificació: EDIFICIO i AULA

Les aules es numeren **dins de cada edifici**: l'edifici A té una aula 1 i l'edifici B també. El número d'aula, per si sol, no identifica: és un **discriminador** (subratllat discontinu).

{{< figura src="ud03/teo-42a-edificio-aula.svg" alt="EDIFICIO (cod_edificio, nombre) es relaciona mitjançant el rombe doble tiene amb l'entitat feble AULA (num_aula discriminador, capacidad); EDIFICIO (1,1), AULA (1,N)" caption="Entitat feble per identificació: rectangle doble i rombe doble" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
EDIFICIO (cod_edificio, nombre)
   PK:  cod_edificio

AULA (cod_edificio, num_aula, capacidad)
   PK:  (cod_edificio, num_aula)
   FK:  cod_edificio → EDIFICIO
```
- La relació `tiene` **no genera taula**: queda absorbida en `AULA`.
- `cod_edificio` és alhora **part de la PK** i **FK**. Com que forma part de la PK, ja és obligatòria: no cal escriure VNN.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (feble, discriminador a0) ──ID── B (b0)
            Restricció d'identitat

A (a0, a1, aB)
   PK:  (a0, aB)
   FK:  aB → B

B (b0, b1)
   PK:  b0
```
{{% /tab %}}
{{% tab "Amb dades" %}}
**EDIFICIO**

| cod_edificio (PK) | nombre |
|---|---|
| A | Edifici principal |
| B | Tallers |

**AULA**

| cod_edificio (PK, FK) | num_aula (PK) | capacidad |
|---|---|---|
| A | 1 | 30 |
| A | 2 | 24 |
| B | 1 | 20 |

El valor `1` de `num_aula` es repetix, però la parella `(A, 1)` no. Inserir `(C, 3)` fallaria: l'edifici `C` no existix (**FK**).
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.2-b · Feble per existència: CLIENTE i PEDIDO

Una comanda té el seu propi número, que no es repetix mai, però **no pot existir sense el client** que la fa (marca **E**).

{{< figura src="ud03/teo-42b-cliente-pedido.svg" alt="CLIENTE (cod_cliente, nombre) realiza PEDIDO (num_pedido, fecha); CLIENTE (1,1), PEDIDO (0,N), amb la marca E de dependència en existència al costat de PEDIDO" caption="Entitat feble per existència: té identificador propi" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
CLIENTE (cod_cliente, nombre)
   PK:  cod_cliente

PEDIDO (num_pedido, fecha, cod_cliente)
   PK:  num_pedido
   FK:  cod_cliente → CLIENTE
   VNN: cod_cliente
```
- La PK de `PEDIDO` és només `num_pedido`: no necessita el client per a identificar-se.
- La dependència en existència es traduïx en **VNN** sobre la FK: no hi ha comandes «òrfenes».
- En esborrar un client, la política habitual és **en cascada** (s'esborren les seues comandes) o **restringida** (no es deixa esborrar). Es decidix en la UD05.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──E── R ── B (b0, b1)     (A depén de B)

A (a0, a1, aB)
   PK:  a0
   FK:  aB → B
   VNN: aB
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| num_pedido (PK) | fecha | cod_cliente (FK, VNN) |
|---|---|---|
| 5001 | 2026-10-04 | C01 |
| 5002 | 2026-10-04 | C02 |
| 5003 | 2026-10-05 | C01 |

Inserir `(5004, 2026-10-06, NULL)` fallaria pel **VNN**.
{{% /tab %}}
{{< /tabs >}}

> [!TIP]
> **ID o E?** Pregunta't: *l'identificador de l'entitat feble es repetix entre propietaris diferents?* Si es repetix (aula 1 de l'edifici A, aula 1 de l'edifici B), és per **identificació** i la PK és composta. Si no es repetix (la comanda 5001 és única en tota l'empresa), és per **existència** i n'hi ha prou amb una FK obligatòria.

---

### 4.3 Transformació d'atributs compostos i multivalorats

Estes són les **regles preparatòries**: s'apliquen abans que les altres i es basen en la primera forma normal (UD04), que exigix que cada columna guarde **un únic valor atòmic**.

1. **Atributs compostos:** S'eliminen desplegant cadascun dels seus subatributs simples com a columnes individuals de la mateixa taula. L'atribut compost «pare» desapareix.
2. **Atributs multivalorats ($N$):** Es crea una **nova taula independent** per a l'atribut multivalorat. La clau primària d'esta nova taula serà la combinació de la clau primària de l'entitat originària i el mateix atribut multivalorat.

#### Exemple 4.3 · PERSONA amb adreça i diversos telèfons

{{< figura src="ud03/teo-43-persona.svg" alt="Entitat PERSONA amb dni (identificador), nombre, l'atribut compost direccion (calle, numero, ciudad) i l'atribut multivalorat telefono (oval doble)" caption="Atribut compost (direccion) i multivalorat (telefono, oval doble)" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
PERSONA (dni, nombre, calle, numero, ciudad)
   PK:  dni

TELEFONO (dni, telefono)
   PK:  (dni, telefono)
   FK:  dni → PERSONA
```
- `direccion` no apareix com a columna: se substituïx per `calle`, `numero` i `ciudad`.
- `telefono` ix de `PERSONA`. Si es deixara dins, caldria guardar «600111222, 965000000» en una sola cel·la, o crear columnes `telefono1`, `telefono2`… sense saber quantes en calen.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1, a2 multivalorat (n), a3)

A (a0, a1, a3)
   PK:  a0

A2 (a0, a2)
   PK:  (a0, a2)
   FK:  a0 → A
```
{{% /tab %}}
{{% tab "Amb dades" %}}
**PERSONA**

| dni (PK) | nombre | calle | numero | ciudad |
|---|---|---|---|---|
| 48123456P | Paula Ortiz | Lillo Juan | 128 | Sant Vicent del Raspeig |
| 21456789K | Izan Pastor | Alfonso X | 12 | Alacant |

**TELEFONO**

| dni (PK, FK) | telefono (PK) |
|---|---|
| 48123456P | 600111222 |
| 48123456P | 965000000 |
| 21456789K | 611222333 |

Paula té dos telèfons: dues files. Repetir `(48123456P, 600111222)` violaria la **PK**.
{{% /tab %}}
{{< /tabs >}}

> [!NOTE]
> **Excepció:** si el valor multivalorat no es pot repetir entre entitats diferents (per exemple, un correu corporatiu que només pertany a una persona), el mateix valor és suficient com a PK: `CORREO (email, dni)` amb PK: `email`, FK: `dni → PERSONA`, VNN: `dni`.

> [!WARNING]
> **Pèrdua semàntica.** Si el diagrama exigix un mínim d'1 («tota persona té almenys un telèfon»), les taules no ho poden garantir: es pot inserir una persona sense cap fila en `TELEFONO`. Cal anotar-ho (apartat 6).

#### Laboratori: de l'E/R a les taules

Este transformador aplica les regles de l'apartat 4 i produïx l'esquema relacional formal. Comença pels casos d'esta sessió (feble, multivalorat) i torna a ell en la següent.

{{< er-a-relacional >}}

---

{{< sesion n="5" h="2" tipo="t" >}}Regles de transformació (II): relacions i jerarquies{{< /sesion >}}

### 4.4 Transformació de relacions binàries 1:N

- **Regla (propagació de clau):** No es crea una taula nova. Es pren la clau primària de l'entitat del costat "1" i es **propaga com a clau forana (`FK`)** a la taula resultant de l'entitat del costat "N".
- Si la relació tenia atributs descriptors propis, estos es traslladen també com a columnes a la taula del costat "N".
- Si la participació del costat "N" és obligatòria (cardinalitat mínima 1), la FK ha de ser obligatòria (**VNN**).
- Si la clau del costat "1" és **composta**, la FK també és composta: viatgen **totes** les seues columnes juntes.

> [!TIP]
> **Truc per a no equivocar-se:** la clau viatja **cap al costat N**. Pensa en una fila del costat N: un empleat té **un** departament, així que cap en una columna. Un departament té **molts** empleats, que no caben en una columna.

#### Exemple 4.4-a · Participació opcional: EMPLEADO i DEPARTAMENTO (0,1)

Cada empleat treballa **com a molt** en un departament (pot haver-hi empleats acabats de contractar sense assignar). Un departament té molts empleats. La relació guarda la data d'alta.

{{< figura src="ud03/teo-44a-emp-dep-opcional.svg" alt="EMPLEADO (dni, nombre) trabaja DEPARTAMENTO (cod_dep, nombre); al costat de DEPARTAMENTO (0,1), al costat d'EMPLEADO (0,N); atribut fecha_alta en la relació" caption="Relació 1:N amb participació opcional de l'empleat" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
DEPARTAMENTO (cod_dep, nombre)
   PK:  cod_dep

EMPLEADO (dni, nombre, cod_dep, fecha_alta)
   PK:  dni
   FK:  cod_dep → DEPARTAMENTO
```
- `cod_dep` viatja a `EMPLEADO` (costat N) com a **FK**.
- `fecha_alta`, atribut de la relació, viatja amb ella.
- Sense VNN: el mínim al costat de DEPARTAMENTO és 0, així que `cod_dep` admet nuls.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──N── R ──1── B (b0, b1)

A (a0, a1, aB)
   PK:  a0
   FK:  aB → B

B (b0, b1)
   PK:  b0
```
{{% /tab %}}
{{% tab "Amb dades" %}}
**DEPARTAMENTO**

| cod_dep (PK) | nombre |
|---|---|
| INF | Informàtica |
| ADM | Administració |

**EMPLEADO**

| dni (PK) | nombre | cod_dep (FK) | fecha_alta |
|---|---|---|---|
| 11111111H | Marta Lloret | INF | 2020-09-01 |
| 22222222J | Andrés Gil | INF | 2023-09-01 |
| 33333333P | Sara Vidal | `NULL` | `NULL` |

Sara encara no té departament: la FK és nul·la i és vàlid.
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.4-b · Participació obligatòria: (1,1)

Si l'enunciat diu que **tot empleat pertany obligatòriament a un departament**, el mínim al costat de DEPARTAMENTO passa a ser 1.

{{< figura src="ud03/teo-44b-emp-dep-obligatoria.svg" alt="EMPLEADO trabaja DEPARTAMENTO; al costat de DEPARTAMENTO (1,1) amb línia doble, al costat d'EMPLEADO (1,N)" caption="Relació 1:N amb participació obligatòria de l'empleat" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
DEPARTAMENTO (cod_dep, nombre)
   PK:  cod_dep

EMPLEADO (dni, nombre, cod_dep, fecha_alta)
   PK:  dni
   FK:  cod_dep → DEPARTAMENTO
   VNN: cod_dep
```
L'única diferència amb 4.4-a és el **VNN**: ara la fila de Sara amb `cod_dep` nul seria rebutjada.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──E── R ── B (b0, b1)     (mínim 1 al costat de B)

A (a0, a1, aB)
   PK:  a0
   FK:  aB → B
   VNN: aB
```
{{% /tab %}}
{{< /tabs >}}

> [!WARNING]
> **Pèrdua semàntica.** Al costat d'EMPLEADO posa **(1,N)**: tot departament té **almenys un** empleat. Això **no es pot** garantir amb claus: res impedix inserir un departament sense empleats. És el cas de la figura del PDF en què la marca **E** està en el costat 1. S'anota com a restricció no representable i es controla en la implementació (UD08).

#### Exemple 4.4-c · Clau aliena composta: SESION i AULA

Ara el costat 1 és `AULA`, la clau de la qual és **composta** `(cod_edificio, num_aula)` (exemple 4.2-a). Cada sessió de classe s'impartix en una aula.

{{< figura src="ud03/teo-44c-sesion-aula.svg" alt="SESION (id_sesion, dia, hora) se_imparte AULA (cod_edificio i num_aula com a identificador compost, capacidad); al costat d'AULA (1,1), al costat de SESION (0,N)" caption="La clau del costat 1 és composta: la clau aliena també ho serà" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
SESION (id_sesion, dia, hora, cod_edificio, num_aula)
   PK:  id_sesion
   FK:  (cod_edificio, num_aula) → AULA
   VNN: cod_edificio, num_aula
```
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──N── R ──1── B (b0, b1)      amb PK de B = (b0, b1)

A (a0, a1, aB0, aB1)
   PK:  a0
   FK:  (aB0, aB1) → B
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| id_sesion (PK) | dia | hora | cod_edificio (FK) | num_aula (FK) |
|---|---|---|---|---|
| 1 | L | 08:00 | A | 1 |
| 2 | L | 09:00 | B | 1 |
| 3 | M | 08:00 | A | 2 |

`(B, 2)` no existix en `AULA` (vegeu 4.2-a): una sessió en eixa aula seria rebutjada.
{{% /tab %}}
{{< /tabs >}}

> [!CAUTION]
> **Error freqüent:** escriure dues FK separades, `cod_edificio → EDIFICIO` i `num_aula → AULA`. Amb dues FK separades s'acceptaria la parella `(B, 2)`, perquè l'edifici B existix i existix *alguna* aula 2. Una clau aliena apunta **sempre a la PK completa** de la taula referenciada: si la PK és simple, la FK és simple; si és composta, la FK és composta.

---

### 4.5 Transformació de relacions binàries N:M

- **Regla (taula intermèdia):** Es crea obligatòriament una **nova taula de relació**.
  - La clau primària d'esta nova taula és una **clau composta** formada per la unió de les claus primàries de les dues entitats participants (doble propagació de clau).
  - Cadascuna d'estes claus funciona per separat com a clau forana (`FK`) cap a la seua taula corresponent.
  - Els atributs propis de la relació $N:M$ s'incorporen com a columnes d'esta nova taula.

#### Exemple 4.5 · ALUMNO cursa MODULO

{{< figura src="ud03/teo-45-alumno-modulo.svg" alt="ALUMNO (nia, nombre) cursa MODULO (cod_modulo, nombre) amb l'atribut nota; al costat d'ALUMNO (0,N), al costat de MODULO (1,N)" caption="Relació N:M amb atribut propi (nota)" >}}

{{% paso-a-paso titulo="De N:M a taules: ALUMNO i MODULO" %}}
{{% etapa titulo="1. El diagrama" %}}
Un alumne cursa molts mòduls i un mòdul té molts alumnes: relació **N:M** amb l'atribut `nota`.
{{% /etapa %}}
{{% etapa titulo="2. Les entitats passen a taules" %}}
`ALUMNO(nia PK, nombre)` i `MODULO(cod_modulo PK, nombre)`. Cada entitat forta es convertix en una taula amb la seua clau.
{{% /etapa %}}
{{% etapa titulo="3. La relació N:M passa a taula" %}}
No es pot posar una FK en cap de les dues taules sense repetir files (un alumne hauria de guardar diversos mòduls en una cel·la), així que es crea una **taula intermèdia** `CURSA`.
{{% /etapa %}}
{{% etapa titulo="4. La seua clau" %}}
Les dues claus alienes formen juntes la PK composta `(nia, cod_modulo)`. Així un alumne no cursa dues vegades el mateix mòdul.
{{% /etapa %}}
{{% etapa titulo="5. Els atributs de la relació" %}}
`nota` va en `CURSA`: depén de la parella alumne-mòdul, no d'un sol.
{{% /etapa %}}
{{% etapa titulo="6. Resultat" %}}
`CURSA(nia PK,FK → ALUMNO · cod_modulo PK,FK → MODULO · nota)`
{{% /etapa %}}
{{% /paso-a-paso %}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
ALUMNO (nia, nombre)
   PK:  nia

MODULO (cod_modulo, nombre)
   PK:  cod_modulo

CURSA (nia, cod_modulo, nota)
   PK:  (nia, cod_modulo)
   FK:  nia        → ALUMNO
   FK:  cod_modulo → MODULO
```
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──N── R (r1) ──M── B (b0, b1)

A (a0, a1)          B (b0, b1)
   PK:  a0             PK:  b0

R (rA, rB, r1)
   PK:  (rA, rB)
   FK:  rA → A
   FK:  rB → B
```
{{% /tab %}}
{{% tab "Amb dades" %}}
**ALUMNO**

| nia (PK) | nombre |
|---|---|
| 10234567 | Paula Ortiz |
| 10234568 | Izan Pastor |

**MODULO**

| cod_modulo (PK) | nombre |
|---|---|
| 0484 | Bases de dades |
| 0485 | Programació |

**CURSA**

| nia (PK, FK) | cod_modulo (PK, FK) | nota |
|---|---|---|
| 10234567 | 0484 | 8,5 |
| 10234567 | 0485 | 7 |
| 10234568 | 0484 | 6,25 |

Cada valor de `nia` i de `cod_modulo` es repetix, però cap **parella** es repetix.
{{% /tab %}}
{{< /tabs >}}

> [!NOTE]
> **I si la parella es pot repetir?** Si un alumne pot cursar el mateix mòdul en diverses convocatòries i es vol guardar cada nota, la parella `(nia, cod_modulo)` ja no és suficient: s'afig a la PK l'atribut que distingix les repeticions, `CURSA (nia, cod_modulo, convocatoria, nota)` amb PK: `(nia, cod_modulo, convocatoria)`.

> [!WARNING]
> **Pèrdua semàntica.** L'(1,N) al costat de MODULO diu que **tot alumne cursa almenys un mòdul**. La taula `CURSA` no pot obligar que cada alumne tinga una fila: s'anota.

---

### 4.6 Transformació de relacions binàries 1:1

Hi ha 3 alternatives segons les cardinalitats mínimes de participació:

1. **Participació opcional en els dos costats (0,1)-(0,1):** hi ha dues solucions vàlides. La més simple propaga la clau d'una entitat a la taula de l'altra com a FK amb restricció d'unicitat (UK) que **admet nuls** (és la que usa EduGest per a la tutoria). Si es volen evitar els nuls, es crea una taula intermèdia amb la clau d'una entitat com a PK i la de l'altra com a UK obligatòria.
2. **Participació obligatòria en un costat i opcional en l'altre (0,1)-(1,1):** la clau aliena es col·loca en la taula de l'entitat la participació de la qual és **obligatòria**, referenciant l'altra, com a FK obligatòria i única (UK + VNN). Així no necessita admetre nuls.
3. **Participació obligatòria en els dos costats (1,1)-(1,1):** les dues entitats es poden unificar en una **única taula** que agrupa tots els atributs, sempre que descriguen de veritat el mateix objecte.

> [!NOTE]
> En el transformador interactiu, la regla 2 es reflectix així: si «cada A ha de tindre un B» (mínim 1) i no al revés, la clau aliena està en A.

#### Exemple 4.6-a · (0,1)-(0,1): EMPLEADO usa TAQUILLA

Un empleat pot tindre una taquilla o cap, i una taquilla pot estar lliure.

{{< figura src="ud03/teo-46a-empleado-taquilla.svg" alt="EMPLEADO (dni, nombre) usa TAQUILLA (num_taquilla, planta) amb l'atribut fecha_entrega; (0,1) al costat de cada entitat" caption="Relació 1:1 amb participació opcional en els dos costats" >}}

{{< tabs >}}
{{% tab "Opció 1: taula intermèdia" %}}
```text
EMPLEADO (dni, nombre)            TAQUILLA (num_taquilla, planta)
   PK:  dni                          PK:  num_taquilla

USA (num_taquilla, dni, fecha_entrega)
   PK:  num_taquilla
   UK:  dni
   FK:  num_taquilla → TAQUILLA
   FK:  dni          → EMPLEADO
   VNN: dni
```
- **PK** en `num_taquilla`: una taquilla apareix una vegada com a molt.
- **UK** en `dni`: un empleat apareix una vegada com a molt. Així es garantix l'«1» dels dos costats.
- No hi ha nuls: si una taquilla està lliure, simplement no té fila en `USA`.
{{% /tab %}}
{{% tab "Opció 2: FK única amb nuls" %}}
```text
EMPLEADO (dni, nombre)
   PK:  dni

TAQUILLA (num_taquilla, planta, dni, fecha_entrega)
   PK:  num_taquilla
   UK:  dni
   FK:  dni → EMPLEADO
```
Menys taules, però `dni` i `fecha_entrega` queden a `NULL` en les taquilles lliures.

> **Nota:** en Oracle, una UK d'una sola columna admet diverses files amb `NULL`, perquè `NULL` no es considera igual a `NULL`.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ─(0,1)─ R ─(0,1)─ B (b0, b1)

A (a0, a1)          B (b0, b1)
   PK:  a0             PK:  b0

R (rA, rB)
   PK:  rA
   UK:  rB
   FK:  rA → A
   FK:  rB → B
   VNN: rB
```
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.6-b · (0,1)-(1,1): PERSONA posee PASAPORTE

Tot passaport pertany a una persona; no tota persona té passaport.

{{< figura src="ud03/teo-46b-persona-pasaporte.svg" alt="PERSONA (dni, nombre) posee PASAPORTE (num_pasaporte, caducidad); al costat de PERSONA (1,1) amb línia doble, al costat de PASAPORTE (0,1)" caption="Relació 1:1 amb participació obligatòria del passaport" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
PERSONA (dni, nombre)
   PK:  dni

PASAPORTE (num_pasaporte, caducidad, dni)
   PK:  num_pasaporte
   UK:  dni
   FK:  dni → PERSONA
   VNN: dni
```
- La FK va en `PASAPORTE`, l'entitat que participa **obligatòriament**: així mai és nul·la.
- La **UK** convertix la FK en «1:1»: sense ella, una persona podria tindre diversos passaports (seria una 1:N).
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──E── R ── B (b0, b1)     (A obligatòria, B opcional)

A (a0, a1, aB)
   PK:  a0
   UK:  aB
   FK:  aB → B
   VNN: aB

B (b0, b1)
   PK:  b0
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| num_pasaporte (PK) | caducidad | dni (UK, FK, VNN) |
|---|---|---|
| PAA123456 | 2031-05-10 | 48123456P |
| PAB654321 | 2029-01-22 | 21456789K |

Un segon passaport per a `48123456P` seria rebutjat per la **UK**. Si la FK s'haguera posat en `PERSONA`, les persones sense passaport tindrien eixa columna a `NULL`.
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.6-c · (1,1)-(1,1): PAIS tiene CAPITAL

Tot país té exactament una capital i tota capital ho és d'exactament un país.

{{< figura src="ud03/teo-46c-pais-capital.svg" alt="PAIS (cod_pais, nombre) tiene CAPITAL (cod_ciudad, habitantes); (1,1) al costat de les dues entitats, amb línia doble" caption="Relació 1:1 amb participació obligatòria en els dos costats" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
PAIS (cod_pais, nombre, cod_ciudad, habitantes)
   PK:  cod_pais
   UK:  cod_ciudad
   VNN: cod_ciudad
```
Les dues entitats es fusionen en una única taula. La clau de l'altra entitat passa a ser **UK**.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ──E── R ──E── B (b0, b1)

R (a0, a1, b0, b1)
   PK:  a0
   UK:  b0
   VNN: b0
```
{{% /tab %}}
{{< /tabs >}}

> [!IMPORTANT]
> Fusionar només té sentit si les dues entitats **no participen en altres relacions** que obliguen a tindre-les separades. Si `CAPITAL` es relacionara a més amb `MUSEO`, convé mantindre dues taules i aplicar la regla 2 (FK amb UK i VNN).

---

### 4.7 Transformació de relacions reflexives / recursives

Les relacions reflexives es transformen **amb els mateixos patrons** que les binàries, però l'entitat apareix en els dos extrems. Com que la clau ha d'aparéixer **dues vegades**, es reanomena cada còpia segons el seu **rol** (`jefe`, `subordinado`…). Les dues còpies són FK cap a la **mateixa** taula.

1. **Reflexiva 1:N:** S'afig una columna de clau forana (`FK`) en la mateixa taula que **apunta a la clau primària de la mateixa taula** (autoreferència).
2. **Reflexiva 1:1:** Igual que una 1:1 binària: una FK amb **UK** en la mateixa taula, o una taula nova amb PK en un rol i UK en l'altre.
3. **Reflexiva N:M:** Es crea una **taula intermèdia** la clau primària de la qual es compon de dues columnes que fan de clau forana cap a la clau primària de la mateixa taula (representant el rol origen i el rol destinació).

#### Exemple 4.7-a · Reflexiva 1:N: EMPLEADO dirige EMPLEADO

{{< figura src="ud03/teo-47a-reflexiva-1n.svg" alt="EMPLEADO (dni, nombre) amb la relació reflexiva dirige; rol jefe (0,1) i rol subordinado (0,N)" caption="Relació reflexiva 1:N amb rols" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
EMPLEADO (dni, nombre, dni_jefe)
   PK:  dni
   FK:  dni_jefe → EMPLEADO
```
`dni_jefe` conté un DNI que ha d'existir **en la mateixa taula**. Admet nuls: el director general no té cap.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
A (a0, a1, rA)
   PK:  a0
   FK:  rA → A
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| dni (PK) | nombre | dni_jefe (FK → EMPLEADO) |
|---|---|---|
| 11111111H | Marta Lloret | `NULL` |
| 22222222J | Andrés Gil | 11111111H |
| 33333333P | Sara Vidal | 11111111H |
| 44444444A | Nerea Soler | 22222222J |

Marta dirigix Andrés i Sara; Andrés dirigix Nerea. És un **arbre** guardat en una sola taula.
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.7-b · Reflexiva 1:1: ALUMNO mentoriza ALUMNO

En el programa de mentoria, un alumne de segon mentoritza com a molt un de primer, i cada alumne de primer té com a molt un mentor.

{{< figura src="ud03/teo-47b-reflexiva-11.svg" alt="ALUMNO (nia, nombre) amb la relació reflexiva mentoriza; rol mentor (0,1) i rol mentorizado (0,1)" caption="Relació reflexiva 1:1" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
ALUMNO (nia, nombre)
   PK:  nia

MENTORIA (nia_mentorizado, nia_mentor)
   PK:  nia_mentorizado
   UK:  nia_mentor
   FK:  nia_mentorizado → ALUMNO
   FK:  nia_mentor      → ALUMNO
   VNN: nia_mentor
```
També seria vàlid posar `nia_mentor` en `ALUMNO` com a FK amb **UK** (admetent nuls), com en l'opció 2 de l'exemple 4.6-a.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
A (a0)
   PK:  a0

R (rA1, rA2)
   PK:  rA1
   UK:  rA2
   FK:  rA1 → A
   FK:  rA2 → A
```
`rA2` representa el mateix tipus de valor que `rA1`: cal duplicar-lo per a poder relacionar l'entitat amb si mateixa.
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.7-c · Reflexiva N:M: MODULO requiere MODULO

Un mòdul pot tindre diversos mòduls previs recomanats, i un mòdul pot ser previ de diversos.

{{< figura src="ud03/teo-47c-reflexiva-nm.svg" alt="MODULO (cod_modulo, nombre) amb la relació reflexiva requiere; rol previo (0,N) i rol posterior (0,N)" caption="Relació reflexiva N:M" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
MODULO (cod_modulo, nombre)
   PK:  cod_modulo

REQUIERE (cod_modulo, cod_modulo_previo)
   PK:  (cod_modulo, cod_modulo_previo)
   FK:  cod_modulo        → MODULO
   FK:  cod_modulo_previo → MODULO
```
{{% /tab %}}
{{% tab "Patró general" %}}
```text
A (a0)
   PK:  a0

R (rA1, rA2)
   PK:  (rA1, rA2)
   FK:  rA1 → A
   FK:  rA2 → A
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| cod_modulo (PK, FK) | cod_modulo_previo (PK, FK) |
|---|---|
| 0486 Accés a dades | 0484 Bases de dades |
| 0486 Accés a dades | 0485 Programació |
| 0489 Prog. multimèdia i disp. mòbils | 0485 Programació |

`0486` té dos previs i `0485` és previ de dos mòduls.
{{% /tab %}}
{{< /tabs >}}

> [!WARNING]
> Les claus no impedixen la fila `(0484, 0484)` (un mòdul previ de si mateix). S'evita amb una **regla de fila** (`cod_modulo <> cod_modulo_previo`, UD05). Els **cicles** (A requerix B i B requerix A) no es poden evitar amb restriccions d'una fila: és una pèrdua semàntica.

---

### 4.8 Transformació de relacions ternàries

Una ternària **sempre** genera una taula nova amb les tres claus propagades (cadascuna és FK). El que canvia segons les cardinalitats és **quina és la PK**:

- **Ternària N:N:N:** la `PK` és la combinació de les **tres** claus.
- **Ternària 1:N:N:** la `PK` són les claus dels **dos costats N**. La del costat 1 porta VNN.
- **Ternària 1:1:N:** la `PK` és la clau del costat N més **una** de les del costat 1. L'altra combinació (costat N + l'altre costat 1) és **UK**.
- **Ternària 1:1:1:** la `PK` són dues claus qualssevol; les altres dues combinacions són **UK**.

> [!TIP]
> Recorda el conveni de la UD02: en una ternària, el parell al costat d'una entitat compta **quantes instàncies d'ella corresponen a cada parella de les altres dues**. Si al costat de PROFESOR posa (1,1), cada parella (mòdul, grup) té **un sol** professor: per això la parella (mòdul, grup) és la que identifica la fila.

#### Exemple 4.8-a · N:N:N: PROFESOR imparte MODULO a GRUPO

Un mateix mòdul en un mateix grup es pot repartir entre diversos professors (per exemple, amb desdoblaments), i es guarden les hores de cadascun.

{{< figura src="ud03/teo-48a-ternaria-nnn.svg" alt="Relació ternària imparte entre PROFESOR (dni, nombre), MODULO (cod_modulo) i GRUPO (cod_grupo), amb l'atribut horas; PROFESOR (1,N), MODULO (0,N), GRUPO (0,N)" caption="Ternària N:N:N" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
IMPARTE (dni, cod_modulo, cod_grupo, horas)
   PK:  (dni, cod_modulo, cod_grupo)
   FK:  dni        → PROFESOR
   FK:  cod_modulo → MODULO
   FK:  cod_grupo  → GRUPO
```
(I a més les taules `PROFESOR`, `MODULO` i `GRUPO`, que ixen de les entitats.)
{{% /tab %}}
{{% tab "Patró general" %}}
```text
A (a0, a1)   PK: a0
B (b0, b1)   PK: b0
C (c0, c1)   PK: c0

R (a0, b0, c0)
   PK:  (a0, b0, c0)
   FK:  a0 → A
   FK:  b0 → B
   FK:  c0 → C
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| dni (PK, FK) | cod_modulo (PK, FK) | cod_grupo (PK, FK) | horas |
|---|---|---|---|
| 11111111H | 0484 | 1DAW | 3 |
| 22222222J | 0484 | 1DAW | 2 |
| 11111111H | 0484 | 1DAM | 5 |

Dos professors compartixen 0484 en 1DAW: és vàlid perquè la PK inclou el professor.
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.8-b · 1:N:N: un sol professor per mòdul i grup

Si el centre decidix que cada mòdul de cada grup l'impartix **un únic** professor, al costat de PROFESOR posa (1,1).

{{< figura src="ud03/teo-48b-ternaria-1nn.svg" alt="Relació ternària imparte amb PROFESOR (1,1), MODULO (0,N) i GRUPO (0,N)" caption="Ternària 1:N:N" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
IMPARTE (cod_modulo, cod_grupo, dni, horas)
   PK:  (cod_modulo, cod_grupo)
   FK:  dni        → PROFESOR
   FK:  cod_modulo → MODULO
   FK:  cod_grupo  → GRUPO
   VNN: dni
```
`dni` ja no forma part de la PK: amb la parella (mòdul, grup) n'hi ha prou per a saber qui l'impartix.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A amb cardinalitat 1; B i C amb cardinalitat N

R (a0, b0, c0)
   PK:  (b0, c0)
   FK:  a0 → A
   FK:  b0 → B
   FK:  c0 → C
   VNN: a0
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| cod_modulo (PK, FK) | cod_grupo (PK, FK) | dni (FK, VNN) | horas |
|---|---|---|---|
| 0484 | 1DAW | 11111111H | 5 |
| 0484 | 1DAM | 11111111H | 5 |
| 0485 | 1DAW | 22222222J | 8 |

La fila `(0484, 1DAW, 22222222J, 2)` seria rebutjada: ja hi ha un professor per a eixa parella.
{{% /tab %}}
{{< /tabs >}}

#### Exemple 4.8-c · 1:1:N: FRANJA, AULA i GRUPO

En l'horari, en una franja horària, un grup està en **una** aula i una aula acull **un** grup. Una mateixa parella aula-grup es repetix en moltes franges.

{{< figura src="ud03/teo-48c-ternaria-11n.svg" alt="Relació ternària ocupa entre FRANJA (cod_franja, dia) (0,N), AULA (cod_aula) (0,1) i GRUPO (cod_grupo) (0,1)" caption="Ternària 1:1:N" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
OCUPA (cod_franja, cod_aula, cod_grupo)
   PK:  (cod_franja, cod_aula)
   UK:  (cod_franja, cod_grupo)
   FK:  cod_franja → FRANJA
   FK:  cod_aula   → AULA
   FK:  cod_grupo  → GRUPO
   VNN: cod_grupo
```
- La **PK** `(cod_franja, cod_aula)` impedix ficar dos grups en la mateixa aula alhora.
- La **UK** `(cod_franja, cod_grupo)` impedix que un grup estiga en dues aules alhora.
- Es podria haver triat al revés (PK amb el grup i UK amb l'aula): les dues combinacions són claus candidates.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A i B amb cardinalitat 1; C amb cardinalitat N

R (a0, b0, c0)
   PK:  (a0, c0)
   UK:  (b0, c0)
   FK:  a0 → A
   FK:  b0 → B
   FK:  c0 → C
   VNN: b0
```
{{% /tab %}}
{{% tab "Amb dades" %}}
| cod_franja (PK, FK) | cod_aula (PK, FK) | cod_grupo (UK, FK) |
|---|---|---|
| L1 | A-1 | 1DAW |
| L1 | A-2 | 1DAM |
| L2 | A-1 | 1DAW |

- `(L1, A-1, 2ASIR)` → rebutjada per la **PK**: l'aula A-1 ja està ocupada en L1.
- `(L1, B-1, 1DAW)` → rebutjada per la **UK**: 1DAW ja està en una altra aula en L1.
{{% /tab %}}
{{< /tabs >}}

#### Ternària 1:1:1 (patró general)

És poc freqüent. Cada parella d'entitats determina la tercera, així que **qualsevol parella** servix de clau:

```text
R (a0, b0, c0)
   PK:  (a0, b0)
   UK:  (a0, c0)
   UK:  (b0, c0)
   FK:  a0 → A
   FK:  b0 → B
   FK:  c0 → C
```

---

### 4.9 Transformació de jerarquies de generalització / especialització

Hi ha 3 estratègies relacionals per a transformar jerarquies EER:

1. **Opció A (taula única per a tota la jerarquia):** Es crea una sola taula amb tots els atributs del supertipus i dels subtipus, afegint una columna discriminadora de tipus (`tipo_subtipo`). Vàlida per a especialitzacions disjuntes; en una solapada cal un indicador per subtipus.
2. **Opció B (taules per al supertipus i cada subtipus):** Es crea una taula per al supertipus (amb la `PK` principal) i una taula per cada subtipus (la `PK` i `FK` de la qual és la clau del supertipus). És la solució més neta i flexible, i la que s'usa per defecte.
3. **Opció C (taules únicament per als subtipus):** Només es creen taules per a les entitats especialitzades, duplicant els atributs del supertipus en cadascuna. Només és vàlida si la jerarquia és Total i Disjunta $(T,D)$.

#### Exemple 4.9 · Especialització d'EMPLEADO (parcial i solapada)

En el centre hi ha professors i personal administratiu. Hi ha empleats que no són ni l'una cosa ni l'altra (conserges: **parcial**) i algun professor que també fa tasques administratives (**solapada**, marca `o`).

{{< figura src="ud03/teo-49-generalizacion.svg" alt="Superclasse EMPLEADO (dni, nombre, sueldo) amb especialització solapada (cercle amb o, línia senzilla: parcial) en PROFESOR (especialidad) i ADMINISTRATIVO (puesto)" caption="Especialització parcial i solapada (P,S)" >}}

{{< tabs >}}
{{% tab "Opció B (recomanada)" %}}
```text
EMPLEADO (dni, nombre, sueldo)
   PK:  dni

PROFESOR (dni, especialidad)
   PK:  dni
   FK:  dni → EMPLEADO

ADMINISTRATIVO (dni, puesto)
   PK:  dni
   FK:  dni → EMPLEADO
```
La mateixa columna `dni` és **PK i FK** en cada subtipus: cada fila de `PROFESOR` «és» un empleat.
{{% /tab %}}
{{% tab "Opció A" %}}
```text
EMPLEADO (dni, nombre, sueldo, es_profesor, especialidad,
          es_administrativo, puesto)
   PK:  dni
   VNN: es_profesor, es_administrativo
```
Com que és **solapada**, no n'hi ha prou amb una columna `tipo`: calen dos indicadors (S/N). `especialidad` i `puesto` queden a `NULL` en moltes files.
{{% /tab %}}
{{% tab "Patró general" %}}
```text
Diagrama:   A (a0, a1) ── especialització (P,S) ──> B (b0), C (c0)

A (a0, a1)
   PK:  a0

B (b0, bA)
   PK:  bA
   FK:  bA → A

C (c0, cA)
   PK:  cA
   FK:  cA → A
```
{{% /tab %}}
{{% tab "Amb dades" %}}
**EMPLEADO**

| dni (PK) | nombre | sueldo |
|---|---|---|
| 11111111H | Marta Lloret | 2.700 |
| 22222222J | Andrés Gil | 2.650 |
| 55555555K | Pepe Ruiz | 1.600 |

**PROFESOR**

| dni (PK, FK) | especialidad |
|---|---|
| 11111111H | Informàtica |
| 22222222J | Informàtica |

**ADMINISTRATIVO**

| dni (PK, FK) | puesto |
|---|---|
| 22222222J | Secretaria |

Andrés està en les dues subtaules (**solapada**). Pepe, el conserge, només està en `EMPLEADO` (**parcial**).
{{% /tab %}}
{{< /tabs >}}

> [!WARNING]
> **Pèrdua semàntica.** Amb l'opció B, el model relacional representa de manera natural l'especialització **parcial i solapada**. Si fora **total** («tot empleat és professor o administratiu») o **disjunta** («ningú és les dues coses»), les claus no ho poden impedir: s'anota i es controla amb disparadors (UD08).

{{< quiz >}}
- q: "Tot `PASAPORTE` pertany a una persona, però no tota `PERSONA` té passaport. On va la clau aliena?"
  options: ["En `PERSONA`, obligatòria i única", "En `PASAPORTE`, obligatòria i única", "En les dues taules", "En una taula nova obligatòriament"]
  answer: 1
  explain: "La clau aliena va en la taula de l'entitat amb participació obligatòria (`PASAPORTE`): mai és nul·la i la unicitat garantix l'«1» de l'altre costat."
- q: "`AULA` és feble per identificació respecte a `EDIFICIO`. Quina és la seua clau primària?"
  options: ["`num_aula`", "`id_edificio`", "`(id_edificio, num_aula)`", "No té clau primària"]
  answer: 2
  explain: "El número d'aula només és únic dins de cada edifici: la clau primària inclou la clau del propietari (que a més és clau aliena)."
- q: "`SESION` es relaciona 1:N amb `AULA`, la PK de la qual és `(cod_edificio, num_aula)`. Com és la clau aliena en `SESION`?"
  options: ["Dues FK: `cod_edificio → EDIFICIO` i `num_aula → AULA`", "Una FK composta: `(cod_edificio, num_aula) → AULA`", "Només `num_aula → AULA`", "No cal FK"]
  answer: 1
  explain: "Una FK apunta sempre a la PK completa. Amb dues FK separades s'acceptaria una aula que no existix en eixe edifici."
- q: "En una ternària `IMPARTE` amb PROFESOR (1,1), MODULO (0,N) i GRUPO (0,N), quina és la PK?"
  options: ["`(dni, cod_modulo, cod_grupo)`", "`(cod_modulo, cod_grupo)`", "`(dni, cod_grupo)`", "`dni`"]
  answer: 1
  explain: "És una 1:N:N: les claus dels costats N formen la PK; la del costat 1 (`dni`) porta VNN."
- q: "En la ternària 1:1:N d'`OCUPA(cod_franja, cod_aula, cod_grupo)`, què evita la UK `(cod_franja, cod_grupo)`?"
  options: ["Que una aula tinga dos grups alhora", "Que un grup estiga en dues aules alhora", "Que una franja no tinga aula", "Res: sobra"]
  answer: 1
  explain: "La PK (franja, aula) controla l'aula; la UK (franja, grup) controla el grup. Les dues són necessàries."
- q: "Una relació reflexiva 1:N `EMPLEADO dirige EMPLEADO`, quantes taules genera?"
  options: ["Cap de nova: una FK `dni_jefe → EMPLEADO` en la mateixa taula", "Una taula nova `DIRIGE`", "Dues taules `JEFE` i `SUBORDINADO`", "Una taula nova amb PK composta"]
  answer: 0
  explain: "És com una 1:N qualsevol, però els dos extrems són la mateixa taula: la clau es duplica amb un altre nom."
{{< /quiz >}}

---

### 4.10 Transformació d'agregacions

- **Regla:** La relació agregada es transforma primer segons el seu tipus (normalment N:M, amb la seua taula intermèdia). Després, eixa taula **actua com una entitat més**: la seua PK és la que es propaga a la relació amb la tercera entitat.

#### Exemple 4.10 · La matrícula, avaluada per un professor

Un alumne cursa mòduls (N:M, amb la data de matrícula). Cada **matrícula** concreta (alumne-mòdul) pot tindre assignat un professor avaluador. No s'avalua l'alumne ni el mòdul per separat, sinó la parella: per això s'agrega `cursa` com a `MATRICULA`.

{{< figura src="ud03/teo-410-agregacion.svg" alt="Agregació MATRICULA que conté ALUMNO (nia, nombre), la relació cursa (fecha_mat) i MODULO (cod_modulo, nombre); l'agregació es relaciona mitjançant evalua amb PROFESOR (dni, nombre): (0,N) al costat de MATRICULA, (0,1) al costat de PROFESOR" caption="Agregació: la relació cursa actua com a entitat" >}}

{{< tabs >}}
{{% tab "Esquema relacional" %}}
```text
ALUMNO (nia, nombre)          PK: nia
MODULO (cod_modulo, nombre)   PK: cod_modulo
PROFESOR (dni, nombre)        PK: dni

CURSA (nia, cod_modulo, fecha_mat, dni_evaluador)
   PK:  (nia, cod_modulo)
   FK:  nia           → ALUMNO
   FK:  cod_modulo    → MODULO
   FK:  dni_evaluador → PROFESOR
```
`evalua` és 1:N des de l'agregació: la clau del professor viatja a la taula de l'agregació (`CURSA`), com en qualsevol 1:N.
{{% /tab %}}
{{% tab "Si evalua fora N:M" %}}
```text
CURSA (nia, cod_modulo, fecha_mat)
   PK:  (nia, cod_modulo)
   FK:  nia        → ALUMNO
   FK:  cod_modulo → MODULO

EVALUA (nia, cod_modulo, dni)
   PK:  (nia, cod_modulo, dni)
   FK:  (nia, cod_modulo) → CURSA
   FK:  dni               → PROFESOR
```
La FK apunta a `CURSA` i és **composta**: així només es pot avaluar una matrícula que existisca. Si es posara `nia → ALUMNO` i `cod_modulo → MODULO` per separat, es podria avaluar un alumne en un mòdul que no cursa.
{{% /tab %}}
{{< /tabs >}}

---

### 4.11 Pèrdues semàntiques en la transformació

Hi ha informació del diagrama E/R que **no es pot representar** amb PK, FK, UK i VNN. A això se li diu **pèrdua semàntica**. No es resol en el disseny lògic: s'anota i s'implementa després amb regles de fila, disparadors (*triggers*) o procediments emmagatzemats (UD08). L'apartat 6 explica com documentar-les.

| Situació del diagrama | Exemple | Per què es perd? |
|---|---|---|
| Mínim 1 en el costat 1 d'una 1:N | Tot departament té almenys un empleat (4.4-b) | La FK està en `EMPLEADO`; res obliga que cada departament hi aparega |
| Mínim 1 en una N:M | Tot alumne cursa almenys un mòdul (4.5) | Res obliga que cada alumne tinga files en `CURSA` |
| Existència d'una entitat respecte a una relació que està en **una altra** taula | Tota persona té passaport, si la FK està en `PASAPORTE` | Només es pot obligar amb VNN en la taula on està la FK |
| Atribut multivalorat amb mínim 1 | Tota persona té almenys un telèfon (4.3) | La taula `TELEFONO` pot no tindre files d'eixa persona |
| Generalització total o disjunta | Ningú és alhora professor i administratiu (4.9) | Les claus de dues taules diferents no es comparen entre si |
| Mínims en agregacions i ternàries | Tota matrícula té avaluador | Igual que en les binàries, depén d'altres taules |
| Cicles en reflexives | Un mòdul no pot ser previ de si mateix a través d'altres (4.7-c) | Implica recórrer diverses files |

---

### 4.12 Taula resum: patrons de transformació

Esta taula reunix els **patrons generals** dels exemples anteriors. És la xuleta per a resoldre les tasques de transformació.

| Cas de l'E/R | Taules | Esquema resultant |
|---|---|---|
| Entitat forta | 1 | `A (a0, a1)` · PK: a0 |
| Feble per identificació | 1 per entitat | `A (a0, a1, aB)` · PK: (a0, aB) · FK: aB → B |
| Feble per existència / 1:N obligatòria | 1 per entitat | `A (a0, a1, aB)` · PK: a0 · FK: aB → B · VNN: aB |
| 1:N opcional | 1 per entitat | `A (a0, a1, aB)` · PK: a0 · FK: aB → B |
| 1:N amb PK composta en el costat 1 | 1 per entitat | `A (a0, aB0, aB1)` · PK: a0 · FK: (aB0, aB1) → B |
| N:M | 3 | `R (rA, rB, r1)` · PK: (rA, rB) · FK: rA → A · FK: rB → B |
| 1:1 (0,1)-(0,1) | 3 | `R (rA, rB)` · PK: rA · UK: rB · FK: rA → A · FK: rB → B · VNN: rB |
| 1:1 (1,1)-(0,1) | 2 | `A (a0, a1, aB)` · PK: a0 · UK: aB · FK: aB → B · VNN: aB |
| 1:1 (1,1)-(1,1) | 1 | `R (a0, a1, b0, b1)` · PK: a0 · UK: b0 · VNN: b0 |
| Reflexiva 1:N | 1 | `A (a0, rA)` · PK: a0 · FK: rA → A |
| Reflexiva 1:1 | 2 | `R (rA1, rA2)` · PK: rA1 · UK: rA2 · FK: rA1 → A · FK: rA2 → A |
| Reflexiva N:M | 2 | `R (rA1, rA2)` · PK: (rA1, rA2) · FK: rA1 → A · FK: rA2 → A |
| Ternària N:N:N | 4 | `R (a0, b0, c0)` · PK: (a0, b0, c0) · 3 FK |
| Ternària 1:N:N (A és el costat 1) | 4 | `R (a0, b0, c0)` · PK: (b0, c0) · VNN: a0 · 3 FK |
| Ternària 1:1:N (C és el costat N) | 4 | `R (a0, b0, c0)` · PK: (a0, c0) · UK: (b0, c0) · VNN: b0 · 3 FK |
| Ternària 1:1:1 | 4 | `R (a0, b0, c0)` · PK: (a0, b0) · UK: (a0, c0) · UK: (b0, c0) · 3 FK |
| Generalització (opció B) | 1 + 1 per subtipus | `B (b0, bA)` · PK: bA · FK: bA → A |
| Atribut multivalorat | 2 | `A2 (a0, a2)` · PK: (a0, a2) · FK: a0 → A |

> [!TIP]
> **Comprovació ràpida de qualsevol transformació:** agafa cada FK i pregunta't *es pot repetir?* (si no, li falta UK o forma part de la PK) i *pot faltar?* (si no, li falta VNN). És el mateix raonament, al revés, de la [pràctica 3.6](/ud03-modelo-relacional/ud03-practicas#ANCLA_36).

---

