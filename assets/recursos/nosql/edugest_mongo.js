// =====================================================================
// EduGest · versión documental para MongoDB 8.0 (UD10)
// Ejecutar con:  mongosh edugest_mongo.js
//           o:  docker exec -i mongo8 mongosh < edugest_mongo.js
// Mismos datos ficticios que el esquema relacional de Oracle (curso 2025-26).
// =====================================================================

db = db.getSiblingDB('edugest');

db.expedientes.drop();
db.ciclos.drop();
db.profesores.drop();

// Ciclos con sus módulos incrustados
db.ciclos.insertMany([
  {
    _id: "DAM",
    nombre: "Desarrollo de Aplicaciones Multiplataforma",
    grado: "SUPERIOR",
    horasTotales: 2000,
    modulos: [
      {
        codigo: "0373",
        nombre: "Lenguajes de marcas y sistemas de gestión de información",
        curso: 1,
        horas: 128
      },
      {
        codigo: "0483",
        nombre: "Sistemas informáticos",
        curso: 1,
        horas: 160
      },
      {
        codigo: "0484",
        nombre: "Bases de datos",
        curso: 1,
        horas: 160
      },
      {
        codigo: "0485",
        nombre: "Programación",
        curso: 1,
        horas: 256
      },
      {
        codigo: "0487",
        nombre: "Entornos de desarrollo",
        curso: 1,
        horas: 96
      },
      {
        codigo: "0486",
        nombre: "Acceso a datos",
        curso: 2,
        horas: 120
      },
      {
        codigo: "0488",
        nombre: "Desarrollo de interfaces",
        curso: 2,
        horas: 120
      },
      {
        codigo: "0489",
        nombre: "Programación multimedia y dispositivos móviles",
        curso: 2,
        horas: 100
      },
      {
        codigo: "0490",
        nombre: "Programación de servicios y procesos",
        curso: 2,
        horas: 80
      },
      {
        codigo: "0491",
        nombre: "Sistemas de gestión empresarial",
        curso: 2,
        horas: 100
      }
    ]
  },
  {
    _id: "DAW",
    nombre: "Desarrollo de Aplicaciones Web",
    grado: "SUPERIOR",
    horasTotales: 2000,
    modulos: [
      {
        codigo: "0373",
        nombre: "Lenguajes de marcas y sistemas de gestión de información",
        curso: 1,
        horas: 128
      },
      {
        codigo: "0483",
        nombre: "Sistemas informáticos",
        curso: 1,
        horas: 160
      },
      {
        codigo: "0484",
        nombre: "Bases de datos",
        curso: 1,
        horas: 160
      },
      {
        codigo: "0485",
        nombre: "Programación",
        curso: 1,
        horas: 256
      },
      {
        codigo: "0487",
        nombre: "Entornos de desarrollo",
        curso: 1,
        horas: 96
      },
      {
        codigo: "0612",
        nombre: "Desarrollo web en entorno cliente",
        curso: 2,
        horas: 140
      },
      {
        codigo: "0613",
        nombre: "Desarrollo web en entorno servidor",
        curso: 2,
        horas: 160
      },
      {
        codigo: "0614",
        nombre: "Despliegue de aplicaciones web",
        curso: 2,
        horas: 80
      },
      {
        codigo: "0615",
        nombre: "Diseño de interfaces web",
        curso: 2,
        horas: 120
      }
    ]
  },
  {
    _id: "ASIR",
    nombre: "Administración de Sistemas Informáticos en Red",
    grado: "SUPERIOR",
    horasTotales: 2000,
    modulos: [
      {
        codigo: "0369",
        nombre: "Implantación de sistemas operativos",
        curso: 1,
        horas: 224
      },
      {
        codigo: "0370",
        nombre: "Planificación y administración de redes",
        curso: 1,
        horas: 192
      },
      {
        codigo: "0371",
        nombre: "Fundamentos de hardware",
        curso: 1,
        horas: 96
      },
      {
        codigo: "0372",
        nombre: "Gestión de bases de datos",
        curso: 1,
        horas: 160
      },
      {
        codigo: "0373",
        nombre: "Lenguajes de marcas y sistemas de gestión de información",
        curso: 1,
        horas: 96
      }
    ]
  },
  {
    _id: "SMR",
    nombre: "Sistemas Microinformáticos y Redes",
    grado: "MEDIO",
    horasTotales: 2000,
    modulos: []
  }
]);

// Profesorado: el departamento se guarda como texto y la docencia incrustada
db.profesores.insertMany([
  {
    _id: 101,
    nombre: "Marta",
    apellidos: "Soler Ivars",
    email: "msoler@edugest.es",
    especialidad: "Informática",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2009-09-01"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1ASIR",
        modulo: "0372",
        horas: 5
      },
      {
        curso: "2025-26",
        grupo: "1DAM",
        modulo: "0484",
        horas: 5
      },
      {
        curso: "2025-26",
        grupo: "1DAW",
        modulo: "0484",
        horas: 5
      }
    ]
  },
  {
    _id: 102,
    nombre: "Javier",
    apellidos: "Pastor Gil",
    email: "jpastor@edugest.es",
    especialidad: "Sistemas y Aplicaciones Informáticas",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2012-09-01"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1ASIR",
        modulo: "0371",
        horas: 3
      },
      {
        curso: "2025-26",
        grupo: "1DAM",
        modulo: "0483",
        horas: 5
      },
      {
        curso: "2025-26",
        grupo: "1DAW",
        modulo: "0483",
        horas: 5
      },
      {
        curso: "2025-26",
        grupo: "2DAM",
        modulo: "0491",
        horas: 3
      }
    ]
  },
  {
    _id: 103,
    nombre: "Lucía",
    apellidos: "Ferrándiz Mora",
    email: "lferrandiz@edugest.es",
    especialidad: "Informática",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2015-09-01"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1DAM",
        modulo: "0485",
        horas: 8
      },
      {
        curso: "2025-26",
        grupo: "2DAM",
        modulo: "0486",
        horas: 4
      },
      {
        curso: "2025-26",
        grupo: "2DAM",
        modulo: "0490",
        horas: 2
      }
    ],
    tutorDe: "1DAM"
  },
  {
    _id: 104,
    nombre: "Andrés",
    apellidos: "Navarro Ruiz",
    email: "anavarro@edugest.es",
    especialidad: "Informática",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2018-09-03"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1DAM",
        modulo: "0487",
        horas: 3
      },
      {
        curso: "2025-26",
        grupo: "1DAW",
        modulo: "0487",
        horas: 3
      },
      {
        curso: "2025-26",
        grupo: "2DAM",
        modulo: "0488",
        horas: 4
      },
      {
        curso: "2025-26",
        grupo: "2DAW",
        modulo: "0613",
        horas: 5
      }
    ],
    tutorDe: "2DAM"
  },
  {
    _id: 105,
    nombre: "Elena",
    apellidos: "Brotons Sala",
    email: "ebrotons@edugest.es",
    especialidad: "Sistemas y Aplicaciones Informáticas",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2020-09-01"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1ASIR",
        modulo: "0369",
        horas: 7
      },
      {
        curso: "2025-26",
        grupo: "1ASIR",
        modulo: "0370",
        horas: 6
      },
      {
        curso: "2025-26",
        grupo: "2DAW",
        modulo: "0614",
        horas: 2
      }
    ],
    tutorDe: "1ASIR"
  },
  {
    _id: 106,
    nombre: "Raúl",
    apellidos: "Cano Vidal",
    email: "rcano@edugest.es",
    especialidad: "Informática",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2021-09-01"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1DAW",
        modulo: "0485",
        horas: 8
      },
      {
        curso: "2025-26",
        grupo: "2DAM",
        modulo: "0489",
        horas: 3
      },
      {
        curso: "2025-26",
        grupo: "2DAW",
        modulo: "0612",
        horas: 4
      }
    ],
    tutorDe: "1DAW"
  },
  {
    _id: 107,
    nombre: "Nuria",
    apellidos: "Gómez Pérez",
    email: "ngomez@edugest.es",
    especialidad: "Informática",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2023-09-01"),
    imparte: [
      {
        curso: "2025-26",
        grupo: "1ASIR",
        modulo: "0373",
        horas: 3
      },
      {
        curso: "2025-26",
        grupo: "1DAM",
        modulo: "0373",
        horas: 4
      },
      {
        curso: "2025-26",
        grupo: "1DAW",
        modulo: "0373",
        horas: 4
      },
      {
        curso: "2025-26",
        grupo: "2DAW",
        modulo: "0615",
        horas: 4
      }
    ],
    tutorDe: "2DAW"
  },
  {
    _id: 108,
    nombre: "Pablo",
    apellidos: "Lillo Martí",
    email: "plillo@edugest.es",
    especialidad: "Sistemas y Aplicaciones Informáticas",
    departamento: "Informática y Comunicaciones",
    fechaAlta: ISODate("2025-09-01")
  },
  {
    _id: 109,
    nombre: "Carmen",
    apellidos: "Ortiz Llorca",
    email: "cortiz@edugest.es",
    especialidad: "Formación y Orientación Laboral",
    departamento: "Formación y Orientación Laboral",
    fechaAlta: ISODate("2010-09-01")
  },
  {
    _id: 110,
    nombre: "Sergio",
    apellidos: "Ramos Climent",
    email: "sramos@edugest.es",
    especialidad: "Formación y Orientación Laboral",
    departamento: "Formación y Orientación Laboral",
    fechaAlta: ISODate("2019-09-02")
  },
  {
    _id: 111,
    nombre: "Laura",
    apellidos: "Vicent Ribes",
    email: "lvicent@edugest.es",
    especialidad: "Inglés",
    departamento: "Inglés",
    fechaAlta: ISODate("2016-09-01")
  },
  {
    _id: 112,
    nombre: "David",
    apellidos: "Esteve Juan",
    email: "desteve@edugest.es",
    especialidad: "Administración de Empresas",
    departamento: "Administración y Gestión",
    fechaAlta: ISODate("2024-09-02")
  }
]);

// Expedientes: un documento por alumno con sus matrículas y faltas incrustadas.
// Observa que los campos que no existen (dni, email, grupo, nota...) simplemente no aparecen.
db.expedientes.insertMany([
  {
    _id: 1,
    nia: "10450037",
    dni: "55568986C",
    nombre: "Adrián",
    apellidos: "Ferri Baeza",
    fechaNacimiento: ISODate("2006-10-18"),
    contacto: {
      email: "adrianferri1@alu.edugest.es",
      telefono: "610608088"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 8.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 4.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2026-02-04"),
            horas: 3,
            justificada: true
          },
          {
            fecha: ISODate("2026-03-19"),
            horas: 3,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 4.75,
        faltas: [
          {
            fecha: ISODate("2026-05-08"),
            horas: 2,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        nota: 6.75
      }
    ]
  },
  {
    _id: 2,
    nia: "10450074",
    dni: "44154098D",
    nombre: "Rubén",
    apellidos: "Iborra Ferri",
    fechaNacimiento: ISODate("2005-11-01"),
    contacto: {
      email: "rubeniborra2@alu.edugest.es",
      telefono: "699695434"
    },
    localidad: "Elche",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 6.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 4.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 4.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 5.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        nota: 6.25
      }
    ]
  },
  {
    _id: 3,
    nia: "10450111",
    dni: "50814806D",
    nombre: "Noelia",
    apellidos: "Verdú Espí",
    fechaNacimiento: ISODate("2004-06-25"),
    contacto: {
      email: "noeliaverdu3@alu.edugest.es",
      telefono: "660587809"
    },
    localidad: "Sant Joan d'Alacant",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 3.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 6.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        faltas: [
          {
            fecha: ISODate("2025-10-09"),
            horas: 1,
            justificada: false
          }
        ]
      }
    ]
  },
  {
    _id: 4,
    nia: "10450148",
    dni: "36608302F",
    nombre: "Paula",
    apellidos: "Ferri Baeza",
    fechaNacimiento: ISODate("2005-01-10"),
    contacto: {
      email: "paulaferri4@alu.edugest.es"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 6.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 3.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        nota: 9.5
      }
    ]
  },
  {
    _id: 5,
    nia: "10450185",
    nombre: "Andrea",
    apellidos: "Brotons Soriano",
    fechaNacimiento: ISODate("2006-02-19"),
    contacto: {
      email: "andreabrotons5@alu.edugest.es",
      telefono: "639572864"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 4.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 6.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        nota: 8.5
      }
    ]
  },
  {
    _id: 6,
    nia: "10450222",
    dni: "76096799B",
    nombre: "Tomás",
    apellidos: "Cerdá Pérez",
    fechaNacimiento: ISODate("2006-04-03"),
    contacto: {
      email: "tomascerda6@alu.edugest.es",
      telefono: "659376353"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2026-03-10"),
            horas: 3,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 8,
        faltas: [
          {
            fecha: ISODate("2025-12-03"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        nota: 8.5
      }
    ]
  },
  {
    _id: 7,
    nia: "10450259",
    dni: "63874840E",
    nombre: "Valeria",
    apellidos: "Quiles Marco",
    fechaNacimiento: ISODate("2004-01-20"),
    contacto: {
      email: "valeriaquiles7@alu.edugest.es",
      telefono: "661054227"
    },
    localidad: "Sant Joan d'Alacant",
    grupo: {
      codigo: "1DAM",
      ciclo: "DAM",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 6.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 1,
        nota: 6.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 1,
        nota: 8,
        faltas: [
          {
            fecha: ISODate("2025-09-25"),
            horas: 1,
            justificada: false
          },
          {
            fecha: ISODate("2026-02-13"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAM",
          horas: 96
        },
        convocatoria: 1,
        nota: 6.5,
        faltas: [
          {
            fecha: ISODate("2025-09-22"),
            horas: 3,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 1,
        nota: 5.25
      }
    ]
  },
  {
    _id: 8,
    nia: "10450296",
    dni: "75326361G",
    nombre: "Iván",
    apellidos: "Ripoll Agulló",
    fechaNacimiento: ISODate("2003-05-01"),
    contacto: {
      telefono: "645665668"
    },
    localidad: "Sant Joan d'Alacant",
    grupo: {
      codigo: "2DAM",
      ciclo: "DAM",
      curso: 2,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0486",
          nombre: "Acceso a datos",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 7.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0488",
          nombre: "Desarrollo de interfaces",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 5.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0489",
          nombre: "Programación multimedia y dispositivos móviles",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 4
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0490",
          nombre: "Programación de servicios y procesos",
          ciclo: "DAM",
          horas: 80
        },
        convocatoria: 1
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0491",
          nombre: "Sistemas de gestión empresarial",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 6.5,
        faltas: [
          {
            fecha: ISODate("2025-10-21"),
            horas: 3,
            justificada: false
          }
        ]
      }
    ]
  },
  {
    _id: 9,
    nia: "10450333",
    dni: "73361397E",
    nombre: "Martina",
    apellidos: "Alemany Vidal",
    fechaNacimiento: ISODate("2005-04-18"),
    contacto: {
      email: "martinaalemany9@alu.edugest.es",
      telefono: "686052214"
    },
    localidad: "Mutxamel",
    grupo: {
      codigo: "2DAM",
      ciclo: "DAM",
      curso: 2,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0486",
          nombre: "Acceso a datos",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 9
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0488",
          nombre: "Desarrollo de interfaces",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 8.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0489",
          nombre: "Programación multimedia y dispositivos móviles",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0490",
          nombre: "Programación de servicios y procesos",
          ciclo: "DAM",
          horas: 80
        },
        convocatoria: 1,
        nota: 6.5,
        faltas: [
          {
            fecha: ISODate("2026-03-11"),
            horas: 1,
            justificada: true
          },
          {
            fecha: ISODate("2026-04-29"),
            horas: 3,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0491",
          nombre: "Sistemas de gestión empresarial",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 9.75,
        faltas: [
          {
            fecha: ISODate("2026-02-25"),
            horas: 3,
            justificada: false
          }
        ]
      }
    ]
  },
  {
    _id: 10,
    nia: "10450370",
    dni: "72926056W",
    nombre: "Nerea",
    apellidos: "Cerdá Tomás",
    fechaNacimiento: ISODate("2005-08-04"),
    contacto: {
      email: "nereacerda10@alu.edugest.es"
    },
    localidad: "San Vicente del Raspeig",
    grupo: {
      codigo: "2DAM",
      ciclo: "DAM",
      curso: 2,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0486",
          nombre: "Acceso a datos",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 9
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0488",
          nombre: "Desarrollo de interfaces",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 2.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0489",
          nombre: "Programación multimedia y dispositivos móviles",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 9.25,
        faltas: [
          {
            fecha: ISODate("2025-11-21"),
            horas: 3,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0490",
          nombre: "Programación de servicios y procesos",
          ciclo: "DAM",
          horas: 80
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0491",
          nombre: "Sistemas de gestión empresarial",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 3.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAM",
          horas: 160
        },
        convocatoria: 2,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2025-11-25"),
            horas: 3,
            justificada: false
          },
          {
            fecha: ISODate("2026-02-27"),
            horas: 2,
            justificada: true
          }
        ]
      }
    ]
  },
  {
    _id: 11,
    nia: "10450407",
    dni: "35988837R",
    nombre: "Hugo",
    apellidos: "Brotons Iborra",
    fechaNacimiento: ISODate("2005-12-17"),
    contacto: {
      email: "hugobrotons11@alu.edugest.es",
      telefono: "678897218"
    },
    localidad: "Mutxamel",
    grupo: {
      codigo: "2DAM",
      ciclo: "DAM",
      curso: 2,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0486",
          nombre: "Acceso a datos",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 4.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0488",
          nombre: "Desarrollo de interfaces",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 7.5,
        faltas: [
          {
            fecha: ISODate("2026-01-21"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0489",
          nombre: "Programación multimedia y dispositivos móviles",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 7.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0490",
          nombre: "Programación de servicios y procesos",
          ciclo: "DAM",
          horas: 80
        },
        convocatoria: 1
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0491",
          nombre: "Sistemas de gestión empresarial",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 3.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAM",
          horas: 128
        },
        convocatoria: 2,
        nota: 5.75,
        faltas: [
          {
            fecha: ISODate("2026-03-18"),
            horas: 1,
            justificada: true
          }
        ]
      }
    ]
  },
  {
    _id: 12,
    nia: "10450444",
    dni: "76691674Z",
    nombre: "Lucía",
    apellidos: "Belda Quiles",
    fechaNacimiento: ISODate("2003-11-07"),
    contacto: {
      email: "luciabelda12@alu.edugest.es",
      telefono: "630313272"
    },
    localidad: "San Vicente del Raspeig",
    grupo: {
      codigo: "2DAM",
      ciclo: "DAM",
      curso: 2,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0486",
          nombre: "Acceso a datos",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 5.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0488",
          nombre: "Desarrollo de interfaces",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 5.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0489",
          nombre: "Programación multimedia y dispositivos móviles",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 5.5,
        faltas: [
          {
            fecha: ISODate("2025-10-31"),
            horas: 2,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0490",
          nombre: "Programación de servicios y procesos",
          ciclo: "DAM",
          horas: 80
        },
        convocatoria: 1,
        nota: 5.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0491",
          nombre: "Sistemas de gestión empresarial",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAM",
          horas: 256
        },
        convocatoria: 2,
        nota: 2.75
      }
    ]
  },
  {
    _id: 13,
    nia: "10450481",
    dni: "27663211F",
    nombre: "María",
    apellidos: "Domènech Quiles",
    fechaNacimiento: ISODate("2005-01-25"),
    contacto: {
      email: "mariadomenech13@alu.edugest.es",
      telefono: "675664399"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "2DAM",
      ciclo: "DAM",
      curso: 2,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0486",
          nombre: "Acceso a datos",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 2.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0488",
          nombre: "Desarrollo de interfaces",
          ciclo: "DAM",
          horas: 120
        },
        convocatoria: 1,
        nota: 2.75,
        faltas: [
          {
            fecha: ISODate("2025-12-08"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0489",
          nombre: "Programación multimedia y dispositivos móviles",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 5.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0490",
          nombre: "Programación de servicios y procesos",
          ciclo: "DAM",
          horas: 80
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0491",
          nombre: "Sistemas de gestión empresarial",
          ciclo: "DAM",
          horas: 100
        },
        convocatoria: 1,
        nota: 7.75,
        faltas: [
          {
            fecha: ISODate("2026-02-26"),
            horas: 2,
            justificada: true
          }
        ]
      }
    ]
  },
  {
    _id: 14,
    nia: "10450518",
    nombre: "Carla",
    apellidos: "Valero Cerdá",
    fechaNacimiento: ISODate("2004-07-08"),
    contacto: {
      email: "carlavalero14@alu.edugest.es",
      telefono: "676159146"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAW",
      ciclo: "DAW",
      curso: 1,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 3.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5,
        faltas: [
          {
            fecha: ISODate("2025-11-28"),
            horas: 2,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAW",
          horas: 256
        },
        convocatoria: 1,
        nota: 4.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAW",
          horas: 96
        },
        convocatoria: 1,
        nota: 8.5,
        faltas: [
          {
            fecha: ISODate("2026-01-14"),
            horas: 2,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAW",
          horas: 128
        },
        convocatoria: 1,
        nota: 4,
        faltas: [
          {
            fecha: ISODate("2026-05-04"),
            horas: 2,
            justificada: true
          }
        ]
      }
    ]
  },
  {
    _id: 15,
    nia: "10450555",
    dni: "75229754C",
    nombre: "Manuel",
    apellidos: "Soriano Domènech",
    fechaNacimiento: ISODate("2006-12-25"),
    contacto: {
      email: "manuelsoriano15@alu.edugest.es",
      telefono: "621760503"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAW",
      ciclo: "DAW",
      curso: 1,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 3
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 6
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAW",
          horas: 256
        },
        convocatoria: 1,
        nota: 6
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAW",
          horas: 96
        },
        convocatoria: 1,
        nota: 5.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAW",
          horas: 128
        },
        convocatoria: 1,
        nota: 8
      }
    ]
  },
  {
    _id: 16,
    nia: "10450592",
    dni: "72901124W",
    nombre: "Julia",
    apellidos: "Espí Marco",
    fechaNacimiento: ISODate("2006-12-01"),
    contacto: {
      email: "juliaespi16@alu.edugest.es"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1DAW",
      ciclo: "DAW",
      curso: 1,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.5,
        faltas: [
          {
            fecha: ISODate("2026-03-05"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAW",
          horas: 256
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAW",
          horas: 96
        },
        convocatoria: 1,
        nota: 8.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAW",
          horas: 128
        },
        convocatoria: 1,
        nota: 6.25
      }
    ]
  },
  {
    _id: 17,
    nia: "10450629",
    dni: "62431102V",
    nombre: "Jorge",
    apellidos: "Iborra Alemany",
    fechaNacimiento: ISODate("2001-06-01"),
    contacto: {
      email: "jorgeiborra17@alu.edugest.es",
      telefono: "674289054"
    },
    localidad: "El Campello",
    grupo: {
      codigo: "1DAW",
      ciclo: "DAW",
      curso: 1,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.75,
        faltas: [
          {
            fecha: ISODate("2026-02-11"),
            horas: 3,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 6
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAW",
          horas: 256
        },
        convocatoria: 1,
        nota: 4
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAW",
          horas: 96
        },
        convocatoria: 1,
        faltas: [
          {
            fecha: ISODate("2026-04-08"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAW",
          horas: 128
        },
        convocatoria: 1,
        nota: 8.25
      }
    ]
  },
  {
    _id: 18,
    nia: "10450666",
    dni: "38842718L",
    nombre: "Daniel",
    apellidos: "Alemany Pérez",
    fechaNacimiento: ISODate("2001-08-22"),
    contacto: {
      email: "danielalemany18@alu.edugest.es",
      telefono: "664181554"
    },
    localidad: "El Campello",
    grupo: {
      codigo: "1DAW",
      ciclo: "DAW",
      curso: 1,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 6
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAW",
          horas: 256
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAW",
          horas: 96
        },
        convocatoria: 1,
        nota: 6.25,
        faltas: [
          {
            fecha: ISODate("2026-03-25"),
            horas: 3,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAW",
          horas: 128
        },
        convocatoria: 1,
        nota: 5.5
      }
    ]
  },
  {
    _id: 19,
    nia: "10450703",
    dni: "76182503V",
    nombre: "Alba",
    apellidos: "Torregrosa Planelles",
    fechaNacimiento: ISODate("2006-12-21"),
    contacto: {
      telefono: "618940629"
    },
    localidad: "Mutxamel",
    grupo: {
      codigo: "1DAW",
      ciclo: "DAW",
      curso: 1,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0483",
          nombre: "Sistemas informáticos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0484",
          nombre: "Bases de datos",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0485",
          nombre: "Programación",
          ciclo: "DAW",
          horas: 256
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0487",
          nombre: "Entornos de desarrollo",
          ciclo: "DAW",
          horas: 96
        },
        convocatoria: 1,
        nota: 5.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "DAW",
          horas: 128
        },
        convocatoria: 1,
        nota: 8
      }
    ]
  },
  {
    _id: 20,
    nia: "10450740",
    dni: "44338976J",
    nombre: "Mateo",
    apellidos: "Sala Brotons",
    fechaNacimiento: ISODate("2003-04-09"),
    contacto: {
      email: "mateosala20@alu.edugest.es",
      telefono: "628385636"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "2DAW",
      ciclo: "DAW",
      curso: 2,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0612",
          nombre: "Desarrollo web en entorno cliente",
          ciclo: "DAW",
          horas: 140
        },
        convocatoria: 1,
        nota: 6.5,
        faltas: [
          {
            fecha: ISODate("2025-09-18"),
            horas: 1,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0613",
          nombre: "Desarrollo web en entorno servidor",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0614",
          nombre: "Despliegue de aplicaciones web",
          ciclo: "DAW",
          horas: 80
        },
        convocatoria: 1,
        nota: 7.5,
        faltas: [
          {
            fecha: ISODate("2026-03-26"),
            horas: 1,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0615",
          nombre: "Diseño de interfaces web",
          ciclo: "DAW",
          horas: 120
        },
        convocatoria: 1,
        nota: 9.25,
        faltas: [
          {
            fecha: ISODate("2025-10-31"),
            horas: 1,
            justificada: false
          },
          {
            fecha: ISODate("2026-04-17"),
            horas: 2,
            justificada: false
          }
        ]
      }
    ]
  },
  {
    _id: 21,
    nia: "10450777",
    dni: "57150988J",
    nombre: "Elena",
    apellidos: "Carbonell Soriano",
    fechaNacimiento: ISODate("2005-06-21"),
    contacto: {
      email: "elenacarbonell21@alu.edugest.es",
      telefono: "633510324"
    },
    localidad: "El Campello",
    grupo: {
      codigo: "2DAW",
      ciclo: "DAW",
      curso: 2,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0612",
          nombre: "Desarrollo web en entorno cliente",
          ciclo: "DAW",
          horas: 140
        },
        convocatoria: 1,
        nota: 8.75,
        faltas: [
          {
            fecha: ISODate("2025-10-14"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0613",
          nombre: "Desarrollo web en entorno servidor",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 7.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0614",
          nombre: "Despliegue de aplicaciones web",
          ciclo: "DAW",
          horas: 80
        },
        convocatoria: 1,
        nota: 1.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0615",
          nombre: "Diseño de interfaces web",
          ciclo: "DAW",
          horas: 120
        },
        convocatoria: 1,
        nota: 4.25
      }
    ]
  },
  {
    _id: 22,
    nia: "10450814",
    dni: "79846783Y",
    nombre: "Sofía",
    apellidos: "Planelles Marco",
    fechaNacimiento: ISODate("2004-07-13"),
    contacto: {
      email: "sofiaplanelles22@alu.edugest.es"
    },
    localidad: "Elche",
    grupo: {
      codigo: "2DAW",
      ciclo: "DAW",
      curso: 2,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0612",
          nombre: "Desarrollo web en entorno cliente",
          ciclo: "DAW",
          horas: 140
        },
        convocatoria: 1,
        nota: 5.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0613",
          nombre: "Desarrollo web en entorno servidor",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5.5,
        faltas: [
          {
            fecha: ISODate("2025-09-23"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0614",
          nombre: "Despliegue de aplicaciones web",
          ciclo: "DAW",
          horas: 80
        },
        convocatoria: 1,
        nota: 4.5,
        faltas: [
          {
            fecha: ISODate("2026-02-19"),
            horas: 1,
            justificada: true
          },
          {
            fecha: ISODate("2026-03-12"),
            horas: 2,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0615",
          nombre: "Diseño de interfaces web",
          ciclo: "DAW",
          horas: 120
        },
        convocatoria: 1,
        nota: 7
      }
    ]
  },
  {
    _id: 23,
    nia: "10450851",
    nombre: "Sara",
    apellidos: "Amorós Guillem",
    fechaNacimiento: ISODate("2000-08-07"),
    contacto: {
      email: "saraamoros23@alu.edugest.es",
      telefono: "631556041"
    },
    localidad: "Mutxamel",
    grupo: {
      codigo: "2DAW",
      ciclo: "DAW",
      curso: 2,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0612",
          nombre: "Desarrollo web en entorno cliente",
          ciclo: "DAW",
          horas: 140
        },
        convocatoria: 1
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0613",
          nombre: "Desarrollo web en entorno servidor",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 6
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0614",
          nombre: "Despliegue de aplicaciones web",
          ciclo: "DAW",
          horas: 80
        },
        convocatoria: 1,
        nota: 3
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0615",
          nombre: "Diseño de interfaces web",
          ciclo: "DAW",
          horas: 120
        },
        convocatoria: 1,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2026-01-06"),
            horas: 3,
            justificada: false
          }
        ]
      }
    ]
  },
  {
    _id: 24,
    nia: "10450888",
    dni: "41037327Z",
    nombre: "Nicolás",
    apellidos: "Verdú Castelló",
    fechaNacimiento: ISODate("2005-05-11"),
    contacto: {
      email: "nicolasverdu24@alu.edugest.es",
      telefono: "622738887"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "2DAW",
      ciclo: "DAW",
      curso: 2,
      turno: "T"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0612",
          nombre: "Desarrollo web en entorno cliente",
          ciclo: "DAW",
          horas: 140
        },
        convocatoria: 1,
        nota: 5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0613",
          nombre: "Desarrollo web en entorno servidor",
          ciclo: "DAW",
          horas: 160
        },
        convocatoria: 1,
        nota: 5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0614",
          nombre: "Despliegue de aplicaciones web",
          ciclo: "DAW",
          horas: 80
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0615",
          nombre: "Diseño de interfaces web",
          ciclo: "DAW",
          horas: 120
        },
        convocatoria: 1,
        nota: 6
      }
    ]
  },
  {
    _id: 25,
    nia: "10450925",
    dni: "70931220W",
    nombre: "Diego",
    apellidos: "Iborra Torregrosa",
    fechaNacimiento: ISODate("2005-09-04"),
    contacto: {
      email: "diegoiborra25@alu.edugest.es",
      telefono: "646908920"
    },
    localidad: "San Vicente del Raspeig",
    grupo: {
      codigo: "1ASIR",
      ciclo: "ASIR",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0369",
          nombre: "Implantación de sistemas operativos",
          ciclo: "ASIR",
          horas: 224
        },
        convocatoria: 1,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2026-02-25"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0370",
          nombre: "Planificación y administración de redes",
          ciclo: "ASIR",
          horas: 192
        },
        convocatoria: 1,
        nota: 8.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0371",
          nombre: "Fundamentos de hardware",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 6.5,
        faltas: [
          {
            fecha: ISODate("2026-01-01"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0372",
          nombre: "Gestión de bases de datos",
          ciclo: "ASIR",
          horas: 160
        },
        convocatoria: 1,
        nota: 6.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 3
      }
    ]
  },
  {
    _id: 26,
    nia: "10450962",
    dni: "64974513L",
    nombre: "Víctor",
    apellidos: "Tomás Guillem",
    fechaNacimiento: ISODate("2006-12-06"),
    contacto: {
      email: "victortomas26@alu.edugest.es",
      telefono: "627804543"
    },
    localidad: "Elche",
    grupo: {
      codigo: "1ASIR",
      ciclo: "ASIR",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0369",
          nombre: "Implantación de sistemas operativos",
          ciclo: "ASIR",
          horas: 224
        },
        convocatoria: 1,
        nota: 8.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0370",
          nombre: "Planificación y administración de redes",
          ciclo: "ASIR",
          horas: 192
        },
        convocatoria: 1,
        nota: 7.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0371",
          nombre: "Fundamentos de hardware",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 8.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0372",
          nombre: "Gestión de bases de datos",
          ciclo: "ASIR",
          horas: 160
        },
        convocatoria: 1,
        nota: 6.75,
        faltas: [
          {
            fecha: ISODate("2025-11-20"),
            horas: 1,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 8.25
      }
    ]
  },
  {
    _id: 27,
    nia: "10450999",
    dni: "65790137V",
    nombre: "Álex",
    apellidos: "Tomás Vidal",
    fechaNacimiento: ISODate("2006-09-20"),
    contacto: {
      email: "alextomas27@alu.edugest.es",
      telefono: "657158423"
    },
    localidad: "Mutxamel",
    grupo: {
      codigo: "1ASIR",
      ciclo: "ASIR",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0369",
          nombre: "Implantación de sistemas operativos",
          ciclo: "ASIR",
          horas: 224
        },
        convocatoria: 1,
        nota: 8,
        faltas: [
          {
            fecha: ISODate("2025-09-29"),
            horas: 1,
            justificada: true
          },
          {
            fecha: ISODate("2026-03-03"),
            horas: 1,
            justificada: false
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0370",
          nombre: "Planificación y administración de redes",
          ciclo: "ASIR",
          horas: 192
        },
        convocatoria: 1,
        nota: 6.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0371",
          nombre: "Fundamentos de hardware",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 4.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0372",
          nombre: "Gestión de bases de datos",
          ciclo: "ASIR",
          horas: 160
        },
        convocatoria: 1,
        nota: 9.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 6.25,
        faltas: [
          {
            fecha: ISODate("2026-01-21"),
            horas: 3,
            justificada: false
          }
        ]
      }
    ]
  },
  {
    _id: 28,
    nia: "10451036",
    dni: "48929967C",
    nombre: "Pablo",
    apellidos: "Amorós Carbonell",
    fechaNacimiento: ISODate("2006-10-21"),
    contacto: {
      email: "pabloamoros28@alu.edugest.es"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1ASIR",
      ciclo: "ASIR",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0369",
          nombre: "Implantación de sistemas operativos",
          ciclo: "ASIR",
          horas: 224
        },
        convocatoria: 1,
        nota: 6
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0370",
          nombre: "Planificación y administración de redes",
          ciclo: "ASIR",
          horas: 192
        },
        convocatoria: 1
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0371",
          nombre: "Fundamentos de hardware",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2025-10-10"),
            horas: 1,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0372",
          nombre: "Gestión de bases de datos",
          ciclo: "ASIR",
          horas: 160
        },
        convocatoria: 1,
        nota: 1.75
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 6.75
      }
    ]
  },
  {
    _id: 29,
    nia: "10451073",
    dni: "65878726X",
    nombre: "Aitana",
    apellidos: "Pascual Brotons",
    fechaNacimiento: ISODate("2006-07-10"),
    contacto: {
      email: "aitanapascual29@alu.edugest.es",
      telefono: "686824567"
    },
    localidad: "Alicante",
    grupo: {
      codigo: "1ASIR",
      ciclo: "ASIR",
      curso: 1,
      turno: "M"
    },
    matriculas: [
      {
        curso: "2025-26",
        modulo: {
          codigo: "0369",
          nombre: "Implantación de sistemas operativos",
          ciclo: "ASIR",
          horas: 224
        },
        convocatoria: 1,
        nota: 7.25,
        faltas: [
          {
            fecha: ISODate("2026-04-02"),
            horas: 1,
            justificada: true
          }
        ]
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0370",
          nombre: "Planificación y administración de redes",
          ciclo: "ASIR",
          horas: 192
        },
        convocatoria: 1,
        nota: 9.25
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0371",
          nombre: "Fundamentos de hardware",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 7.5
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0372",
          nombre: "Gestión de bases de datos",
          ciclo: "ASIR",
          horas: 160
        },
        convocatoria: 1,
        nota: 8
      },
      {
        curso: "2025-26",
        modulo: {
          codigo: "0373",
          nombre: "Lenguajes de marcas y sistemas de gestión de información",
          ciclo: "ASIR",
          horas: 96
        },
        convocatoria: 1,
        nota: 10,
        faltas: [
          {
            fecha: ISODate("2025-10-29"),
            horas: 1,
            justificada: true
          }
        ]
      }
    ]
  },
  {
    _id: 30,
    nia: "10451110",
    dni: "24667071P",
    nombre: "Zoe",
    apellidos: "Iborra Valero",
    fechaNacimiento: ISODate("2006-06-22"),
    contacto: {
      telefono: "639706969"
    },
    localidad: "Sant Joan d'Alacant",
    matriculas: []
  },
  {
    _id: 31,
    nia: "10451147",
    dni: "69382434J",
    nombre: "Lucas",
    apellidos: "Agulló Cerdá",
    fechaNacimiento: ISODate("2006-04-18"),
    contacto: {
      email: "lucasagullo31@alu.edugest.es",
      telefono: "627202308"
    },
    localidad: "Alicante",
    matriculas: []
  },
  {
    _id: 32,
    nia: "10451184",
    nombre: "Irene",
    apellidos: "Belda Iborra",
    fechaNacimiento: ISODate("2006-07-28"),
    contacto: {
      email: "irenebelda32@alu.edugest.es",
      telefono: "642961184"
    },
    localidad: "Mutxamel",
    matriculas: []
  }
]);

print('ciclos: ' + db.ciclos.countDocuments() + ' · profesores: ' + db.profesores.countDocuments() + ' · expedientes: ' + db.expedientes.countDocuments());
