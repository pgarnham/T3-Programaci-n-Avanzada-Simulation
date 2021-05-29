"""Simulacion e implementacion de Clases."""

import gui
from casino import Casino
from funciones import check_tiempo
MENSAJE_1 = "Ingrese la cantidad de segundos que desea de simulacion"
TIEMPO_SIMULACION = check_tiempo()


gui.init()

CASINO = Casino()


CASINO.definir_simulacion(TIEMPO_SIMULACION)
CASINO.agregar_juego("ruleta")
CASINO.agregar_juego("tragamonedas")
CASINO.agregar_instalacion("restobar")
CASINO.agregar_instalacion("bano")
CASINO.agregar_instalacion("tarot")
for i in range(0, 31):
    CASINO.agregar_personal("tragamonedas")
    CASINO.agregar_personal("ruleta")
for i in range(0, 3):
    CASINO.agregar_personal("tarot")
for i in range(0, 55):
    CASINO.agregar_personal("restobar")
gui.set_size(773, 485)


def tick(casino=CASINO):
    """Funcion que se repite en el run."""
    casino.poblar()
    casino.tick()
    casino.actualizar_interfaz()
    casino.actualizar_clientes()
    for est in casino.establecimientos:
        est.tick()
    for cliente in casino.clientes:
        cliente.tick_()


gui.run(tick, 16)
