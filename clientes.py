"""Clase Cliente."""

import random
import time
from math import pi
from gui.entities import Human
import gui
import funciones as fn
from parametros import ALPHA, DELTA, EPSILON, ETA, GAMMA, K, OMEGA, P, X, THETHA

NOMBRES = []
APELLIDOS = []
with open("nombres.csv", "r") as archivo:
    for linea in archivo:
        nombre, apellido = linea.strip().split(",")
        NOMBRES.append(nombre)
        APELLIDOS.append(apellido)
NOMBRES = tuple(NOMBRES)
APELLIDOS = tuple(APELLIDOS)


class Cliente:
    """Clase madre para clientes."""

    def __init__(self, personalidad, code, cassino, l_nomb=NOMBRES,
                 l_apell=APELLIDOS):
        """Inicializando la clase madre cliente."""
        self.personalidad = personalidad
        self.identificador = code
        self.edad = random.randint(18, 70)
        self.nombre = random.choice(l_nomb) + " " + random.choice(l_apell)
        self.personaje = Human(personalidad)
        gui.add_entity(self.personaje)
        self._dinero = 0
        self.dinero_inicial = 0
        self._lucidez = 0
        self._ansiedad = 0
        self._suerte = 0
        self._sociabilidad = 0
        self._stamina = 0
        self._deshonestidad = 0
        self.definir_perso()
        self._retirarse = 1 - self.stamina
        self._jugar = min(self.ansiedad, 1 - self._retirarse)
        self._actividad = (min(self.sociabilidad, 1 - self._retirarse -
                               self._jugar))
        self._instalacion = (1 - (self._retirarse + self._actividad +
                                  self._jugar))
        self._tini = 0
        self.pos_siguiente_x = 0
        self.pos_siguiente_y = 0
        self._moviendose = False
        self.casino = cassino
        self.tragamonedas = self.casino.tragamonedas
        self.ruleta = self.casino.ruleta
        self.bano = self.casino.bano
        self.tarot = self.casino.tarot
        self.restobar = self.casino.restobar
        self.me_voy = False
        self.decision_1 = False
        self.converse = False
        self._minutos_restantes = 0
        self.tiempo_anterior = 0
        self.momento_llegada = time.time()
        self.momento_irse = 0
        self.hize_trampa = False
        self.razon_salida = ""
        self.me_pillaron = False
        self.proxima_duracion = 0
        self.proxima_accion = None
        self.retornar_ruleta = None
        self.retornar_tragamonedas = None

    @property
    def moviendose(self):
        """Property para el booleano (moviendose/no_moviendose)."""
        if self.personaje.x == self.pos_siguiente_x:
            if self.personaje.y == self.pos_siguiente_y:
                return False
        else:
            if self.minutos_restantes != 0:
                return True

    def calcular_estadia(self):
        """Calcula la estadia del cliente en el casino."""
        if self.momento_irse - self.momento_llegada > 0:
            return self.momento_irse - self.momento_llegada
        return 0

    @property
    def ocupado(self):
        """Property para saber si esta ocupado."""
        if self.moviendose:
            if self.minutos_restantes > 0:
                return True
        else:
            return False

    def definir_perso(self):
        """Define la personalidad del Cliente."""
        if self.personalidad is "ludopata":
            self.ansiedad = random.uniform(0.7, 1)
            self.stamina = random.uniform(0.7, 1)
            self.dinero = 200 * random.uniform(0.3, 0.7)
            self.dinero_inicial = self.dinero
            self.lucidez = random.uniform(0.3, 0.7)
            self.suerte = random.uniform(0.3, 0.7)
            self.sociabilidad = random.uniform(0.3, 0.7)
            self.deshonestidad = random.uniform(0.3, 0.7)
        elif self.personalidad is "kibitzer":
            self.ansiedad = random.uniform(0, 0.3)
            self.stamina = random.uniform(0, 0.3)
            self.dinero = 200 * random.uniform(0, 0.3)
            self.dinero_inicial = self.dinero
            self.lucidez = random.uniform(0.3, 0.7)
            self.suerte = random.uniform(0.3, 0.7)
            self.sociabilidad = random.uniform(0.7, 1)
            self.deshonestidad = random.uniform(0.3, 0.7)
        elif self.personalidad is "dieciochero":
            self.ansiedad = random.uniform(0.7, 1)
            self.stamina = random.uniform(0.3, 0.7)
            self.dinero = 200 * random.uniform(0.3, 0.7)
            self.dinero_inicial = self.dinero
            self.lucidez = random.uniform(0, 0.3)
            self.suerte = random.uniform(0.3, 0.7)
            self.sociabilidad = random.uniform(0.7, 1)
            self.deshonestidad = random.uniform(0, 0.3)
        elif self.personalidad is "ganador":
            self.ansiedad = random.uniform(0.3, 0.7)
            self.stamina = random.uniform(0.7, 1)
            self.dinero = 200 * random.uniform(0.3, 0.7)
            self.dinero_inicial = self.dinero
            self.lucidez = random.uniform(0.3, 0.7)
            self.suerte = random.uniform(0.7, 1)
            self.sociabilidad = random.uniform(0.7, 1)
            self.deshonestidad = random.uniform(0.7, 1)
        else:
            self.ansiedad = random.uniform(0.3, 0.7)
            self.stamina = random.uniform(0.7, 1)
            self.dinero = 200 * random.uniform(0.7, 1)
            self.dinero_inicial = self.dinero
            self.lucidez = random.uniform(0.3, 0.7)
            self.suerte = random.uniform(0.3, 0.7)
            self.sociabilidad = random.uniform(0.3, 0.7)
            self.deshonestidad = random.uniform(0.3, 0.7)

    @property
    def retirarse(self):
        """Probabilidad de retirarse del Casino."""
        return self._retirarse

    @retirarse.setter
    def retirarse(self):
        self._retirarse = 1 - self.stamina
        if self._retirarse > 1:
            self._retirarse = 1
        elif self._retirarse < 0:
            self._retirarse = 0

    @property
    def jugar(self):
        """Probabilidad de jugar en el casino."""
        return self._jugar

    @jugar.setter
    def jugar(self):
        self._jugar = min(self.ansiedad, 1 - self.retirarse)
        self._jugar = fn.check_valores(self._jugar)

    @property
    def actividad(self):
        """Probabilidad de realizar una actividad en el Casino."""
        return self._actividad

    @actividad.setter
    def actividad(self):
        self._actividad = (min(self.sociabilidad, 1 - self.retirarse -
                               self.jugar))
        self._actividad = fn.check_valores(self._actividad)

    @property
    def instalacion(self):
        """Probabilidad de usar una instalacion."""
        return self._instalacion

    @instalacion.setter
    def instalacion(self, arg):
        self._instalacion = (1 - (self.retirarse + self.actividad +
                                  self.jugar))
        self._instalacion = fn.check_valores(self._instalacion)

    @property
    def deshonestidad(self):
        """Getter para deshonestidad."""
        return self._deshonestidad

    @deshonestidad.setter
    def deshonestidad(self, arg):
        self._deshonestidad = fn.check_valores(arg)

    @property
    def suerte(self):
        """Getter para la suerte."""
        return self._suerte

    @suerte.setter
    def suerte(self, arg):
        self._suerte = fn.check_valores(arg)

    @property
    def sociabilidad(self):
        """Getter para sociabilidad."""
        return self._sociabilidad

    @sociabilidad.setter
    def sociabilidad(self, arg):
        self._sociabilidad = fn.check_valores(arg)

    @property
    def dinero(self):
        """Getter para dinero."""
        return self._dinero

    @dinero.setter
    def dinero(self, arg):
        self._dinero = arg
        if self._dinero < 0:
            self._dinero = 0
        if self._dinero == 0:
            self.stamina = 0
            self.razon_salida = "Sin Dinero"
        if ((self._dinero > 2 * self.dinero_inicial) or
                (self._dinero < self.dinero_inicial/5)):
            self.ansiedad *= 1.25

    @property
    def stamina(self):
        """Getter para stamina."""
        return self._stamina

    @stamina.setter
    def stamina(self, valor):
        self._stamina = fn.check_valores(valor)

    @property
    def ansiedad(self):
        """Getter para ansiedad."""
        return self._ansiedad

    @ansiedad.setter
    def ansiedad(self, arg):
        self._ansiedad = fn.check_valores(arg)

    @property
    def lucidez(self):
        """Getter para lucidez."""
        return self._lucidez

    @lucidez.setter
    def lucidez(self, arg):
        self._lucidez = fn.check_valores(arg)

    def tomar_decision(self):
        """Metodo para tomar decision cada vez."""
        interv_ret = (0, self.retirarse)
        interv_jugar = (self.retirarse, self.retirarse + self.jugar)
        interv_act = (interv_jugar[1], interv_jugar[1] + self.actividad)
        interv_inst = (interv_act[1], 1)
        numero_decision = random.random()
        if interv_ret[0] <= numero_decision < interv_ret[1]:
            if self.dinero:
                if not self.me_pillaron:
                    self.razon_salida = "Me quiero ir"
                else:
                    self.razon_salida = "Me pillaron"
            self.irse_del_casino()
            self.moviendose
        elif interv_jugar[0] <= numero_decision < interv_jugar[1]:
            juego = random.randint(0, 1)
            if juego:
                self.jugar_ruleta()
            else:
                self.jugar_tragamonedas()
        elif interv_act[0] <= numero_decision < interv_act[1]:
            if self.personalidad is "kibitzer":
                hacer = random.randint(0, 2)
                if hacer is 1:
                    self.conversar()
                elif hacer is 2:
                    self.hablar_con_tini += 1
                else:
                    if self.converse:
                        self.fisico_determinista()
                    else:
                        pass
            else:
                hacer = random.randint(0, 1)
                if hacer:
                    self.conversar()
                else:
                    self.hablar_con_tini += 1
        elif interv_inst[0] <= numero_decision <= interv_inst[1]:
            ir_inst = random.randint(0, 2)
            if ir_inst is 1:
                self.ir_restobar()
            elif ir_inst is 2:
                self.ir_tarot()
            else:
                self.ir_al_bano()
        self.decision_1 = True

    def irse_del_casino(self):
        """Irse del casino."""
        self.pos_siguiente_x = 0
        self.pos_siguiente_y = 0
        self.me_voy = True
        self.proxima_duracion = 1
        self.momento_irse = time.time()

    def tomar(self, duracion):
        """Tomar un trago magico en el restobar."""
        self.minutos_restantes = duracion
        self.lucidez *= 0.8
        self.ansiedad *= 0.85
        self.stamina = 1 - 0.7 * (1 - self.stamina)

    def comer(self, duracion):
        """Comer algo en el restobar."""
        self.minutos_restantes = duracion
        self.lucidez *= 1.1
        self.ansiedad *= 0.8

    def ir_al_bano(self):
        """Método para ir al baño."""
        self.ansiedad *= 0.9
        self.pos_siguiente_x = random.randint(40, 100)
        self.pos_siguiente_y = random.randint(290, 370)
        self.proxima_duracion = random.normalvariate(3 * (1 - self.lucidez), 2)

    def conversar(self):
        """Accion de conversar con otra persona."""
        self.deshonestidad += X
        self.ansiedad *= 1 - EPSILON / 100
        # faltan muchas acciones aca
        self.pos_siguiente_x = random.randint(100, 150)
        self.pos_siguiente_y = random.randint(200, 250)
        self.proxima_duracion = self.duracion_actividades
        self.converse = True

    @property
    def hablar_con_tini(self):
        """El cliente habla con tini."""
        return self._tini

    @hablar_con_tini.setter
    def hablar_con_tini(self, arg):
        """Va a aumentar siempre en uno, pero igual le pongo arg."""
        self._tini = arg
        self.stamina -= ETA
        self.pos_siguiente_x = random.randint(500, 540)
        self.pos_siguiente_y = random.randint(270, 300)
        self.proxima_duracion = self.duracion_actividades

    def apostar(self):
        """Método para decidir cuanto se va a apostar."""
        if self.ansiedad * self.dinero / 6 < 1:
            return 1
        return (1 + THETHA * self.ansiedad) * 1

    def jugar_tragamonedas(self):
        """El cliente decide cuanto va a apostar en el tragamonedas."""
        self.pos_siguiente_x = random.randint(360, 420)
        self.pos_siguiente_y = random.randint(35, 140)
        self.proxima_duracion = 15
        apuesta = self.apostar()
        self.proxima_accion = self.tragamonedas.entrar
        self.retornar_tragamonedas = apuesta

    def ir_restobar(self):
        """Metodo para ir al Restobar."""
        self.pos_siguiente_x = random.randint(530, 700)
        self.pos_siguiente_y = random.randint(385, 460)
        self.proxima_accion = self.restobar.entrar
        # falta bastante codigo creo

    def jugar_ruleta(self):
        """El cliente decide cuanto va a apostar en la ruleta, y a qué."""
        self.pos_siguiente_x = random.randint(580, 680)
        self.pos_siguiente_y = random.randint(78, 135)
        self.proxima_accion = self.ruleta.entrar
        # creo que se como hacerlo
        self.proxima_duracion = 15
        apuesta = self.apostar()
        numero_o_color = random.randint(0, 3)
        if numero_o_color is 0:
            retornar = "verde", apuesta
        if numero_o_color is 1:
            retornar = "negro", apuesta
        if numero_o_color is 2:
            retornar = "rojo", apuesta
        if numero_o_color is 3:
            retornar = "numero", apuesta
        self.retornar_ruleta = retornar

    def ir_tarot(self):
        """Ir a verse la suerte al Tarot."""
        self.pos_siguiente_x = random.randint(250, 400)
        self.pos_siguiente_y = random.randint(382, 440)
        self.proxima_duracion = self.tarot.duracion
        self.proxima_accion = self.tarot.entrar

    def fisico_determinista(self):
        """Actividad pseudo ilicita que un kibitzer puede hacer."""
        self.pos_siguiente_x = random.randint(580, 680)
        self.pos_siguiente_y = random.randint(78, 135)
        self.proxima_duracion = self.duracion_actividades
        self.hize_trampa = True

    @property
    def minutos_restantes(self):
        """Property que define los minutos restantes."""
        return self._minutos_restantes

    @minutos_restantes.setter
    def minutos_restantes(self, arg):
        self._minutos_restantes = arg
        if self._minutos_restantes <= 0:
            self._minutos_restantes = 0
            self.tiempo_anterior = 0
        elif self._minutos_restantes > 0:
            self._minutos_restantes = time.time() - self.tiempo_anterior

    @property
    def duracion_actividades(self):
        """Property que define la duracion de las actividades."""
        return max(self.lucidez + self.sociabilidad - self.ansiedad, 0.1) * pi

    def tick_(self):
        """Funcion para determinar que hacer en cada minuto."""
        self.tiempo_anterior = time.time()
        if self.moviendose:
            self.caminar()
        if not self.moviendose:
            self.minutos_restantes += self.proxima_duracion
            self.proxima_duracion = 0
        if self.proxima_accion:
            self.proxima_accion(self)
            self.proxima_accion = None
        if not self.ocupado:
            self.tomar_decision()

    def caminar(self):
        """Caminar desde el lugar actual hasta el lugar deseado."""
        problemas = fn.check_restricciones(self.personaje.x, self.personaje.y,
                                           self.pos_siguiente_x,
                                           self.pos_siguiente_y)
        # problemas = False
        if problemas:
            valor_x, valor_y = fn.restricciones(self.personaje.x,
                                                self.personaje.y,
                                                self.pos_siguiente_x,
                                                self.pos_siguiente_y)
            self.personaje.x += valor_x
            self.personaje.y += valor_y
        else:
            if self.pos_siguiente_x > self.personaje.x:
                self.personaje.x += 1
            if self.pos_siguiente_y > self.personaje.y:
                self.personaje.y += 1
            if self.pos_siguiente_x < self.personaje.x:
                self.personaje.x -= 1
            if self.pos_siguiente_y < self.personaje.y:
                self.personaje.y -= 1
