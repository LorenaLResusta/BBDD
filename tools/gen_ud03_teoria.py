#!/usr/bin/env python3
"""Diagramas de Chen de los ejemplos del apartado 4 de la teoría de la UD03.

Uso: python3 tools/gen_ud03_teoria.py   → escribe assets/images/ud03/teo-*.svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chen_eer import A, K, KP, MV, AK, C, E, R, ISA, AGG, Model, draw  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "ud03")

M = {
    "teo-41-alumno": Model("Entidad fuerte ALUMNO", "Entidad fuerte con identificador y clave alternativa",
        [E("ALUMNO", [K("nia"), AK("dni"), A("nombre"), A("fecha_nac")])]),
    "teo-42a-edificio-aula": Model("EDIFICIO identifica AULA", "Entidad débil por identificación",
        [E("EDIFICIO", [K("cod_edificio"), A("nombre")]), E("AULA", [KP("num_aula"), A("capacidad")], weak=True)],
        [R("tiene", [("EDIFICIO", "(1,1)", None), ("AULA", "(1,N)", None)], ident=True)]),
    "teo-42b-cliente-pedido": Model("CLIENTE realiza PEDIDO", "Entidad débil por existencia",
        [E("CLIENTE", [K("cod_cliente"), A("nombre")]), E("PEDIDO", [K("num_pedido"), A("fecha")])],
        [R("realiza", [("CLIENTE", "(1,1)", None), ("PEDIDO", "(0,N)", None)], exist="PEDIDO")]),
    "teo-43-persona": Model("PERSONA con atributo compuesto y multivaluado", "Atributos compuestos y multivaluados",
        [E("PERSONA", [K("dni"), A("nombre"), C("direccion", "calle", "numero", "ciudad"), MV("telefono")])]),
    "teo-44a-emp-dep-opcional": Model("EMPLEADO trabaja en DEPARTAMENTO (0,1)", "Relación 1:N con participación opcional",
        [E("EMPLEADO", [K("dni"), A("nombre")]), E("DEPARTAMENTO", [K("cod_dep"), A("nombre")])],
        [R("trabaja", [("EMPLEADO", "(0,N)", None), ("DEPARTAMENTO", "(0,1)", None)], [A("fecha_alta")])]),
    "teo-44b-emp-dep-obligatoria": Model("EMPLEADO trabaja en DEPARTAMENTO (1,1)", "Relación 1:N con participación obligatoria",
        [E("EMPLEADO", [K("dni"), A("nombre")]), E("DEPARTAMENTO", [K("cod_dep"), A("nombre")])],
        [R("trabaja", [("EMPLEADO", "(1,N)", None), ("DEPARTAMENTO", "(1,1)", None)], [A("fecha_alta")])]),
    "teo-44c-sesion-aula": Model("SESION se imparte en AULA", "Clave ajena compuesta",
        [E("SESION", [K("id_sesion"), A("dia"), A("hora")]), E("AULA", [K("cod_edificio"), K("num_aula"), A("capacidad")])],
        [R("se_imparte", [("SESION", "(0,N)", None), ("AULA", "(1,1)", None)])]),
    "teo-45-alumno-modulo": Model("ALUMNO cursa MODULO", "Relación N:M con atributo",
        [E("ALUMNO", [K("nia"), A("nombre")]), E("MODULO", [K("cod_modulo"), A("nombre")])],
        [R("cursa", [("ALUMNO", "(0,N)", None), ("MODULO", "(1,N)", None)], [A("nota")])]),
    "teo-46a-empleado-taquilla": Model("EMPLEADO usa TAQUILLA", "Relación 1:1 (0,1)-(0,1)",
        [E("EMPLEADO", [K("dni"), A("nombre")]), E("TAQUILLA", [K("num_taquilla"), A("planta")])],
        [R("usa", [("EMPLEADO", "(0,1)", None), ("TAQUILLA", "(0,1)", None)], [A("fecha_entrega")])]),
    "teo-46b-persona-pasaporte": Model("PERSONA posee PASAPORTE", "Relación 1:1 (1,1)-(0,1)",
        [E("PERSONA", [K("dni"), A("nombre")]), E("PASAPORTE", [K("num_pasaporte"), A("caducidad")])],
        [R("posee", [("PERSONA", "(1,1)", None), ("PASAPORTE", "(0,1)", None)])]),
    "teo-46c-pais-capital": Model("PAIS tiene CAPITAL", "Relación 1:1 (1,1)-(1,1)",
        [E("PAIS", [K("cod_pais"), A("nombre")]), E("CAPITAL", [K("cod_ciudad"), A("habitantes")])],
        [R("tiene", [("PAIS", "(1,1)", None), ("CAPITAL", "(1,1)", None)])]),
    "teo-47a-reflexiva-1n": Model("EMPLEADO dirige EMPLEADO", "Reflexiva 1:N",
        [E("EMPLEADO", [K("dni"), A("nombre")])],
        [R("dirige", [("EMPLEADO", "(0,1)", "jefe"), ("EMPLEADO", "(0,N)", "subordinado")])]),
    "teo-47b-reflexiva-11": Model("ALUMNO mentoriza ALUMNO", "Reflexiva 1:1",
        [E("ALUMNO", [K("nia"), A("nombre")])],
        [R("mentoriza", [("ALUMNO", "(0,1)", "mentor"), ("ALUMNO", "(0,1)", "mentorizado")])]),
    "teo-47c-reflexiva-nm": Model("MODULO requiere MODULO", "Reflexiva N:M",
        [E("MODULO", [K("cod_modulo"), A("nombre")])],
        [R("requiere", [("MODULO", "(0,N)", "previo"), ("MODULO", "(0,N)", "posterior")])]),
    "teo-48a-ternaria-nnn": Model("Ternaria N:N:N", "PROFESOR imparte MODULO a GRUPO",
        [E("PROFESOR", [K("dni"), A("nombre")]), E("MODULO", [K("cod_modulo")]), E("GRUPO", [K("cod_grupo")])],
        [R("imparte", [("PROFESOR", "(1,N)", None), ("MODULO", "(0,N)", None), ("GRUPO", "(0,N)", None)], [A("horas")])]),
    "teo-48b-ternaria-1nn": Model("Ternaria 1:N:N", "Un solo profesor por módulo y grupo",
        [E("PROFESOR", [K("dni"), A("nombre")]), E("MODULO", [K("cod_modulo")]), E("GRUPO", [K("cod_grupo")])],
        [R("imparte", [("PROFESOR", "(1,1)", None), ("MODULO", "(0,N)", None), ("GRUPO", "(0,N)", None)], [A("horas")])]),
    "teo-48c-ternaria-11n": Model("Ternaria 1:1:N", "FRANJA, AULA y GRUPO",
        [E("FRANJA", [K("cod_franja"), A("dia")]), E("AULA", [K("cod_aula")]), E("GRUPO", [K("cod_grupo")])],
        [R("ocupa", [("FRANJA", "(0,N)", None), ("AULA", "(0,1)", None), ("GRUPO", "(0,1)", None)])]),
    "teo-49-generalizacion": Model("Especialización de EMPLEADO", "Generalización parcial y solapada",
        [E("EMPLEADO", [K("dni"), A("nombre"), A("sueldo")]), E("PROFESOR", [A("especialidad")]),
         E("ADMINISTRATIVO", [A("puesto")])],
        isas=[ISA("EMPLEADO", ["PROFESOR", "ADMINISTRATIVO"], "o", False)],
        pos={"EMPLEADO": (2.2, 0), "ISA:EMPLEADO": (2.2, 1.4), "PROFESOR": (0.6, 2.6), "ADMINISTRATIVO": (3.9, 2.6)}),
    "teo-410-agregacion": Model("Agregación MATRICULA", "La relación cursa agregada se relaciona con PROFESOR",
        [E("ALUMNO", [K("nia"), A("nombre")]), E("MODULO", [K("cod_modulo"), A("nombre")]),
         E("PROFESOR", [K("dni"), A("nombre")])],
        [R("cursa", [("ALUMNO", "(0,N)", None), ("MODULO", "(1,N)", None)], [A("fecha_mat")]),
         R("evalua", [("MATRICULA", "(0,N)", None), ("PROFESOR", "(0,1)", None)])],
        aggs=[AGG("MATRICULA", ["ALUMNO", "MODULO", "cursa"])],
        pos={"ALUMNO": (0, 0.6), "cursa": (2.2, 0.6), "MODULO": (4.4, 0.6), "evalua": (2.2, 2.6), "PROFESOR": (2.2, 3.9)}),
}

if __name__ == "__main__":
    solo = sys.argv[1:]
    for nombre, modelo in M.items():
        if solo and nombre not in solo:
            continue
        print(nombre, draw(modelo, os.path.join(OUT, nombre + ".svg"), 8))
