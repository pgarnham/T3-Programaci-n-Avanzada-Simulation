"""Acá van las funciones."""


def check_valores(arg):
    """Checkea que sea una probabilidad valida."""
    if arg > 1:
        arg = 1
    elif arg < 0:
        arg = 0
    return arg


def restricciones(x_actual, y_actual, x_final, y_final):
    """Restricciones de movimiento para los personajes."""
    if x_actual is 127 and 30 < y_actual < 162:
        return 0, 1
    elif 340 < x_actual < 350 and 0 < y_actual < 162:
        if x_final < x_actual:
            return 0, 1
        elif x_final > x_actual:
            return 0, 1
        elif x_final and y_final is 0:
            return 0, 1
    elif y_actual is 162 and 127 < x_actual < 348:
        if x_actual < x_final:
            return 1, 0
        return -1, 0
    elif x_actual is 348 and 30 < y_actual < 162:
        return 0, 1
    elif y_actual > y_final and 127 < x_actual < 348:
        return 1, 0
    elif y_actual is 258 and 258 < x_actual < 375:
        if x_final > x_actual:
            return 1, 0
        else:
            return -1, 0
    elif x_actual is 258 and 258 < y_actual < 375:
        return 0, -1
    elif 0 <= y_actual <= 154:
        if x_final is 0:
            if 360 < x_actual < 420:
                return 0, 1


def check_restricciones(x_actual, y_actual, x_final, y_final):
    """Revisa si hay problemas en el camino."""
    if x_actual is 127 and 30 < y_actual < 162:
        return True
    elif 340 < x_actual < 350 and 0 <= y_actual < 162:
        if x_final < x_actual:
            return True
        elif x_final > x_actual:
            return True
        elif x_final and y_final is 0:
            return True
    elif y_actual is 162 and 127 < x_actual < 348:
        if x_actual < x_final:
            return True
        return -1, 0
    elif x_actual is 348 and 30 < y_actual < 162:
        return True
    elif y_actual > y_final and 127 < x_actual < 348:
        return True
    elif y_actual is 258 and 258 < x_actual < 375:
        if x_final > x_actual:
            return True
        else:
            return True
    elif x_actual is 258 and 258 < y_actual < 375:
        return True
    elif 0 <= y_actual <= 154:
        if x_final is 0:
            if 360 < x_actual < 420:
                return True

    return False


def check_tiempo():
    """Checkea que el tiempo de simulacion sea ingresado correctamente."""
    print("_________________________________________________________________")
    print("")
    print("Bienvenido a la Simulacion del Casino DCCasino")
    print("_________________________________________________________________")
    print("")
    ingresado = input("Ingrese el tiempo en segundos: ")
    mal = False
    if len(ingresado) < 2:
        mal = True
    else:
        lista = list(ingresado)
        for caracter in lista:
            if caracter not in "1234567890":
                mal = True
        if mal:
            ingresado = check_tiempo()
    return int(ingresado)
