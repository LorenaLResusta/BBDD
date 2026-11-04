---
title: "Juegos UD03"
weight: 3
bookToc: true
aliases:
  - /ud03-modelo-relacional/ud03-escape-room/
---

# Juegos · UD03 Modelo relacional

{{< ra "RA6:b,c,d,e,f,h" "RA2:a,d,e" >}}

Cinco juegos para dominar el modelo relacional y la transformación desde el E/R, de menos a más difíciles. El **memory** y el **duelo** se pueden jugar **por equipos**.

| Juego | Formato | Duración |
|---|---|---|
| 🏦 Escape room | Cuatro salas; la última, con superclaves, cadenas de débiles y borrados combinados | 40-50 min |
| 🔤 Rosco | Pasapalabra de claves, integridad y transformación, a contrarreloj | 2,5 min |
| 🔍 Caza de errores | Cinco errores en un esquema transformado | 5-10 min |
| 🃏 Memory | 18 parejas diagrama ↔ esquema que solo cambian en las cardinalidades | 15-20 min |
| ⚔️ Duelo por equipos | Doce rondas para transformar un caso EER completo en 13 tablas | 40-50 min |

## 1. Escape room · Bloqueo en el Banco Codd

El sistema de seguridad del Banco Codd te ha dejado encerrado en el sótano y solo abre las puertas a quien demuestra que entiende su base de datos relacional.

| Sala | Candado | Qué repasas |
|---|---|---|
| 📚 Archivo | 4 dígitos | Grado y cardinalidad, claves candidatas, valores nulos, restricciones inherentes |
| 🖥️ Sala de servidores | 3 dígitos + corriente | Integridad referencial, VNN, políticas de borrado, borrado en cascada, FK compuestas |
| 🏦 Cámara acorazada | 3 dígitos + llave | Transformación de N:M, 1:N y 1:1, número de tablas, pérdidas semánticas |
| 🗄️ Despacho del director | 3 dígitos, sin pegatinas | Superclaves, cadena de entidades débiles, borrado con cascada y puesta a nulos, jerarquías parciales |

> [!TIP]
> En la sala de servidores, **lee primero la pizarra**. En el despacho del director no hay pegatinas: el orden está en la historia de la sala.

{{< escape-click data="escape_ud03" >}}

## 2. Rosco del modelo relacional

> [!TIP]
> **Por equipos:** proyectadlo y que cada equipo conteste una letra por turno; quien dice *pasapalabra* cede el turno.

{{< rosco data="rosco_ud03" >}}

## 3. Caza de errores en un esquema

> [!TIP]
> Antes de buscar errores, **transforma tú el diagrama** con las reglas de la unidad y compara tu esquema con el del becario.

{{< caza data="caza_ud03" >}}

## 4. Memory de parejas

> [!WARNING]
> Muchas cartas usan las mismas entidades (EMPLEADO, DEPARTAMENTO, ALUMNO, EXAMEN, AULA…) y solo cambian las cardinalidades o una restricción: VNN, UK, nulos… Léelas enteras.

{{< memory data="memory_ud03" >}}

## 5. Duelo por equipos

> [!TIP]
> Es el mismo caso del duelo de la UD02, ya resuelto. Las rondas abiertas se contestan escribiendo el esquema en la pizarra.

{{< duelo data="duelo_ud03" >}}

## Instrucciones

- **Orden recomendado:** rosco y caza al acabar la teoría; escape room y memory en la sesión de repaso; duelo como actividad final de la unidad.
- **Dificultad:** el rosco va a contrarreloj (140 s), el memory obliga a fijarse en cada cardinalidad y el duelo exige transformar un caso con jerarquía solapada, ternaria, débil, agregación y dos FK hacia la misma tabla.
- **Al terminar** cada juego aparece el repaso de lo que ha costado más, con enlaces a la teoría.
- **Progreso:** el escape room y la mejor marca del rosco se guardan en el navegador.
- **Más:** el [escape room final del trimestre](/escape-rooms/trimestre-1) mezcla la UD02 y la UD03.
