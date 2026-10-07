"""Soluciones de las prácticas 2.7–2.32 de la UD02 en notación de Chen (EER)."""
from chen import Diagram

SPECS = {}
def spec(num):
    def deco(f):
        SPECS[num] = f
        return f
    return deco

def D(num, title, **kw):
    return Diagram(f"2-{num:02d}", title=title, **kw)

# ───────────── NIVEL 1 ─────────────
@spec(7)
def p07():
    d = D(7, "Ventas: clientes, productos y proveedores")
    d.entity("CLIENTE", ["*dni", "nombre", "apellidos", "dirección", "fecha_nacimiento"], pos=(0, 0))
    d.relation("COMPRA", [("CLIENTE", "(0,N)"), ("PRODUCTO", "(0,N)")], attrs=["*fecha", "unidades"], pos=(1, 0))
    d.entity("PRODUCTO", ["*código", "nombre", "precio_unitario"], pos=(2, 0))
    d.relation("SUMINISTRA", [("PROVEEDOR", "(1,1)"), ("PRODUCTO", "(0,N)")], pos=(2, 1))
    d.entity("PROVEEDOR", ["*nif", "nombre", "dirección"], pos=(2, 2))
    return d

@spec(8)
def p08():
    d = D(8, "Multas de tráfico")
    d.entity("PROPIETARIO", ["*dni", "nombre", "apellidos", "dirección"], pos=(0, 0))
    d.relation("POSEE", [("PROPIETARIO", "(1,1)"), ("VEHÍCULO", "(1,N)")], pos=(1, 0))
    d.entity("VEHÍCULO", ["*matrícula", "tipo", "marca", "modelo"], pos=(2, 0))
    d.relation("MULTA", [("VEHÍCULO", "(0,N)"), ("INFRACCIÓN", "(0,N)")], attrs=["*fecha_sanción", "fecha_pago"], pos=(2, 1))
    d.entity("INFRACCIÓN", ["*código", "descripción", "cuantía"], pos=(2, 2))
    return d

@spec(9)
def p09():
    d = D(9, "Naviera: capitanes, barcos y contenedores")
    d.entity("CAPITÁN", ["*dni", "nombre", "teléfono", "dirección", "salario", "población"], pos=(0, 0))
    d.relation("GOBIERNA", [("CAPITÁN", "(0,N)"), ("BARCO", "(0,N)")], attrs=["*fecha_inicio", "fecha_fin"], pos=(1, 0))
    d.entity("BARCO", ["*matrícula", "nombre", "potencia_motor", "astillero"], pos=(2, 0))
    d.relation("TRANSPORTA", [("CAPITÁN", "(1,1)"), ("CONTENEDOR", "(0,N)")], pos=(0, 1))
    d.entity("CONTENEDOR", ["*código", "descripción", "dir_remitente", "dir_destinatario"], pos=(0, 2))
    d.relation("TIENE DESTINO", [("PUERTO", "(1,1)"), ("CONTENEDOR", "(0,N)")], pos=(1, 2))
    d.entity("PUERTO", ["*código", "nombre"], pos=(2, 2))
    return d

@spec(10)
def p10():
    d = D(10, "Instituto: profesores, módulos, alumnos y casilleros")
    d.entity("PROFESOR", ["*dni", "nombre", "dirección", "teléfono"], pos=(0, 0))
    d.relation("IMPARTE", [("PROFESOR", "(1,1)"), ("MÓDULO", "(0,N)")], pos=(1, 0))
    d.entity("MÓDULO", ["*código", "nombre"], pos=(2, 0))
    d.relation("MATRÍCULA", [("ALUMNO", "(0,N)"), ("MÓDULO", "(1,N)")], attrs=["fecha_matrícula"], pos=(2, 1))
    d.entity("ALUMNO", ["*nº_expediente", "nombre", "apellidos", "fecha_nacimiento"], pos=(2, 2))
    d.relation("TIENE ASIGNADO", [("ALUMNO", "(1,1)"), ("CASILLERO", "(0,1)")], pos=(1, 2))
    d.entity("CASILLERO", ["*número", "tamaño_m"], pos=(0, 2))
    return d

# ───────────── NIVEL 2 ─────────────
@spec(11)
def p11():
    d = D(11, "Hospital: ingresos de pacientes")
    d.entity("PACIENTE", ["*código", "nombre", "apellidos", "dirección{calle,población,provincia,código_postal}",
                          "teléfono", "fecha_nacimiento", "/edad"], pos=(0, 0))
    d.relation("INGRESA", [("PACIENTE", "(1,1)"), ("INGRESO", "(0,N)")], identifying=True, pos=(1.2, 0))
    d.entity("INGRESO", ["~nº_ingreso", "habitación", "cama", "fecha_ingreso", "fecha_alta"], weak=True, pos=(2.4, 0))
    d.relation("ATIENDE", [("MÉDICO", "(1,1)"), ("INGRESO", "(0,N)")], pos=(2.4, 1.2))
    d.entity("MÉDICO", ["*código", "nombre", "apellidos", "teléfono", "especialidad"], pos=(2.4, 2.4))
    return d

@spec(12)
def p12():
    d = D(12, "Parentesco familiar")
    d.entity("PERSONA", ["*dni", "nombre", "dirección{calle,número,ciudad}", "+teléfono", "fecha_nacimiento", "/edad"], pos=(0, 0))
    d.relation("ES PROGENITOR DE", [("PERSONA", "(0,2)", "progenitor"), ("PERSONA", "(0,N)", "hijo/a")], pos=(1.3, 0))
    return d

@spec(13)
def p13():
    d = D(13, "Concesionario: ventas y revisiones")
    d.entity("CLIENTE", ["*cód_cliente", "nif", "nombre", "dirección", "ciudad", "teléfono"], pos=(0, 0))
    d.relation("COMPRA", [("CLIENTE", "(0,1)"), ("COCHE", "(0,N)")], pos=(1, 0))
    d.entity("COCHE", ["*matrícula", "marca", "modelo", "color", "precio_venta"], pos=(2, 0))
    d.relation("TIENE", [("COCHE", "(1,1)"), ("REVISIÓN", "(0,N)")], identifying=True, pos=(2, 1))
    d.entity("REVISIÓN", ["~nº_revisión", "cambio_filtro", "cambio_aceite", "cambio_frenos", "otros"], weak=True, pos=(2, 2))
    d.relation("REALIZA", [("MÉDICO_", "(1,1)"), ("REVISIÓN", "(0,N)")], pos=(1, 2)) if False else None
    d.relation("REALIZA", [("MECÁNICO", "(1,1)"), ("REVISIÓN", "(0,N)")], pos=(1, 2))
    d.entity("MECÁNICO", ["*cód_empleado", "dni", "nombre", "teléfono", "dirección"], pos=(0, 2))
    d.relation("SUPERVISA", [("MECÁNICO", "(0,1)", "supervisor"), ("MECÁNICO", "(0,N)", "supervisado")], pos=(0, 3.4))
    return d

@spec(14)
def p14():
    d = D(14, "Centro de menores: seguimiento")
    d.entity("MENOR", ["*nº_expediente", "nombre", "apellidos", "fecha_nacimiento",
                       "datos_tutores{nombre_padre,nombre_madre,teléfono}"], pos=(0, 0))
    d.relation("TIENE", [("MENOR", "(1,1)"), ("INFORME", "(0,N)")], identifying=True, pos=(1.2, 0))
    d.entity("INFORME", ["~nº_informe", "fecha", "valoración", "incidencias"], weak=True, pos=(2.4, 0))
    d.relation("TUTELA", [("EDUCADOR", "(1,1)"), ("MENOR", "(0,N)")], pos=(0, 1.3))
    d.entity("EDUCADOR", ["*nº_colegiado", "dni", "nombre", "apellidos", "especialidad"], pos=(0, 2.6))
    d.relation("COORDINA", [("EDUCADOR", "(0,1)", "coordinador"), ("EDUCADOR", "(0,N)", "coordinado")], pos=(1.4, 2.6))
    return d

@spec(15)
def p15():
    d = D(15, "Consultora de software")
    d.entity("CLIENTE", ["*cif", "razón_social", "web", "teléfono"], pos=(0, 0))
    d.relation("ENCARGA", [("CLIENTE", "(1,1)"), ("PROYECTO", "(0,N)")], pos=(1, 0))
    d.entity("PROYECTO", ["*código", "nombre", "fecha_inicio", "presupuesto"], pos=(2, 0))
    d.relation("SE DESCOMPONE EN", [("PROYECTO", "(1,1)"), ("TAREA", "(1,N)")], identifying=True, pos=(2, 1.2))
    d.entity("TAREA", ["~nº_tarea", "descripción", "horas_estimadas", "estado"], weak=True, pos=(2, 2.4))
    d.relation("TRABAJA EN", [("DESARROLLADOR", "(0,N)"), ("TAREA", "(0,N)")], attrs=["*fecha", "horas_reales"], pos=(1, 2.4))
    d.entity("DESARROLLADOR", ["*nº_empleado", "dni", "nombre", "especialidad", "nivel"], pos=(0, 2.4))
    d.relation("TUTELA", [("DESARROLLADOR", "(0,1)", "mentor"), ("DESARROLLADOR", "(0,N)", "júnior")], pos=(0, 3.8))
    return d

@spec(16)
def p16():
    d = D(16, "Cadena hotelera: reservas")
    d.entity("HOTEL", ["*código", "nombre", "estrellas", "dirección", "ciudad"], pos=(0, 0))
    d.relation("DISPONE DE", [("HOTEL", "(1,1)"), ("HABITACIÓN", "(1,N)")], identifying=True, pos=(1, 0))
    d.entity("HABITACIÓN", ["~número", "tipo", "precio_noche"], weak=True, pos=(2, 0))
    d.relation("RESERVA", [("CLIENTE", "(0,N)"), ("HABITACIÓN", "(0,N)")], attrs=["*fecha_entrada", "fecha_salida", "precio_total"], pos=(2, 1.2))
    d.entity("CLIENTE", ["*dni", "nombre", "email", "teléfono"], pos=(2, 2.4))
    d.relation("TRABAJA EN", [("HOTEL", "(1,1)"), ("EMPLEADO", "(1,N)")], pos=(0, 1.2))
    d.entity("EMPLEADO", ["*código", "nombre", "puesto"], pos=(0, 2.4))
    d.relation("SUPERVISA", [("EMPLEADO", "(0,1)", "gobernanta"), ("EMPLEADO", "(0,N)", "personal de limpieza")], pos=(1.1, 2.4))
    return d

@spec(17)
def p17():
    d = D(17, "Red de gimnasios")
    d.entity("GIMNASIO", ["*código", "nombre", "dirección", "ciudad", "superficie_m2"], pos=(0, 0))
    d.relation("DISPONE DE", [("GIMNASIO", "(1,1)"), ("SALA", "(1,N)")], identifying=True, pos=(1, 0))
    d.entity("SALA", ["~nº_sala", "tipo_actividad", "aforo"], weak=True, pos=(2, 0))
    d.relation("RESERVA", [("SOCIO", "(0,N)"), ("SALA", "(0,N)")], attrs=["*fecha", "*hora", "plaza"], pos=(2, 1.3))
    d.entity("SOCIO", ["*nº_socio", "dni", "nombre", "apellidos", "teléfono", "fecha_alta"], pos=(2, 2.6))
    d.relation("ESTÁ INSCRITO EN", [("GIMNASIO", "(1,1)"), ("SOCIO", "(0,N)")], pos=(1, 1.3))
    d.relation("DISEÑA RUTINA", [("ENTRENADOR", "(0,N)"), ("SOCIO", "(0,N)")], attrs=["*fecha_asignación", "objetivo"], pos=(1, 2.6))
    d.entity("ENTRENADOR", ["*cód_empleado", "nombre", "especialidad", "titulación"], pos=(0, 2.6))
    d.relation("TRABAJA EN", [("GIMNASIO", "(1,1)"), ("ENTRENADOR", "(1,N)")], pos=(0, 1.3))
    d.relation("DIRIGE", [("ENTRENADOR", "(0,1)", "director técnico"), ("ENTRENADOR", "(0,N)", "entrenador")], pos=(0, 4.0))
    return d

@spec(18)
def p18():
    d = D(18, "Tienda online", colw=215, rowh=170)
    d.entity("CATEGORÍA", ["*código", "nombre"], pos=(0, 0))
    d.relation("SUBCATEGORÍA DE", [("CATEGORÍA", "(0,1)", "padre"), ("CATEGORÍA", "(0,N)", "hija")], pos=(0, 1.4))
    d.relation("PERTENECE A", [("CATEGORÍA", "(1,1)"), ("PRODUCTO", "(0,N)")], pos=(1, 0))
    d.entity("PRODUCTO", ["*sku", "nombre", "descripción", "precio", "stock"], pos=(2, 0))
    d.relation("VALORA", [("CLIENTE", "(0,N)"), ("PRODUCTO", "(0,N)")], attrs=["puntuación", "comentario"], pos=(3, 0.5))
    d.entity("CLIENTE", ["*email", "nombre", "contraseña_hash", "+teléfono"], pos=(4, 1))
    d.relation("CONTIENE", [("PEDIDO", "(0,N)"), ("PRODUCTO", "(1,N)")], attrs=["cantidad", "precio_unitario"], pos=(2, 1.2))
    d.entity("PEDIDO", ["*nº_pedido", "fecha", "estado"], pos=(2, 2.4))
    d.relation("REALIZA", [("CLIENTE", "(1,1)"), ("PEDIDO", "(0,N)")], pos=(3, 1.7))
    d.relation("TIENE", [("CLIENTE", "(1,1)"), ("DIRECCIÓN", "(0,N)")], identifying=True, pos=(4, 2.2))
    d.entity("DIRECCIÓN", ["~alias", "calle", "número", "código_postal", "ciudad", "país"], weak=True, pos=(4, 3.4))
    d.relation("SE ENVÍA A", [("DIRECCIÓN", "(1,1)"), ("PEDIDO", "(0,N)")], pos=(3, 3.4))
    return d

@spec(19)
def p19():
    d = D(19, "Club de pádel: reservas de pistas")
    d.entity("PISTA", ["*código", "superficie", "cubierta"], pos=(0, 0))
    d.relation("TIENE", [("PISTA", "(1,1)"), ("RESERVA", "(0,N)")], identifying=True, pos=(1, 0))
    d.entity("RESERVA", ["~fecha", "~hora_inicio", "importe"], weak=True, pos=(2, 0))
    d.relation("RESPONSABLE DE", [("SOCIO", "(1,1)"), ("RESERVA", "(0,N)")], pos=(1.4, 1.3))
    d.relation("JUEGA EN", [("SOCIO", "(2,4)"), ("RESERVA", "(0,N)")], attrs=["importe_pagado"], pos=(2.8, 1.3))
    d.entity("SOCIO", ["*nº_socio", "dni", "nombre", "+teléfono", "fecha_alta"], pos=(2, 2.6))
    return d

@spec(20)
def p20():
    d = D(20, "Alquiler de vehículos con jerarquías", colw=215, rowh=165)
    d.entity("TURISMO", ["plazas", "tipo_cambio"], pos=(0, 0))
    d.entity("FURGONETA", ["carga_útil_kg", "volumen_m3"], pos=(1.3, 0))
    d.entity("MOTOCICLETA", ["cilindrada"], pos=(2.6, 0))
    d.specialization("VEHÍCULO", ["TURISMO", "FURGONETA", "MOTOCICLETA"], "d", total=True, pos=(1.3, 0.8), sid="S1")
    d.entity("VEHÍCULO", ["*matrícula", "marca", "modelo", "fecha_matriculación", "kilometraje", "tarifa_diaria"], pos=(1.3, 1.8))
    d.specialization("VEHÍCULO", ["ELÉCTRICO", "HÍBRIDO"], "d", total=False, pos=(3.0, 1.8), sid="S2")
    d.entity("ELÉCTRICO", ["autonomía_km", "tipo_conector"], pos=(4.2, 1.2))
    d.entity("HÍBRIDO", ["capacidad_batería_kwh"], pos=(4.2, 2.5))
    d.relation("SOBRE", [("VEHÍCULO", "(1,1)"), ("ALQUILER", "(0,N)")], pos=(1.3, 2.9))
    d.entity("ALQUILER", ["*nº_contrato", "fecha_inicio", "fecha_fin_prevista", "fecha_devolución", "km_inicial", "km_final", "importe"], pos=(1.3, 4.0))
    d.relation("FIRMA", [("CLIENTE", "(1,1)"), ("ALQUILER", "(0,N)")], pos=(1.3, 5.2))
    d.entity("CLIENTE", ["*nif", "nombre", "nº_carnet", "caducidad_carnet", "teléfono"], pos=(1.3, 6.4))
    d.relation("RECOGIDA EN", [("SUCURSAL", "(1,1)"), ("ALQUILER", "(0,N)")], pos=(0.1, 3.5))
    d.relation("DEVOLUCIÓN EN", [("SUCURSAL", "(0,1)"), ("ALQUILER", "(0,N)")], pos=(0.1, 4.6))
    d.entity("SUCURSAL", ["*código", "nombre", "ciudad", "dirección"], pos=(-1.3, 4.0))
    return d


# ───────────── NIVEL 3 ─────────────
@spec(21)
def p21():
    d = D(21, "Autobuses urbanos", colw=230, rowh=175)
    d.entity("LÍNEA", ["*código", "trayecto", "frecuencia_min"], pos=(0, 0))
    d.relation("TIENE PARADA", [("LÍNEA", "(1,1)"), ("PARADA", "(2,N)")], identifying=True, pos=(1.2, 0))
    d.entity("PARADA", ["~nº_orden", "ubicación", "pantalla_digital"], weak=True, pos=(2.4, 0))
    d.relation("TRANSBORDO", [("PARADA", "(0,N)", "origen"), ("PARADA", "(0,N)", "destino")], attrs=["tiempo_a_pie_min"], pos=(4.0, 0))
    d.relation("TURNO", [("CONDUCTOR", "N"), ("AUTOBÚS", "M"), ("LÍNEA", "P")], attrs=["*fecha", "*turno"], pos=(1.2, 2.0))
    d.entity("CONDUCTOR", ["*dni", "nombre", "tipo_licencia"], pos=(0, 3.4))
    d.entity("AUTOBÚS", ["*matrícula", "modelo", "capacidad_de_pie"], pos=(2.4, 3.4))
    return d

@spec(22)
def p22():
    d = D(22, "Federación deportiva: partidos e incidencias", colw=230, rowh=175)
    d.entity("EQUIPO", ["*código", "club", "ciudad"], pos=(1, 1))
    d.entity("PARTIDO", ["*código", "fecha_hora", "jornada"], pos=(3.6, 1))
    d.relation("LOCAL", [("EQUIPO", "(1,1)"), ("PARTIDO", "(0,N)")], pos=(2.3, 0.1))
    d.relation("VISITANTE", [("EQUIPO", "(1,1)"), ("PARTIDO", "(0,N)")], pos=(2.3, 1.9))
    d.entity("JUGADOR", ["*nº_ficha", "dni", "nombre", "dorsal"], pos=(1, 3.7))
    d.relation("PERTENECE A", [("EQUIPO", "(1,1)"), ("JUGADOR", "(1,N)")], pos=(0.2, 2.4))
    d.relation("ES CAPITÁN DE", [("JUGADOR", "(1,1)"), ("EQUIPO", "(0,1)")], pos=(1.8, 2.5))
    d.relation("REGISTRA", [("PARTIDO", "(1,1)"), ("INCIDENCIA", "(0,N)")], identifying=True, pos=(3.6, 2.4))
    d.entity("INCIDENCIA", ["~nº_secuencia", "minuto", "tipo"], weak=True, pos=(3.6, 3.7))
    d.relation("INTERVIENE", [("JUGADOR", "(1,N)"), ("INCIDENCIA", "(0,N)")], attrs=["rol"], pos=(2.3, 3.7))
    return d

@spec(23)
def p23():
    d = D(23, "Planta industrial y lista de materiales", colw=230, rowh=175)
    d.entity("FÁBRICA", ["*código", "ubicación", "teléfono"], pos=(0, 0))
    d.relation("ALBERGA", [("FÁBRICA", "(1,1)"), ("LÍNEA DE MONTAJE", "(1,N)")], identifying=True, pos=(1.2, 0))
    d.entity("LÍNEA DE MONTAJE", ["~código_línea", "denominación"], weak=True, pos=(2.6, 0))
    d.relation("SE FABRICA EN", [("LÍNEA DE MONTAJE", "(0,1)"), ("PIEZA", "(0,N)")], pos=(2.6, 1.3))
    d.entity("PIEZA", ["*código", "nombre", "peso_g", "coste_estándar"], pos=(2.6, 2.6))
    d.relation("COMPONE", [("PIEZA", "(0,N)", "subpieza"), ("PIEZA", "(0,N)", "pieza ensamblada")], attrs=["cantidad"], pos=(4.3, 2.6))
    d.relation("INSPECCIONADA", [("PIEZA", "(1,1)"), ("INFORME DE INSPECCIÓN", "(0,N)")], identifying=True, pos=(1.2, 2.6))
    d.entity("INFORME DE INSPECCIÓN", ["~nº_inspección", "fecha", "resultado", "observaciones"], weak=True, pos=(0, 2.6))
    d.relation("REDACTA", [("INSPECTOR", "(1,1)"), ("INFORME DE INSPECCIÓN", "(0,N)")], pos=(0, 3.9))
    d.entity("INSPECTOR", ["*cód_inspector", "nombre"], pos=(0, 5.2))
    return d

@spec(24)
def p24():
    d = D(24, "Universidad: departamentos, cátedras y profesorado", colw=215, rowh=170)
    d.entity("FACULTAD", ["*código", "nombre"], pos=(0, 0))
    d.relation("INTEGRA", [("FACULTAD", "(1,1)"), ("DEPARTAMENTO", "(1,N)")], pos=(1, 0))
    d.entity("DEPARTAMENTO", ["*código", "área_conocimiento"], pos=(2, 0))
    d.relation("CREA", [("DEPARTAMENTO", "(1,1)"), ("CÁTEDRA", "(0,N)")], identifying=True, pos=(3.2, 0))
    d.entity("CÁTEDRA", ["~nº_cátedra", "nombre", "presupuesto"], weak=True, pos=(4.4, 0))
    d.relation("DIRIGE", [("CATEDRÁTICO", "(1,1)"), ("CÁTEDRA", "(0,1)")], pos=(4.4, 1.3))
    d.entity("CATEDRÁTICO", ["año_cátedra"], pos=(4.4, 2.6))
    d.relation("PERTENECE A", [("DEPARTAMENTO", "(1,1)"), ("PROFESOR", "(1,N)")], pos=(2, 1.5))
    d.entity("PROFESOR", ["*nº_registro", "dni", "nombre", "fecha_incorporación"], pos=(2, 3.1))
    d.specialization("PROFESOR", ["CATEDRÁTICO", "TITULAR", "ASOCIADO"], "d", total=True, pos=(3.3, 3.1), sid="S1")
    d.entity("TITULAR", ["sexenios"], pos=(4.4, 3.8))
    d.entity("ASOCIADO", ["empresa_origen"], pos=(4.4, 4.9))
    d.relation("TUTELA", [("PROFESOR", "(0,1)", "tutor"), ("PROFESOR", "(0,N)", "tutorizado")], pos=(0.5, 3.1))
    return d

@spec(25)
def p25():
    d = D(25, "Ingeniería: agregación de la asignación", colw=230, rowh=175)
    d.entity("EMPLEADO", ["*nº_empleado", "nombre", "categoría"], pos=(0, 1))
    d.relation("TRABAJA EN", [("EMPLEADO", "(0,N)"), ("PROYECTO", "(1,N)")], attrs=["fecha_incorporación", "horas_semana"], pos=(1.4, 1))
    d.entity("PROYECTO", ["*código", "nombre", "presupuesto"], pos=(2.8, 1))
    d.aggregate("ASIGNACIÓN", ["EMPLEADO", "TRABAJA EN", "PROYECTO"], "ASIGNACIÓN (agregación)")
    d.relation("SUPERVISA", [("SUPERVISOR", "(0,N)"), ("ASIGNACIÓN", "(0,1)")], attrs=["fecha_revisión", "valoración"], pos=(0.2, 3.7))
    d.entity("SUPERVISOR", ["*cód_supervisor", "nombre"], pos=(0.2, 5.0))
    d.relation("REQUIERE", [("EQUIPO", "(0,N)"), ("ASIGNACIÓN", "(0,N)")], attrs=["cantidad"], pos=(2.6, 3.7))
    d.entity("EQUIPO", ["*cód_equipo", "descripción"], pos=(2.6, 5.0))
    return d

@spec(26)
def p26():
    d = D(26, "Muestra gastronómica de platos españoles", colw=215, rowh=165)
    d.entity("PROVINCIA", ["*nombre", "extensión", "capital"], pos=(0, 2))
    d.relation("CONTIENE", [("PROVINCIA", "(1,1)"), ("LOCALIDAD", "(1,N)")], identifying=True, pos=(1, 2))
    d.entity("LOCALIDAD", ["~nombre", "tamaño", "habitantes"], weak=True, pos=(2, 2))
    d.relation("ORGANIZA", [("LOCALIDAD", "(1,1)"), ("VISITA", "(0,N)")], identifying=True, pos=(2, 0.7))
    d.entity("VISITA", ["~lugar"], weak=True, pos=(2, -0.6))
    d.specialization("VISITA", ["CULTURAL", "INDUSTRIAL"], "d", total=True, pos=(3.2, -0.6), sid="S1")
    d.entity("CULTURAL", ["horario"], pos=(4.4, -1.4))
    d.entity("INDUSTRIAL", ["persona_contacto", "teléfono"], pos=(4.4, 0.2))
    d.relation("UBICA", [("LOCALIDAD", "(1,1)"), ("RESTAURANTE", "(0,N)")], identifying=True, pos=(2, 3.3))
    d.entity("RESTAURANTE", ["~nombre", "dirección", "teléfono", "precio_menú", "aforo"], weak=True, pos=(2, 4.6))
    d.relation("ES TÍPICO DE", [("PLATO", "(0,N)"), ("LOCALIDAD", "(1,N)")], attrs=["variaciones_locales"], pos=(3.2, 2))
    d.entity("PLATO", ["*nombre", "ingredientes_básicos", "preparación"], pos=(4.4, 2))
    d.relation("ESPECIALIZADO EN", [("RESTAURANTE", "(0,N)"), ("PLATO", "(1,N)")], pos=(3.3, 3.4))
    d.relation("ACONSEJA", [("PLATO", "(0,N)"), ("VINO", "(1,N)")], pos=(4.4, 3.4))
    d.entity("VINO", ["*código", "cosecha", "grado", "color", "textura"], pos=(4.4, 4.8))
    d.relation("OFRECE", [("BODEGA", "(1,1)"), ("VINO", "(1,N)")], pos=(4.4, 6.0))
    d.entity("BODEGA", ["*cif", "director", "sede", "teléfono"], pos=(4.4, 7.2))
    return d

@spec(27)
def p27():
    d = D(27, "Repostería PAVA S.A.", colw=230, rowh=175)
    d.entity("INGREDIENTE", ["*nombre", "vitamina_A", "vitamina_B", "vitamina_C", "calorías", "coste_kg"], pos=(0, 1.3))
    d.relation("COMPUESTO POR", [("PRODUCTO", "(0,N)"), ("INGREDIENTE", "(1,N)")], attrs=["porcentaje"], pos=(1.2, 1.3))
    d.entity("PRODUCTO", ["*nombre_comercial"], pos=(2.4, 1.3))
    d.relation("SE PARECE A", [("PRODUCTO", "(1,1)"), ("PRODUCTO COMPETIDOR", "(0,N)")], pos=(2.4, 0.0))
    d.entity("PRODUCTO COMPETIDOR", ["*nombre_comercial", "marca", "año_lanzamiento"], pos=(2.4, -1.3))
    d.relation("SE VENDE EN", [("PRODUCTO", "(1,1)"), ("FORMATO", "(1,N)")], identifying=True, pos=(3.6, 1.3))
    d.entity("FORMATO", ["~peso_g", "precio_venta"], weak=True, pos=(4.8, 1.3))
    d.relation("PROMOCIONA", [("PROMOCIÓN", "(0,N)"), ("FORMATO", "(1,N)")], attrs=["cantidad_máxima"], pos=(4.8, 0.0))
    d.entity("PROMOCIÓN", ["*tipo", "fecha_inicio", "fecha_fin"], pos=(4.8, -1.3))
    d.relation("SOLICITA", [("PEDIDO", "(0,N)"), ("FORMATO", "(1,N)")], attrs=["unidades"], pos=(4.8, 2.6))
    d.entity("PEDIDO", ["*nº_pedido", "fecha"], pos=(4.8, 3.9))
    d.relation("REALIZA", [("CLIENTE", "(1,1)"), ("PEDIDO", "(0,N)")], pos=(3.5, 3.9))
    d.entity("CLIENTE", ["*cif", "nombre", "dirección", "población", "provincia", "teléfono"], pos=(2.2, 3.9))
    return d

@spec(28)
def p28():
    d = D(28, "Comandancia de Starship Troopers", colw=230, rowh=175)
    d.entity("TROOPER", ["*nº_placa", "dni", "nombre", "categoría"], pos=(1.2, 1.5))
    d.relation("JEFE DE", [("TROOPER", "(0,1)", "jefe"), ("TROOPER", "(0,N)", "subordinado")], pos=(-0.2, 1.5))
    d.relation("USA", [("TROOPER", "(0,N)"), ("ARMA", "(0,N)")], attrs=["habilidad"], pos=(1.2, 2.9))
    d.entity("ARMA", ["*código", "clase", "nombre"], pos=(1.2, 4.2))
    d.relation("DETIENE", [("TROOPER", "(1,N)"), ("BICHO", "(0,N)")], attrs=["*fecha_detención"], pos=(2.6, 1.5))
    d.entity("BICHO", ["*id", "raza", "origen", "peso"], pos=(4.0, 1.5))
    d.relation("ENCIERRA", [("MAZMORRA", "(0,1)"), ("BICHO", "(0,4)")], pos=(4.0, 0.2))
    d.entity("MAZMORRA", ["*código", "ubicación"], pos=(4.0, -1.1))
    d.relation("IMPUTADO", [("BICHO", "(1,N)"), ("DELITO", "(0,N)")], attrs=["cargo_principal"], pos=(4.0, 2.8))
    d.entity("DELITO", ["*nº_asalto", "juzgado"], pos=(4.0, 4.1))
    d.relation("INVESTIGA", [("TROOPER", "(1,N)"), ("DELITO", "(0,N)")], pos=(2.6, 4.1))
    return d

@spec(29)
def p29():
    d = D(29, "Seguridad bancaria, vigilantes y atracos", colw=215, rowh=170)
    d.entity("ENTIDAD BANCARIA", ["*código", "dirección_sede"], pos=(0, 0))
    d.relation("TIENE", [("ENTIDAD BANCARIA", "(1,1)"), ("SUCURSAL", "(1,N)")], pos=(1, 0))
    d.entity("SUCURSAL", ["*código_sucursal", "dirección", "nº_empleados"], pos=(2, 0))
    d.relation("CONTRATA", [("SUCURSAL", "(0,N)"), ("VIGILANTE", "(1,N)")], attrs=["*fecha_contrato", "con_arma"], pos=(2, 1.4))
    d.entity("VIGILANTE", ["*cód_vigilante", "dni", "nombre", "fecha_nacimiento", "/edad"], pos=(2, 2.8))
    d.specialization("VIGILANTE", ["ARMADO", "NO ARMADO"], "d", total=True, pos=(3.2, 2.8), sid="S1")
    d.entity("ARMADO", ["puntuación_tiro", "calibre"], pos=(4.4, 2.2))
    d.entity("NO ARMADO", ["artes_marciales"], pos=(4.4, 3.5))
    d.relation("ATRACO", [("SUCURSAL", "N"), ("DETENIDO", "M"), ("JUEZ", "P")], attrs=["*fecha", "condena_años", "indemnización"], pos=(3.7, 0))
    d.entity("JUEZ", ["*clave_juzgado", "nombre", "años_servicio"], pos=(3.7, -1.5))
    d.entity("DETENIDO", ["*código", "nombre_completo"], pos=(5.4, 0))
    d.relation("ES MIEMBRO DE", [("BANDA", "(0,1)"), ("DETENIDO", "(1,N)")], pos=(5.4, 1.4))
    d.entity("BANDA", ["*nº_banda", "/nº_miembros"], pos=(5.4, 2.8))
    d.relation("SUBORDINADA A", [("BANDA", "(0,1)", "matriz"), ("BANDA", "(0,N)", "subordinada")], pos=(5.4, 4.3))
    return d

@spec(30)
def p30():
    d = D(30, "Balneario: huéspedes, habitaciones y tratamientos", colw=195, rowh=160)
    d.entity("CLIENTE", ["*dni", "nombre", "apellidos", "fecha_nacimiento"], pos=(1.2, 0))
    d.specialization("CLIENTE", ["ALOJADO", "AMBULANTE"], "d", total=True, pos=(1.2, 1.1), sid="S1")
    d.entity("ALOJADO", ["tarjeta_crédito", "fecha_salida_prevista"], pos=(0, 2.2))
    d.entity("AMBULANTE", ["teléfono_emergencia"], pos=(2.4, 2.2))
    d.relation("RESERVA", [("ALOJADO", "(0,N)"), ("HABITACIÓN", "(1,N)")], attrs=["fecha_asignación"], pos=(0, 3.5))
    d.entity("HABITACIÓN", ["~nº_habitación", "capacidad"], weak=True, pos=(0, 4.8))
    d.specialization("HABITACIÓN", ["SUITE", "ESTÁNDAR"], "d", total=True, pos=(1.3, 4.8), sid="S2")
    d.entity("SUITE", ["nº_jacuzzis", "m2"], pos=(2.5, 4.2))
    d.entity("ESTÁNDAR", ["cama_supletoria", "tipo_baño"], pos=(2.5, 5.5))
    d.relation("TIENE", [("PLANTA", "(1,1)"), ("HABITACIÓN", "(1,N)")], identifying=True, pos=(0, 6.1))
    d.entity("PLANTA", ["*nº_planta", "nombre", "/nº_habitaciones"], pos=(0, 7.4))
    d.relation("SESIÓN", [("CLIENTE", "N"), ("TERAPEUTA", "M"), ("TRATAMIENTO", "P")], attrs=["*fecha", "*hora", "duración_min", "observaciones"], pos=(3.2, 0))
    d.entity("TRATAMIENTO", ["*cód_tratamiento", "nombre"], pos=(3.2, -1.5))
    d.entity("TERAPEUTA", ["especialidad"], pos=(5.0, 0))
    d.relation("SUPERVISA", [("TERAPEUTA", "(0,1)", "sénior"), ("TERAPEUTA", "(0,N)", "júnior")], pos=(6.4, 0))
    d.specialization("EMPLEADO", ["TERAPEUTA"], "", total=False, pos=(5.0, 1.1), sid="S3")
    d.entity("EMPLEADO", ["*código", "nombre", "puesto"], pos=(5.0, 2.2))
    return d

@spec(31)
def p31():
    d = D(31, "Red de producción y distribución de energía eléctrica", colw=215, rowh=170)
    d.entity("CENTRAL", ["*código", "nombre", "producción_media", "fecha_puesta_en_marcha"], pos=(1.4, 1.5))
    d.relation("REGISTRA", [("CENTRAL", "(1,1)"), ("PARTE DE MANTENIMIENTO", "(0,N)")], identifying=True, pos=(0.1, 1.5))
    d.entity("PARTE DE MANTENIMIENTO", ["~nº_incidencia", "fecha_revisión", "empresa_mantenedora", "coste"], weak=True, pos=(-1.3, 1.5))
    d.specialization("CENTRAL", ["HIDROELÉCTRICA", "TÉRMICA O NUCLEAR", "RENOVABLE"], "d", total=True, pos=(1.4, 2.7), sid="S1")
    d.entity("HIDROELÉCTRICA", ["río", "embalse", "volumen_útil"], pos=(0, 4.0))
    d.entity("TÉRMICA O NUCLEAR", ["combustible", "emisiones"], pos=(1.4, 4.0))
    d.entity("RENOVABLE", ["nº_generadores", "superficie_captación"], pos=(2.8, 4.0))
    d.relation("CONTRATO", [("CENTRAL", "N"), ("COMERCIALIZADORA", "M"), ("ZONA", "P")], attrs=["*fecha", "mwh_contratados", "tarifa"], pos=(3.0, 1.5))
    d.entity("COMERCIALIZADORA", ["*cif", "nombre"], pos=(4.4, 0.4))
    d.entity("ZONA", ["*cód_zona", "nombre"], pos=(4.4, 2.6))
    d.entity("NODO", ["*código_nodo", "tipo"], pos=(1.4, -1.4))
    d.relation("LÍNEA DE TRANSMISIÓN", [("NODO", "(0,N)", "extremo A"), ("NODO", "(0,N)", "extremo B")], attrs=["capacidad_kv", "distancia_km"], pos=(3.2, -1.4))
    return d

@spec(32)
def p32():
    d = D(32, "Club hípico: caballos, cuadras y lecciones", colw=190, rowh=165)
    d.entity("CABALLO", ["*microchip", "nombre", "raza", "fecha_nacimiento"], pos=(1.4, 2.0))
    d.relation("GENEALOGÍA", [("CABALLO", "(0,2)", "progenitor"), ("CABALLO", "(0,N)", "potro")], pos=(1.4, 0.4))
    d.specialization("CABALLO", ["PROPIO", "PRIVADO"], "d", total=True, pos=(1.4, 3.2), sid="S1")
    d.entity("PROPIO", ["fecha_adquisición", "coste_mensual"], pos=(0.2, 4.4))
    d.entity("PRIVADO", ["cuota_pupilaje"], pos=(2.6, 4.4))
    d.relation("PERTENECE A", [("SOCIO", "(1,1)"), ("PRIVADO", "(0,N)")], pos=(3.9, 4.4))
    d.entity("SOCIO", ["*nº_socio", "dni", "nombre"], pos=(5.2, 4.4))
    d.relation("OCUPA", [("CABALLO", "(0,1)"), ("BOX", "(0,1)")], pos=(-0.2, 2.0))
    d.entity("BOX", ["~nº_box"], weak=True, pos=(-1.6, 2.0))
    d.relation("DISPONE DE", [("PABELLÓN", "(1,1)"), ("BOX", "(1,N)")], identifying=True, pos=(-1.6, 0.7))
    d.entity("PABELLÓN", ["*código", "nombre"], pos=(-1.6, -0.6))
    d.relation("LECCIÓN", [("SOCIO", "N"), ("INSTRUCTOR", "M"), ("CABALLO", "P")], attrs=["*fecha", "*hora", "pista", "nivel"], pos=(3.4, 2.0))
    d.entity("INSTRUCTOR", ["*nº_colegiado", "dni", "nombre", "titulación"], pos=(5.2, 1.0))
    d.specialization("INSTRUCTOR", ["TITULAR", "EN PRÁCTICAS"], "d", total=True, pos=(5.2, -0.1), sid="S2")
    d.entity("TITULAR", ["antigüedad"], pos=(4.0, -1.2))
    d.entity("EN PRÁCTICAS", ["fecha_fin_prácticas"], pos=(6.4, -1.2))
    d.relation("TUTORIZA", [("TITULAR", "(0,N)"), ("EN PRÁCTICAS", "(1,1)")], pos=(5.2, -1.9))
    return d

@spec(0)
def leyenda():
    d = Diagram("2-leyenda", title="Leyenda de la notación de Chen EER", colw=240, rowh=175)
    d.entity("ALUMNO", ["*nia", "nombre", "+teléfono", "/edad", "dirección{calle,código_postal}"], pos=(0, 0))
    d.relation("SE MATRICULA", [("ALUMNO", "(0,N)"), ("MÓDULO", "(1,N)")], attrs=["fecha"], pos=(1.4, 0))
    d.entity("MÓDULO", ["*código", "nombre"], pos=(2.8, 0))
    d.relation("TIENE", [("MÓDULO", "(1,1)"), ("TEMA", "(1,N)")], identifying=True, pos=(2.8, 1.3))
    d.entity("TEMA", ["~nº_tema", "título"], weak=True, pos=(2.8, 2.6))
    d.entity("EMPLEADO", ["*dni", "nombre"], pos=(0, 2.6))
    d.specialization("EMPLEADO", ["FIJO", "TEMPORAL"], "d", total=True, pos=(1.4, 2.6), sid="S1")
    d.entity("FIJO", ["antigüedad"], pos=(2.2, 3.7)) if False else None
    d.entity("FIJO", ["antigüedad"], pos=(1.4, 3.9))
    d.entity("TEMPORAL", ["fecha_fin_contrato"], pos=(0, 3.9))
    return d
