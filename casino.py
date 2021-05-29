"""Clase Casino para el DCCasino."""

import time
import random
from functools import reduce
from math import fabs
from clientes import Cliente
from clases import Tragamonedas, Ruleta, Restobar, Bano, Tarot, Personal
from parametros import ALPHA, DELTA, EPSILON, ETA, GAMMA, K, OMEGA, P, X


class Casino:
    """Clase Casino, administra cosas generales."""

    def __init__(self):
        """Inicializador para el Casino."""
        self._fondos = 0
        self.establecimientos = []
        self.endeudados = False
        self.clientes = set()
        self.dict_clientes = {0: "ninguno"}  # para partir
        self.dict_juegos = {0: "ninguno"}  # para partir
        self.dict_instalaciones = {0: "ninguno"}  # para partir
        self.dict_personal = {0: "ninguno"}  # para partir
        self.persos = ("ludopata", "kibitzer", "dieciochero", "ganador",
                       "millonario")
        self.ruleta = None
        self.tragamonedas = None
        self.bano = None
        self.restobar = None
        self.tarot = None
        self.personal = set()
        self.tiempo_simulacion = 0
        self.tiempo_anterior = 0
        self.contador_primer_usuario = 0
        self.tiempo_inicio = time.time()
        self.clientes_historico = list()
        self.dias_transcurridos = 0
        self.inicio_dia = time.time()
        self.fondos_por_dia = {}
        self.fondo_actual = 0

    def poblar(self):
        """Método para poblar el Casino."""
        self.contador_primer_usuario += 1
        if self.contador_primer_usuario == 1:
            self.tiempo_inicio = time.time()
        prob_p = P
        result = random.random()
        if result <= prob_p:
            personalidad = random.choice(self.persos)
            proximo_id = max(list(self.dict_clientes.keys())) + 1
            self.dict_clientes[proximo_id] = Cliente(personalidad, proximo_id,
                                                     self)
            self.clientes.add(self.dict_clientes[proximo_id])
            self.dict_clientes[proximo_id].momento_llegada = time.time()
            self.clientes_historico.append(self.dict_clientes[proximo_id])
            cliente = self.dict_clientes[proximo_id]
            cliente.personaje.setFixedSize(36, 36)

    @property
    def fondos(self):
        """Property para los fondos del casino."""
        return self._fondos

    @property
    def total_clientes(self):
        """Property que devuelve el total de clientes (#nro)."""
        return len(self.clientes_historico)

    @fondos.setter
    def fondos(self, arg):
        self._fondos = arg
        if self._fondos < 0:
            self.endeudados = True

    @property
    def tiempo_transcurrido(self):
        """Property que retorna el tiempo de simulacion transcurrido."""
        return time.time() - self.tiempo_inicio

    @property
    def minutos_del_dia(self):
        """Retorna los minutos que han pasado en el dia."""
        return time.time() - self.inicio_dia

    def actualizar_dia_instalaciones(self):
        """Actualiza los dias de las instalaciones."""
        for est in self.establecimientos:
            est.dia_actual += 1
            est.clientes_historico.append(set())

    def contar_dias(self):
        """Cuenta los dias que han transcurrido, tambien actualiza fondos."""
        if self.minutos_del_dia >= 1440:
            self.inicio_dia = time.time()
            self.dias_transcurridos += 1
            self.actualizar_dia_instalaciones()
            self.actualizar_fondos()
            self.fondos_por_dia[self.dias_transcurridos] = (self.fondos -
                                                            self.fondo_actual)
            self.fondo_actual += self.fondos

    @property
    def simulacion_en_curso(self):
        """Getter para ver si la simulacion está en curso o no."""
        if self.tiempo_transcurrido >= self.tiempo_simulacion:
            return False
        else:
            return True

    def definir_simulacion(self, arg):
        """Se define el tiempo de simulacion del casino."""
        self.tiempo_simulacion = arg

    def actualizar_fondos(self):
        """El casino le pide a cada juego que entregue sus ganancias."""
        for establecimiento in self.establecimientos:
            self.fondos += establecimiento.entregar_ganancia()

    def actualizar_clientes(self):
        """Actualiza los clientes, sacando a los que se van."""
        self.clientes = ({cliente for cliente in self.clientes if
                          cliente.personaje is not None})

    def actualizar_interfaz(self):
        """Actualiza y elimina los personajes que no estan en la interfaz."""
        for cliente in self.clientes:
            if not cliente.moviendose:
                if cliente.personaje.x is 0:
                    if cliente.personaje.y is 0:
                        if cliente.me_voy:
                            cliente.personaje.deleteLater()
                            cliente.personaje = None

    def agregar_juego(self, tipo):
        """Metodo para agregar juegos al casino."""
        proximo_id = max(list(self.dict_juegos.keys())) + 1
        if tipo is "tragamonedas":
            juego_nuevo = Tragamonedas(proximo_id)
            self.tragamonedas = juego_nuevo
        if tipo is "ruleta":
            juego_nuevo = Ruleta(proximo_id)
            self.ruleta = juego_nuevo
        self.dict_juegos[proximo_id] = juego_nuevo
        self.establecimientos.append(juego_nuevo)

    def agregar_instalacion(self, tipo):
        """Metodo para agregar una instalacion al Casino."""
        proximo_id = max(list(self.dict_instalaciones.keys())) + 1
        if tipo is "restobar":
            instalacion_nueva = Restobar(proximo_id)
            self.restobar = instalacion_nueva
        elif tipo is "bano":
            instalacion_nueva = Bano(proximo_id)
            self.bano = instalacion_nueva
        else:
            instalacion_nueva = Tarot(proximo_id)
            self.tarot = instalacion_nueva
        self.dict_instalaciones[proximo_id] = instalacion_nueva
        self.establecimientos.append(instalacion_nueva)

    def agregar_personal(self, instalacion):
        """Método que agrega el personal del casino."""
        proximo_id = max(list(self.dict_personal.keys())) + 1
        if instalacion is "ruleta":
            nuevo_personal = Personal("juego", proximo_id)
            self.ruleta.personal.add(nuevo_personal)
        elif instalacion is "tragamonedas":
            nuevo_personal = Personal("juego", proximo_id)
            self.tragamonedas.personal.add(nuevo_personal)
        elif instalacion is "tarot":
            nuevo_personal = Personal("tarot", proximo_id)
            self.tarot.entra_mr_t(nuevo_personal)
        elif instalacion is "restobar":
            nuevo_personal = Personal("restobar", proximo_id)
            self.restobar.personal.add(nuevo_personal)
        self.dict_personal[proximo_id] = nuevo_personal
        self.personal.add(nuevo_personal)

    def promedio_dinero_final(self):
        """Calcula el promedio de dineros finales de todos los clientes."""
        suma = 0
        total = len(self.clientes_historico)
        for cliente in self.clientes_historico:
            suma += cliente.dinero
        promedio = suma / total
        return f"Promedio de dineros finales de los clientes: {promedio}"

    def separa_por_personalidad(self):
        """Separa los clientes por personalidad."""
        dieciocheros = [cliente for cliente in self.clientes_historico if
                        cliente.personalidad == "dieciochero"]
        ganadores = [cliente for cliente in self.clientes_historico if
                     cliente.personalidad == "ganador"]
        kibitzers = [cliente for cliente in self.clientes_historico if
                     cliente.personalidad == "kibitzer"]
        ludopatas = [cliente for cliente in self.clientes_historico if
                     cliente.personalidad == "ludopata"]
        millonarios = [cliente for cliente in self.clientes_historico if
                       cliente.personalidad == "millonario"]
        persos = [dieciocheros, ganadores, kibitzers, ludopatas, millonarios]
        return persos

    def promedio_por_personalidad(self):
        """Calcula el promedio de dinero final por personalidad."""
        persos = self.separa_por_personalidad()
        total_dieciocheros = reduce(lambda x, y: x + y, [clien.dinero - clien.dinero_inicial for
                                                         clien in
                                                         persos[0]])
        total_ganadores = reduce(lambda x, y: x + y, [clien.dinero -
                                                      clien.dinero_inicial for
                                                      clien in
                                                      persos[1]])
        total_kibitzers = reduce(lambda x, y: x + y, [clien.dinero -
                                                      clien.dinero_inicial for
                                                      clien in
                                                      persos[2]])
        total_ludopatas = reduce(lambda x, y: x + y, [clien.dinero -
                                                      clien.dinero_inicial for
                                                      clien in
                                                      persos[3]])
        total_millonarios = reduce(lambda x, y: x + y, [clien.dinero -
                                                        clien.dinero_inicial
                                                        for clien in
                                                        persos[4]])
        promedio_dieciocheros = total_dieciocheros / len(persos[0])
        promedio_ganadores = total_ganadores / len(persos[1])
        promedio_kibitzers = total_kibitzers / len(persos[2])
        promedio_ludopatas = total_ludopatas / len(persos[3])
        promedio_millonarios = total_millonarios / len(persos[4])
        promedios = [promedio_dieciocheros, promedio_ganadores,
                     promedio_kibitzers, promedio_ludopatas,
                     promedio_millonarios]
        nombre = "Promedio de ganancia/perdida por personalidades --->"
        string = (f"""dieciocheros: {promedios[0]} | ganadores: {promedios[1]}| kibitzers: {promedios[2]} | ludopatas: {promedios[3]} | millonarios: {promedios[4]}""")
        return nombre + string

    def estadias(self):
        """Calcula el tiempo promedio de estadia de los clientes."""
        cant = self.total_clientes
        estadias = [cliente.calcular_estadia() for cliente in
                    self.clientes_historico if cliente.calcular_estadia() > 2]
        return f"""Promedio de estadias: {reduce(lambda x, y: x + y, estadias) / len(estadias)}"""

    def estadias_por_personalidad(self):
        """Calcula el promedio de estadias por personalidad."""
        persos = self.separa_por_personalidad()
        promedios = list()
        for perso in persos:
            reales = [client.calcular_estadia() for client in perso if
                      client.calcular_estadia() > 2]
            if len(reales) < 1:
                promedios.append(0)
            else:
                prom = (reduce(lambda x, y: x + y, reales) / len(reales))
                promedios.append(prom)
        nombre = "Estadías por personalidad --->"
        string = (f"""dieciocheros: {promedios[0]} | ganadores: {promedios[1]}| kibitzers: {promedios[2]} | ludopatas: {promedios[3]} |millonarios: {promedios[4]}""")
        return nombre + string

    def ganancias_por_dia(self):
        """Calcula y retorna promedio de ganancias por dia."""
        return f"""Promedio de ganancia por dia: {self.fondos / (self.dias_transcurridos + 1)}"""

    def ganancias_por_juego(self):
        """Determina que juego fue mas rentable."""
        ganado_tragamonedas = (self.tragamonedas.dinero_ganado +
                               self.tragamonedas.pozo)
        perdido_tragamonedas = self.tragamonedas.dinero_entregado
        ganado_ruleta = self.ruleta.dinero_ganado
        perdido_ruleta = self.ruleta.dinero_entregado
        balance_traga = ganado_tragamonedas - perdido_tragamonedas
        balance_ruleta = ganado_ruleta - perdido_ruleta
        if balance_traga > balance_ruleta:
            return f"Tragamonedas generó más ganancias: $ {balance_traga} vs ruleta que genero: {balance_ruleta}"
        return f"Ruleta generó más ganancias: $ {balance_ruleta}"

    def porcentaje_tramposos(self):
        """Entrega el porcentaje de tramposos que asistieron."""
        tramposos = [cliente for cliente in self.clientes_historico if
                     cliente.hize_trampa]
        cant_tramposos = len(tramposos)
        total = self.total_clientes
        nombre = "Porcentaje de tramposos --->"
        return nombre + f"{(cant_tramposos / total) * 100} %"

    def razon_de_salida(self):
        """Define las razones de salida en porcentaje c/r al total."""
        tramposos = len([1 for client in self.clientes_historico if
                         client.razon_salida == "Me pillaron"])
        aburridos = len([1 for client in self.clientes_historico if
                         client.razon_salida == "Me quiero ir"])
        pobres = len([1 for client in self.clientes_historico if
                      client.razon_salida == "Sin Dinero"])
        tupla = (tramposos / self.total_clientes * 100,
                 aburridos / self.total_clientes * 100, pobres /
                 self.total_clientes * 100)
        nombre = "Motivos por los que la gente se va --->"
        resultado = f"tramposos: {tupla[0]}%  | aburridos: {tupla[1]}%  |  pobres: {tupla[2]}%"
        return nombre + resultado

    def tiempo_sin_funcionar(self):
        """Entrega el tiempo sin funcionar de cada instalacion."""
        pass

    def visitantes_por_juego(self):
        """Calcula la cantidad de visitantes por juego (prom por dia)."""
        promedios = list()
        for est in self.establecimientos:
            dias = len(est.clientes_historico)
            visitantes = sum([len(set_) for set_ in est.clientes_historico])
            promedios.append(visitantes / dias)
        return f"""Visitantes Ruleta: {promedios[0]} | Visitantes Tragamonedas: {promedios[1]}"""

    def guardar(self):
        """Metodo para guardar todo y luego terminar la simulacion."""
        strings = list()
        self.actualizar_fondos()
        strings.append(self.promedio_dinero_final())
        strings.append(self.promedio_por_personalidad())
        strings.append(self.estadias())
        strings.append(self.estadias_por_personalidad())
        strings.append(self.ganancias_por_dia())
        strings.append(self.ganancias_por_juego())
        strings.append(self.porcentaje_tramposos())
        strings.append(self.razon_de_salida())
        strings.append(self.visitantes_por_juego())
        with open("resultados.txt", "a", encoding="utf-8") as file:
            file.write(70 * "-" + "\n")
            file.write("Resultados de la Simulacion" + "\n")
            file.write(70 * "-" + "\n")
            for resultado in strings:
                file.write(resultado.strip("\n") + "\n")
                file.write("\n")

    def tick(self):
        """Tick para la clase Casino."""
        self.tiempo_anterior = time.time()
        self.contar_dias()
        if not self.simulacion_en_curso:
            self.guardar()
            quit()
