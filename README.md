# Software FJ — Sistema de Gestión de Clientes, Servicios y Reservas

Aplicación de consola desarrollada en **Python 3.12**, orientada a objetos, para
la empresa ficticia **Software FJ**. Gestiona **clientes**, **servicios** y
**reservas** en memoria (sin base de datos). El foco del proyecto es el
**manejo robusto de excepciones** y la **estabilidad**: la aplicación **nunca se
detiene** ante un error, y todo error o evento relevante queda registrado en un
archivo de logs.

Curso: **Programación (213023)** — Fase 4 — UNAD.

---

## Descripción

El sistema modela tres entidades principales que heredan de una clase abstracta
común (`EntidadBase`):

- **Cliente**: encapsula datos personales con atributos privados y validaciones
  robustas (nombre, documento, correo y teléfono).
- **Servicio** (abstracto) y sus tres especializaciones con **polimorfismo**:
  - `ReservaSala` (capacidad, horas)
  - `AlquilerEquipos` (tipo de equipo, cantidad, días)
  - `AsesoriaEspecializada` (área, horas, nivel experto)
- **Reserva**: integra cliente, servicio, duración y estado (`Enum`), y
  **congela** el costo total al momento de crearse.

El cálculo de costos aplica **sobrecarga** mediante parámetros opcionales y
`functools.singledispatchmethod`, e incluye una constante **IVA = 0.19 (19%)**.

---

## Requisitos

- **Python 3.12** o superior.
- **Solo librería estándar** (no requiere dependencias externas):
  `abc`, `logging`, `re`, `datetime`, `functools`, `enum`, `os`.

---

## Instrucciones de ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

Al ejecutarse:

1. Se imprimen por consola **10 casos** rotulados (válidos e inválidos).
2. Cada caso inválido es **capturado** y el programa **continúa**.
3. Se genera (o actualiza) el archivo de logs en `logs/sistema.log` con
   entradas de nivel **INFO** (eventos exitosos) y **ERROR** (excepciones).

> La carpeta `logs/` se crea automáticamente en tiempo de ejecución.

---

## Estructura de módulos

Integrados en orden de dependencia:

```
software-fj-gestion-reservas/
├── excepciones.py     # Jerarquía de excepciones personalizadas
├── logger_config.py   # obtener_logger(): configura el log en logs/sistema.log
├── entidad_base.py    # Clase abstracta EntidadBase (id, describir(), validar())
├── cliente.py         # Cliente: datos privados + properties con validación
├── servicios.py       # Servicio (ABC) + ReservaSala / AlquilerEquipos / AsesoriaEspecializada
├── reserva.py         # Reserva + EstadoReserva (Enum); costo congelado
├── main.py            # Punto de entrada: ejecuta los 10 casos de prueba
├── README.md          # Este archivo
└── logs/
    └── sistema.log    # Archivo de logs (generado en runtime)
```

**Cadena de dependencias:**
`excepciones → logger_config → entidad_base → cliente → servicios → reserva → main`

---

## Manejo de excepciones cubierto

- Excepciones **personalizadas** con jerarquía (`ErrorBaseSistema` y derivadas).
- `try` / `except`.
- `try` / `except` / `else`.
- `try` / `except` / `finally`.
- Encadenamiento con `raise ... from ...`.
- Todos los errores y eventos se registran en `logs/sistema.log`.
- La aplicación **nunca se detiene** ante un error.

---

## Casos de prueba ejecutados por `main.py`

| #   | Tipo     | Descripción                                             |
| --- | -------- | ------------------------------------------------------- |
| 1   | VÁLIDO   | Cliente correcto                                        |
| 2   | INVÁLIDO | Cliente con correo mal formado                          |
| 3   | VÁLIDO   | `ReservaSala` y cálculo de costo                        |
| 4   | INVÁLIDO | Servicio con capacidad negativa                         |
| 5   | VÁLIDO   | `AlquilerEquipos`                                       |
| 6   | VÁLIDO   | `AsesoriaEspecializada`                                 |
| 7   | VÁLIDO   | Reserva exitosa: `confirmar()` y `procesar()`           |
| 8   | INVÁLIDO | Reserva sobre servicio no disponible                    |
| 9   | INVÁLIDO | Reserva con duración inválida                           |
| 10  | VÁLIDO   | Cálculo con impuesto y descuento (demuestra sobrecarga) |

---

## Flujo de trabajo en GitHub

- Repositorio público con la rama `main` **protegida** mediante un _ruleset_:
  pull request obligatorio con **una aprobación**, sin _force push_ y sin
  eliminación de la rama.
- Cada módulo se integró mediante el flujo profesional:
  **rama propia → commit descriptivo → pull request → revisión → aprobación → merge**.

---

## Nota sobre el desarrollo

Debido a la no participación de los demás integrantes del grupo asignado, y con
**autorización expresa del tutor** (foro del curso, 25 de junio de 2026), el
proyecto fue desarrollado de **forma individual**. Para ejercitar y evidenciar el
flujo completo de ramas y revisión de pull requests, se utilizó una segunda
cuenta de GitHub del mismo autor para crear los pull requests, mientras que la
cuenta propietaria del repositorio realizó la revisión y aprobación. Si algún
integrante se incorpora, podrá hacerlo creando una rama independiente y aportando
mediante pull request para su revisión.

---

## Grupo asignado (Programación 213023)

- Andrea Katalina Marciales Luna
- Keilyn Daniela Acosta Peña
- Lisbeth Karina Carrascal Clavijo
- John Alexander Rodríguez Sereno _(desarrollo del proyecto)_
- Jose Luis Cardozo Inciarte
