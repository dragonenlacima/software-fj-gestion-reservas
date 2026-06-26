"""
Módulo principal del sistema "Software FJ".

Ejecuta de forma secuencial al menos 10 operaciones (válidas e inválidas) para
demostrar el MANEJO ROBUSTO DE EXCEPCIONES y la ESTABILIDAD de la aplicación:
ningún error detiene el programa y todo evento o error se registra en el log
(`logs/sistema.log`). Cada caso se rotula por consola y se captura con
try/except, de modo que el programa SIEMPRE continúa.
"""

from cliente import Cliente
from excepciones import ErrorBaseSistema
from logger_config import obtener_logger
from reserva import Reserva
from servicios import AlquilerEquipos, AsesoriaEspecializada, ReservaSala

# Logger principal de la aplicación.
logger = obtener_logger()


def rotular(numero, tipo, descripcion):
    """Imprime un rótulo de caso por consola y devuelve su título."""
    titulo = f"--- CASO {numero} ({tipo}): {descripcion} ---"
    print("\n" + titulo)
    return titulo


def main():
    """Orquesta la ejecución secuencial de los casos de prueba."""
    print("=" * 70)
    print("   SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 70)
    logger.info("Inicio de la ejecución del sistema Software FJ.")

    # Contenedores en memoria (sin base de datos): listas de objetos.
    clientes = []
    servicios = []
    reservas = []

    # Referencias reutilizadas entre casos (inicializadas en None por seguridad).
    cliente1 = None
    sala = None

    # =====================================================================
    # CASO 1 (VÁLIDO): cliente correcto
    # =====================================================================
    rotular(1, "VÁLIDO", "creación de cliente correcto")
    try:
        cliente1 = Cliente(1, "María Fernanda López", "1023456789",
                           "maria.lopez@correo.com", "3001234567")
    except ErrorBaseSistema as exc:
        logger.error("CASO 1 falló: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:  # Red de seguridad: la app nunca se detiene.
        logger.error("CASO 1: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        clientes.append(cliente1)
        print(f"[OK] {cliente1.describir()}")
        logger.info("CASO 1: cliente creado -> %s", cliente1.describir())

    # =====================================================================
    # CASO 2 (INVÁLIDO): correo mal formado
    # =====================================================================
    rotular(2, "INVÁLIDO", "correo mal formado")
    try:
        cliente_malo = Cliente(2, "Carlos Pérez", "987654321",
                               "carlos.perez@@correo", "3009876543")
    except ErrorBaseSistema as exc:
        logger.error("CASO 2: cliente inválido (correo): %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 2: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        clientes.append(cliente_malo)
        print(f"[OK] {cliente_malo.describir()}")

    # =====================================================================
    # CASO 3 (VÁLIDO): ReservaSala y cálculo de costo
    # =====================================================================
    rotular(3, "VÁLIDO", "creación de ReservaSala y cálculo de costo")
    try:
        sala = ReservaSala(101, costo_base=50000, capacidad=20, horas=3)
        sala.validar()
        costo = sala.calcular_costo()
    except ErrorBaseSistema as exc:
        logger.error("CASO 3 falló: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 3: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        servicios.append(sala)
        print(f"[OK] {sala.describir()}")
        print(f"     Costo base calculado: {costo:.2f}")
        logger.info("CASO 3: ReservaSala creada, costo=%.2f", costo)

    # =====================================================================
    # CASO 4 (INVÁLIDO): servicio con capacidad negativa
    # =====================================================================
    rotular(4, "INVÁLIDO", "servicio con capacidad negativa")
    try:
        sala_mala = ReservaSala(102, costo_base=50000, capacidad=-5, horas=2)
        sala_mala.validar_parametros()
    except ErrorBaseSistema as exc:
        logger.error("CASO 4: parámetro inválido: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 4: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        print("[OK] (no debería ocurrir)")

    # =====================================================================
    # CASO 5 (VÁLIDO): AlquilerEquipos
    # =====================================================================
    rotular(5, "VÁLIDO", "creación de AlquilerEquipos")
    try:
        equipos = AlquilerEquipos(103, costo_base=30000, tipo_equipo="Laptop",
                                  cantidad=5, dias=4)
        equipos.validar()
        costo_eq = equipos.calcular_costo(aplicar_impuesto=True)
    except ErrorBaseSistema as exc:
        logger.error("CASO 5 falló: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 5: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        servicios.append(equipos)
        print(f"[OK] {equipos.describir()}")
        print(f"     Costo con IVA: {costo_eq:.2f}")
        logger.info("CASO 5: AlquilerEquipos creado, costo con IVA=%.2f", costo_eq)

    # =====================================================================
    # CASO 6 (VÁLIDO): AsesoriaEspecializada
    # =====================================================================
    rotular(6, "VÁLIDO", "creación de AsesoriaEspecializada")
    try:
        asesoria_v = AsesoriaEspecializada(104, costo_base=80000, area="Cloud",
                                           horas=6, nivel_experto=False)
        asesoria_v.validar()
        costo_as = asesoria_v.calcular_costo()
    except ErrorBaseSistema as exc:
        logger.error("CASO 6 falló: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 6: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        servicios.append(asesoria_v)
        print(f"[OK] {asesoria_v.describir()}")
        print(f"     Costo base calculado: {costo_as:.2f}")
        logger.info("CASO 6: AsesoriaEspecializada creada, costo=%.2f", costo_as)

    # =====================================================================
    # CASO 7 (VÁLIDO): reserva exitosa -> confirmar() y procesar()
    # =====================================================================
    rotular(7, "VÁLIDO", "reserva exitosa: confirmar() y procesar()")
    try:
        # Si por algún motivo el cliente o la sala no existen, se aborta el caso.
        if cliente1 is None or sala is None:
            raise ErrorBaseSistema("Faltan datos previos (cliente o servicio).")
        reserva_ok = Reserva(1001, cliente1, sala, duracion=3)
        reserva_ok.confirmar()
        reserva_ok.procesar()
    except ErrorBaseSistema as exc:
        logger.error("CASO 7 falló: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 7: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        reservas.append(reserva_ok)
        print(f"[OK] {reserva_ok.describir()}")
        logger.info("CASO 7: reserva confirmada y procesada -> %s",
                    reserva_ok.describir())

    # =====================================================================
    # CASO 8 (INVÁLIDO): reserva sobre servicio no disponible
    # =====================================================================
    rotular(8, "INVÁLIDO", "reserva sobre servicio no disponible")
    try:
        equipo_no_disp = AlquilerEquipos(105, 30000, "Proyector", cantidad=2,
                                         dias=1, disponible=False)
        Reserva(1002, cliente1, equipo_no_disp, duracion=2)
    except ErrorBaseSistema as exc:
        logger.error("CASO 8: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 8: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        print("[OK] (no debería ocurrir)")

    # =====================================================================
    # CASO 9 (INVÁLIDO): reserva con duración inválida
    # =====================================================================
    rotular(9, "INVÁLIDO", "reserva con duración inválida")
    try:
        Reserva(1003, cliente1, sala, duracion=0)
    except ErrorBaseSistema as exc:
        logger.error("CASO 9: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 9: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        print("[OK] (no debería ocurrir)")

    # =====================================================================
    # CASO 10 (VÁLIDO): cálculo con impuesto y descuento (sobrecarga)
    # =====================================================================
    rotular(10, "VÁLIDO", "cálculo con impuesto y descuento (sobrecarga)")
    try:
        asesoria = AsesoriaEspecializada(106, costo_base=80000,
                                         area="Ciberseguridad", horas=4,
                                         nivel_experto=True)
        # Variante 1: sin parámetros.
        c1 = asesoria.calcular_costo()
        # Variante 2: solo impuesto.
        c2 = asesoria.calcular_costo(aplicar_impuesto=True)
        # Variante 3: impuesto + descuento como fracción (float -> singledispatch).
        c3 = asesoria.calcular_costo(aplicar_impuesto=True, descuento=0.10)
        # Variante 4: impuesto + descuento como porcentaje (int -> singledispatch).
        c4 = asesoria.calcular_costo(aplicar_impuesto=True, descuento=10)
    except ErrorBaseSistema as exc:
        logger.error("CASO 10 falló: %s", exc)
        print(f"[ERROR capturado] {exc}")
    except Exception as exc:
        logger.error("CASO 10: error inesperado: %s", exc)
        print(f"[ERROR inesperado] {exc}")
    else:
        servicios.append(asesoria)
        print(f"[OK] calcular_costo()                    = {c1:.2f}")
        print(f"     calcular_costo(impuesto)            = {c2:.2f}")
        print(f"     calcular_costo(impuesto, desc=0.10) = {c3:.2f}  (float = fracción)")
        print(f"     calcular_costo(impuesto, desc=10)   = {c4:.2f}  (int = porcentaje)")
        logger.info("CASO 10: sobrecarga demostrada (%.2f / %.2f / %.2f / %.2f)",
                    c1, c2, c3, c4)

    # =====================================================================
    # Resumen final en memoria
    # =====================================================================
    print("\n" + "=" * 70)
    print(f"   RESUMEN: {len(clientes)} cliente(s), {len(servicios)} servicio(s), "
          f"{len(reservas)} reserva(s) en memoria.")
    print("=" * 70)
    logger.info("Fin de la ejecución del sistema Software FJ.")


if __name__ == "__main__":
    # try/finally a nivel de aplicación: garantiza un cierre limpio y deja
    # constancia del fin de la ejecución pase lo que pase.
    try:
        main()
    finally:
        print("\nEjecución finalizada. Revise 'logs/sistema.log' para el detalle.")
