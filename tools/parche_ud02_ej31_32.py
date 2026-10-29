#!/usr/bin/env python3
"""Reescribe con más claridad los enunciados de los ejercicios 31 y 32 de la UD02.

Uso: python3 tools/parche_ud02_ej31_32.py [raiz ...]
Por defecto actúa sobre content.es/content.val y, si existe, privado/content.es/content.val.
"""
import os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ES31 = """> Berlín, el de la serie *Berlín*, ha montado su propia aerolínea para sus golpes por Europa y necesita una base de datos que no sea una servilleta.
>
> La base de datos guarda varias compañías aéreas, porque Berlín también vende plazas en vuelos de otras compañías. De cada compañía se conoce un código interno, un nombre y un país.
>
> Cada compañía tiene su flota de aeronaves. De cada aeronave se guarda la matrícula, que la identifica, y la fecha en que entró en servicio; una aeronave pertenece a una sola compañía. Además, cada aeronave es de un modelo concreto, del que se conoce el fabricante, la capacidad de pasajeros y la autonomía en kilómetros; de un mismo modelo puede haber muchas aeronaves.
>
> Los aeropuertos se identifican por su código IATA (VLC, MAD, LIM…) y tienen nombre, ciudad, país y unas coordenadas formadas por latitud y longitud, que siempre se consultan juntas.
>
> Una ruta es un par ordenado de aeropuertos (origen y destino) entre los que se puede volar; de cada ruta solo se guarda la distancia en kilómetros. Las rutas son un catálogo común: no interesa qué compañía las opera, solo que existen. Valencia-Madrid y Madrid-Valencia son dos rutas distintas. Ojo: una ruta no es un vuelo; la ruta es un dato permanente y el vuelo ocurre un día concreto.
>
> Un vuelo no tiene un código único en el mundo: el vuelo «IB6250» lo opera la misma compañía todos los días. Por eso un vuelo se identifica por tres datos a la vez: la compañía que lo opera, el número de vuelo y la fecha. Un vuelo no puede existir sin su compañía. Cuando el vuelo termina se calcula su duración real.
>
> Cada vuelo se divide en uno o varios tramos, numerados dentro del vuelo (1, 2, 3…). Un vuelo directo tiene un único tramo; uno con escala tiene varios: por ejemplo, el tramo 1 es Valencia-Madrid y el tramo 2, Madrid-Lima. De cada tramo se guardan la hora de salida y la de llegada, el aeropuerto del que sale y el aeropuerto al que llega. Cada tramo lo realiza una única aeronave, y una aeronave realiza muchos tramos a lo largo del día.
>
> De cada empleado se guarda el DNI, el nombre y la fecha de alta; su antigüedad se calcula a partir de esa fecha. Algunos empleados son pilotos (número de licencia y horas de vuelo), otros son tripulantes de cabina (hablan uno o varios idiomas) y otros son instructores (especialidad). Un empleado puede pertenecer a más de un grupo: un piloto veterano puede ser también instructor. Y hay empleados que no pertenecen a ninguno, como el personal de tierra.
>
> Los roles que se pueden desempeñar a bordo forman un catálogo (comandante, copiloto, jefe de cabina, sobrecargo…) con un código y una descripción. En cada tramo trabajan varios empleados, y cada uno desempeña en él uno o varios roles: en vuelos cortos, por ejemplo, el jefe de cabina hace también de sobrecargo. De cada asignación (empleado, tramo y rol) se anota la hora de presentación. Un mismo empleado trabaja en muchos tramos y puede desempeñar roles distintos en cada uno. Por seguridad, en un tramo solo puede haber un comandante; esta regla no se puede expresar en el diagrama y tendrás que recogerla como restricción.
>
> De cada pasajero se guarda el número de pasaporte, que lo identifica, el nombre y uno o varios teléfonos. Las tarifas tienen un código, un nombre (Basic, Classic, Plus…) y los kilos de equipaje incluidos.
>
> Un pasajero reserva plaza en un vuelo (no en un tramo) con una tarifa; de cada reserva se guardan el asiento y el precio pagado. En un mismo vuelo, un pasajero viaja con una sola tarifa. En cambio, puede volar muchas veces, con tarifas distintas en vuelos distintos, y en un vuelo viajan muchos pasajeros con la misma tarifa."""

VAL31 = """> Berlín, el de la sèrie *Berlín*, ha muntat la seua pròpia aerolínia per als seus colps per Europa i necessita una base de dades que no siga un tovalló.
>
> La base de dades guarda diverses companyies aèries, perquè Berlín també ven places en vols d'altres companyies. De cada companyia es coneix un codi intern, un nom i un país.
>
> Cada companyia té la seua flota d'aeronaus. De cada aeronau es guarda la matrícula, que la identifica, i la data en què va entrar en servei; una aeronau pertany a una sola companyia. A més, cada aeronau és d'un model concret, del qual es coneix el fabricant, la capacitat de passatgers i l'autonomia en quilòmetres; d'un mateix model hi pot haver moltes aeronaus.
>
> Els aeroports s'identifiquen pel seu codi IATA (VLC, MAD, LIM…) i tenen nom, ciutat, país i unes coordenades formades per latitud i longitud, que sempre es consulten juntes.
>
> Una ruta és un parell ordenat d'aeroports (origen i destinació) entre els quals es pot volar; de cada ruta només es guarda la distància en quilòmetres. Les rutes són un catàleg comú: no interessa quina companyia les opera, només que existeixen. València-Madrid i Madrid-València són dues rutes distintes. Compte: una ruta no és un vol; la ruta és una dada permanent i el vol té lloc un dia concret.
>
> Un vol no té un codi únic al món: el vol «IB6250» l'opera la mateixa companyia tots els dies. Per això un vol s'identifica per tres dades alhora: la companyia que l'opera, el número de vol i la data. Un vol no pot existir sense la seua companyia. Quan el vol acaba se'n calcula la durada real.
>
> Cada vol es divideix en un o diversos trams, numerats dins del vol (1, 2, 3…). Un vol directe té un sol tram; un amb escala en té diversos: per exemple, el tram 1 és València-Madrid i el tram 2, Madrid-Lima. De cada tram es guarden l'hora d'eixida i la d'arribada, l'aeroport del qual ix i l'aeroport al qual arriba. Cada tram el fa una única aeronau, i una aeronau fa molts trams al llarg del dia.
>
> De cada empleat es guarda el DNI, el nom i la data d'alta; l'antiguitat es calcula a partir d'eixa data. Alguns empleats són pilots (número de llicència i hores de vol), altres són tripulants de cabina (parlen un o diversos idiomes) i altres són instructors (especialitat). Un empleat pot pertànyer a més d'un grup: un pilot veterà pot ser també instructor. I hi ha empleats que no pertanyen a cap, com el personal de terra.
>
> Els rols que es poden exercir a bord formen un catàleg (comandant, copilot, cap de cabina, sobrecàrrec…) amb un codi i una descripció. En cada tram treballen diversos empleats, i cadascun hi exerceix un o diversos rols: en vols curts, per exemple, el cap de cabina fa també de sobrecàrrec. De cada assignació (empleat, tram i rol) s'anota l'hora de presentació. Un mateix empleat treballa en molts trams i pot exercir rols distints en cadascun. Per seguretat, en un tram només hi pot haver un comandant; esta regla no es pot expressar en el diagrama i l'hauràs de recollir com a restricció.
>
> De cada passatger es guarda el número de passaport, que l'identifica, el nom i un o diversos telèfons. Les tarifes tenen un codi, un nom (Basic, Classic, Plus…) i els quilos d'equipatge inclosos.
>
> Un passatger reserva plaça en un vol (no en un tram) amb una tarifa; de cada reserva es guarden el seient i el preu pagat. En un mateix vol, un passatger viatja amb una sola tarifa. En canvi, pot volar moltes vegades, amb tarifes distintes en vols distints, i en un vol viatgen molts passatgers amb la mateixa tarifa."""

ES32 = """> El hospital de *Hospital Central* crece: ahora tiene plantas, habitaciones, camas y hasta prescripciones, y necesita una base de datos a la altura.
>
> De cada paciente se guarda el número de historia clínica, que lo identifica, el nombre, la fecha de nacimiento (la edad se calcula a partir de ella), las alergias (puede no tener ninguna o tener varias) y la dirección. El servicio de admisión necesita la dirección por partes: calle, número, código postal y localidad.
>
> Un paciente puede ingresar muchas veces. Los ingresos se numeran dentro de cada paciente (ingreso 1, ingreso 2…), así que el número de ingreso por sí solo no identifica un ingreso: hace falta saber de qué paciente es. De cada ingreso se guardan la fecha de ingreso, la fecha de alta (vacía mientras el paciente sigue ingresado) y el motivo.
>
> El hospital se organiza en plantas, identificadas por su número y con un nombre. Las habitaciones se numeran desde 1 dentro de cada planta (la planta 2 y la planta 3 tienen las dos una habitación 1) y tienen un tipo: individual o doble. A su vez, las camas se distinguen por una letra (A, B…) dentro de cada habitación. Toda planta tiene al menos una habitación y toda habitación, al menos una cama.
>
> Durante la estancia, un ingreso va ocupando camas. De cada ocupación se guardan la fecha de inicio y la de fin. El paciente puede cambiar de cama e incluso volver más tarde a una cama que ya ocupó en el mismo ingreso; por eso la misma pareja ingreso-cama puede repetirse en fechas distintas. Con el tiempo, una cama la ocupan muchos ingresos.
>
> Cada miembro del personal se identifica por un código y tiene nombre y DNI. Hay tres grupos: médicos (especialidad y número de colegiado), enfermeros (titulación) y docentes (categoría); los docentes son los que tutorizan a los residentes. Una persona puede estar en más de un grupo (es habitual que un médico sea también docente) y hay personal, como el administrativo, que no está en ninguno.
>
> Cada persona tiene como máximo un supervisor, que también forma parte del personal; un supervisor puede tener muchas personas a su cargo.
>
> Un médico atiende muchos ingresos, y cada ingreso lo atienden uno o varios médicos. De cada atención (un médico concreto con un ingreso concreto) se anota la fecha de la primera visita.
>
> Durante una atención, el médico prescribe medicamentos. De cada medicamento se guarda el código, el nombre y sus principios activos (uno o varios). De cada prescripción se guardan la fecha, la dosis y la frecuencia. Dentro de una misma atención, cada medicamento se prescribe una sola vez: si cambia la pauta, se modifica la prescripción existente. La prescripción no se hace «a un médico» ni «a un ingreso» por separado, sino dentro de una atención concreta."""

VAL32 = """> L'hospital d'*Hospital Central* creix: ara té plantes, habitacions, llits i fins i tot prescripcions, i necessita una base de dades a l'altura.
>
> De cada pacient es guarda el número d'història clínica, que l'identifica, el nom, la data de naixement (l'edat es calcula a partir d'ella), les al·lèrgies (pot no tindre'n cap o tindre'n diverses) i l'adreça. El servei d'admissió necessita l'adreça per parts: carrer, número, codi postal i localitat.
>
> Un pacient pot ingressar moltes vegades. Els ingressos es numeren dins de cada pacient (ingrés 1, ingrés 2…), així que el número d'ingrés tot sol no identifica un ingrés: cal saber de quin pacient és. De cada ingrés es guarden la data d'ingrés, la data d'alta (buida mentre el pacient continua ingressat) i el motiu.
>
> L'hospital s'organitza en plantes, identificades pel seu número i amb un nom. Les habitacions es numeren des d'1 dins de cada planta (la planta 2 i la planta 3 tenen totes dues una habitació 1) i tenen un tipus: individual o doble. Al seu torn, els llits es distingeixen per una lletra (A, B…) dins de cada habitació. Tota planta té almenys una habitació i tota habitació, almenys un llit.
>
> Durant l'estada, un ingrés va ocupant llits. De cada ocupació es guarden la data d'inici i la de fi. El pacient pot canviar de llit i fins i tot tornar més tard a un llit que ja va ocupar en el mateix ingrés; per això la mateixa parella ingrés-llit es pot repetir en dates distintes. Amb el temps, un llit l'ocupen molts ingressos.
>
> Cada membre del personal s'identifica per un codi i té nom i DNI. Hi ha tres grups: metges (especialitat i número de col·legiat), infermers (titulació) i docents (categoria); els docents són els que tutoritzen els residents. Una persona pot estar en més d'un grup (és habitual que un metge siga també docent) i hi ha personal, com l'administratiu, que no està en cap.
>
> Cada persona té com a màxim un supervisor, que també forma part del personal; un supervisor pot tindre moltes persones al seu càrrec.
>
> Un metge atén molts ingressos, i cada ingrés l'atenen un o diversos metges. De cada atenció (un metge concret amb un ingrés concret) s'anota la data de la primera visita.
>
> Durant una atenció, el metge prescriu medicaments. De cada medicament es guarda el codi, el nom i els seus principis actius (un o diversos). De cada prescripció es guarden la data, la dosi i la freqüència. Dins d'una mateixa atenció, cada medicament es prescriu una sola vegada: si canvia la pauta, es modifica la prescripció existent. La prescripció no es fa «a un metge» ni «a un ingrés» per separat, sinó dins d'una atenció concreta."""

# (lang, inicio de sección, fin de sección, enunciado nuevo, sustituciones exactas)
CAMBIOS = [
    ('es', '### Ejercicio 31 ·', '### Ejercicio 32 ·', ES31, '#### Enunciado', '{{% details title="Tareas', [
        ('3. Calcula las cardinalidades de las dos ternarias fijando, por turnos, dos de sus entidades.',
         '3. Calcula las cardinalidades de las dos ternarias, *reserva* (pasajero, vuelo, tarifa) y *tripulación* (empleado, tramo, rol), fijando por turnos dos de sus entidades.'),
        ('- [ ] *Ruta* es una relación reflexiva N:M entre `AEROPUERTO` con roles origen y destino, y *sale de* y *llega a* son dos relaciones distintas.',
         '- [ ] *Ruta* es una relación reflexiva N:M entre `AEROPUERTO` con roles origen y destino y el atributo `distancia`; no está unida a `COMPAÑÍA`.\n- [ ] *Sale de* y *llega a* son dos relaciones distintas entre `TRAMO` y `AEROPUERTO`.'),
        ('- [ ] *Reserva* tiene `TARIFA` con máximo 1 y *tripulación* tiene las tres entidades con máximo N.',
         '- [ ] *Reserva* (`PASAJERO`, `VUELO`, `TARIFA`) tiene `TARIFA` con máximo 1, y *tripulación* (`EMPLEADO`, `TRAMO`, `ROL`) tiene las tres entidades con máximo N.'),
    ]),
    ('val', '### Exercici 31 ·', '### Exercici 32 ·', VAL31, '#### Enunciat', '{{% details title="Tasques', [
        ('3. Calcula les cardinalitats de les dues ternàries fixant, per torns, dues de les seues entitats.',
         '3. Calcula les cardinalitats de les dues ternàries, *reserva* (passatger, vol, tarifa) i *tripulació* (empleat, tram, rol), fixant per torns dues de les seues entitats.'),
        ('- [ ] *Ruta* és una relació reflexiva N:M entre `AEROPUERTO` amb rols origen i destinació, i *ix de* i *arriba a* són dues relacions distintes.',
         '- [ ] *Ruta* és una relació reflexiva N:M entre `AEROPUERTO` amb rols origen i destinació i l\'atribut `distancia`; no està unida a `COMPAÑÍA`.\n- [ ] *Ix de* i *arriba a* són dues relacions distintes entre `TRAMO` i `AEROPUERTO`.'),
        ('- [ ] *Reserva* té `TARIFA` amb màxim 1 i *tripulació* té les tres entitats amb màxim N.',
         '- [ ] *Reserva* (`PASAJERO`, `VUELO`, `TARIFA`) té `TARIFA` amb màxim 1, i *tripulació* (`EMPLEADO`, `TRAMO`, `ROL`) té les tres entitats amb màxim N.'),
    ]),
    ('es', '### Ejercicio 32 ·', '### Ejercicio 33 ·', ES32, '#### Enunciado', '{{% details title="Tareas', [
        ('Resolver un caso con tres niveles de entidades débiles, una reflexiva 1:N con roles, una especialización solapada y una agregación que se relaciona con otra entidad.',
         'Resolver un caso con tres entidades débiles en dos cadenas (`PLANTA` → `HABITACIÓN` → `CAMA` y `PACIENTE` → `INGRESO`), una reflexiva 1:N con roles, una especialización parcial y solapada y una agregación que se relaciona con otra entidad.'),
        ('- [ ] *Prescribe* relaciona la agregación *atención* con `MEDICAMENTO`.',
         '- [ ] *Prescribe* relaciona la agregación *atención* con `MEDICAMENTO` (N:M) y no necesita discriminador: cada medicamento se prescribe una sola vez por atención.'),
    ]),
    ('val', '### Exercici 32 ·', '### Exercici 33 ·', VAL32, '#### Enunciat', '{{% details title="Tasques', [
        ('Resoldre un cas amb tres nivells d\'entitats febles, una reflexiva 1:N amb rols, una especialització solapada i una agregació que es relaciona amb una altra entitat.',
         'Resoldre un cas amb tres entitats febles en dues cadenes (`PLANTA` → `HABITACIÓN` → `CAMA` i `PACIENTE` → `INGRESO`), una reflexiva 1:N amb rols, una especialització parcial i solapada i una agregació que es relaciona amb una altra entitat.'),
        ('- [ ] *Prescriu* relaciona l\'agregació *atenció* amb `MEDICAMENTO`.',
         '- [ ] *Prescriu* relaciona l\'agregació *atenció* amb `MEDICAMENTO` (N:M) i no necessita discriminador: cada medicament es prescriu una sola vegada per atenció.'),
    ]),
]


def aplicar(base):
    for lang, ini, fin, enunciado, cab, tras, subs in CAMBIOS:
        f = os.path.join(base, f'content.{lang}', 'ud02-modelo-er', 'ud02-practicas.md')
        if not os.path.exists(f):
            continue
        t = open(f, encoding='utf-8').read()
        a, b = t.index(ini), t.index(fin)
        sec = t[a:b]
        e0 = sec.index(cab) + len(cab)
        e1 = sec.index(tras, e0)
        sec = sec[:e0] + '\n\n' + enunciado + '\n\n' + sec[e1:]
        for viejo, nuevo in subs:
            if nuevo in sec:
                continue
            assert sec.count(viejo) == 1, (f, viejo[:60])
            sec = sec.replace(viejo, nuevo)
        open(f, 'w', encoding='utf-8', newline='\n').write(t[:a] + sec + t[b:])
        print('ok', os.path.relpath(f, base), ini)


if __name__ == '__main__':
    bases = sys.argv[1:] or [RAIZ, os.path.join(RAIZ, 'privado')]
    for base in bases:
        if os.path.isdir(base):
            aplicar(base)
