"""Otras clases necesarias."""

import random
import time
from collections import deque
from functools import reduce
from gui.entities import Building, Game
import gui
from clientes import Cliente
from parametros import ALPHA, DELTA, EPSILON, ETA, GAMMA, K, OMEGA, P, X

NOMBRES = []
APELLIDOS = []
with open("nombres.csv", "r") as archivo:
    for linea in archivo:
        nombre, apellido = linea.strip().split(",")
        NOMBRES.append(nombre)
        APELLIDOS.append(apellido)
NOMBRES = tuple(NOMBRES)
APELLIDOS = tuple(APELLIDOS)


class Personal:
    """Clase madre para el personal del casino."""

    def __init__(self, tipo, code, l_nomb=NOMBRES, l_apell=APELLIDOS):
        """Inicializador general para personal de casino."""
        self.instalacion = tipo
        self.identificador = code
        self.edad = random.randint(21, 70)
        self.nombre = random.choice(l_nomb) + " " + random.choice(l_apell)
        self._tiempo_trabajo = 0
        self._tiempo_descanso = 0
        self.coludido = bool(random.choice([0, 0, 0, 1]))
        self.tiempo_descanso_restante = 0
        self.tiempo_trabajo_restante = 0
        self._minutos_restantes_t = 0
        self._minutos_restantes_d = 0
        self.tiempo_anterior = 0

        @property
        def tiempo_trabajo(self):
            """Property para el tiempo que se trabaja."""
            return self._tiempo_trabajo

        @tiempo_trabajo.setter
        def tiempo_trabajo(self):
            if self.tipo is "restobar":
                self._tiempo_trabajo = random.triangular(360, 540, 490) / 60
            elif self.tipo is "juego":
                self._tiempo_trabajo = random.triangular(360, 540, 540) / 60
            elif self.tipo is "tarot":
                self._tiempo_trabajo = random.triangular(360, 500, 420) / 60
            if self._tiempo_trabajo < 6:
                self._tiempo_trabajo = 6
            elif self._tiempo_trabajo > 9:
                self._tiempo_trabajo = 9

        @property
        def tiempo_descanso(self):
            """Property para tiempo de descanso del trabajador."""
            return self._tiempo_descanso

        @tiempo_descanso.setter
        def tiempo_descanso(self, arg):
            self._tiempo_descanso = random.normalvariate(14, 5)
            if self._tiempo_descanso < 8:
                self._tiempo_descanso = 8
            elif self._tiempo_descanso > 20:
                self._tiempo_descanso = 20

        @property
        def trabajando(self):
            """Property que define si se está trabajando o no."""
            return self._trabajando

        @trabajando.setter
        def trabajando(self, arg):
            self._trabajando = arg
            if self.minutos_restantes_t > 0:
                self._trabajando = True

        @property
        def minutos_restantes_t(self):
            """Property que define los minutos restantes."""
            return self._minutos_restantes

        @minutos_restantes_t.setter
        def minutos_restantes_t(self, arg):
            self._minutos_restantes_t = arg
            if self._minutos_restantes_t <= 0.005:
                self._minutos_restantes_t = 0
                self.tiempo_anterior = 0
            elif self._minutos_restantes_t > 0:
                self._minutos_restantes_t = time.time() - self.tiempo_anterior

        @property
        def minutos_restantes_d(self):
            """Property que define los minutos restantes."""
            return self._minutos_restantes_d

        @minutos_restantes_d.setter
        def minutos_restantes_d(self, arg):
            self._minutos_restantes_d = arg
            if self._minutos_restantes_d <= 0.005:
                self._minutos_restantes_d = 0
                self.tiempo_anterior = 0
            elif self._minutos_restantes_d > 0:
                self._minutos_restantes_d = time.time() - self.tiempo_anterior

        def tick(self):
            """La funcion tick para el personal del Casino."""
            self.tiempo_anterior = time.time()


class Tragamonedas:
    """Clase madre para juego."""

    def __init__(self, code):
        """Inicializador para juego."""
        self.jugador_actual = None
        self._pozo = 0
        self.minimo = 1
        self._ganancia = 0
        self._id = code
        self.interfaz = Game("tragamonedas")
        gui.add_entity(self.interfaz)
        self.interfaz.x = 200
        self.interfaz.y = 30
        self.angle = 0
        self.personal = set()
        self.dinero_entregado = 0
        self.dinero_ganado = 0
        self.clientes_historico = [set()]
        self.dia_actual = 0
        self.atendiendose = set()
        self.cola = deque()
        self._funcionando = False
        self.capacidad_max = 20

    @property
    def funcionando(self):
        """Define si esta funcionando o no."""
        if self.personal:
            return True
        return False

    @property
    def ganancia(self):
        """Se define la property de ganancia para el casino."""
        return self._ganancia

    @ganancia.setter
    def ganancia(self, arg):
        self._ganancia = arg

    @property
    def pozo(self):
        """Se define la property del pozo del tragamonedas."""
        return self._pozo

    @pozo.setter
    def pozo(self, arg):
        self._pozo = arg
        if self._pozo < 0:
            self._pozo = 0

    def entrar(self, cliente):
        """El cliente entra a la ruleta."""
        if self.funcionando:
            self.cola.append(cliente)
            self.clientes_historico[self.dia_actual].add(cliente)

    def atender(self):
        """Metodo para atender a los clientes."""
        if len(self.atendiendose) < self.capacidad_max:
            if len(self.cola) > 0:
                cliente = self.cola.popleft()
                self.atendiendose.add(cliente)
                apuesta = cliente.retornar_tragamonedas
                self.jugar(cliente, apuesta)
        if len(self.atendiendose) > 0:
            terminaron = [client for client in self.atendiendose if
                          client.personaje]
            if len(terminaron) > 0:
                terminaron = [client for client in terminaron if not
                              client.ocupado]
                for client in terminaron:
                    self.atendiendose.remove(client)

    def jugar(self, cliente, apuesta):
        """El tragamonedas efectua la jugada."""
        if cliente.dinero >= 1:
            self.pozo += apuesta * 0.9
            self.clientes_historico[self.dia_actual].add(cliente)
            self.ganancia += apuesta * 0.1
            self.dinero_ganado += apuesta * 0.1
            cliente.dinero -= apuesta
            probabilidad = ALPHA - 0.2 * cliente.suerte - 0.1
            resultado = random.random()
            if 0 < resultado < probabilidad:
                cliente.dinero += self.pozo
                self.dinero_entregado += self.pozo
                self.pozo = 0

    def entregar_ganancia(self):
        """Método para entregarle la ganancia al casino."""
        a_entregar = self.ganancia
        self.ganancia = 0
        return a_entregar

    def agregar_personal(self):
        """Método para agregar personal al tragamonedas."""
        self.personal.add(Personal("juego", 1))

    def tick(self):
        """Funcion tick para el Tragamonedas."""
        self.interfaz.angle = 0
        self.atender()


class Ruleta:
    """docstring for Ruleta."""

    def __init__(self, code):
        """Iniciando una ruleta para el casino."""
        self._balance = 0
        self._id = code
        self.interfaz = Game("ruleta")
        gui.add_entity(self.interfaz)
        self.interfaz.x = 620
        self.interfaz.y = 30
        self.interfaz.angle = 0
        self.capacidad_max = 20
        self.personal = set()
        self.dinero_ganado = 0
        self.dinero_entregado = 0
        self.clientes_historico = [set()]
        self.dia_actual = 0
        self._funcionando = False
        self.cola = deque()
        self.atendiendose = set()

    @property
    def balance(self):
        """Estado de ganancia o perdida directa del Casino."""
        return self._balance

    @property
    def funcionando(self):
        """Dice si esta abierto o no."""
        if len(self.personal) > 0:
            return True
        else:
            return False

    @balance.setter
    def balance(self, arg):
        self._balance = arg

    def entrar(self, cliente):
        """El cliente entra a la ruleta."""
        if self.funcionando:
            if cliente not in self.cola:
                self.cola.append(cliente)
                self.clientes_historico[self.dia_actual].add(cliente)

    def atender(self):
        """Metodo para atender a los clientes."""
        if len(self.atendiendose) < self.capacidad_max:
            if len(self.cola) > 0:
                cliente = self.cola.popleft()
                self.atendiendose.add(cliente)
                retornado = cliente.retornar_ruleta
                self.jugar(cliente, retornado)
        if len(self.atendiendose) > 0:
            terminaron = [client for client in self.atendiendose if
                          client.personaje]
            if len(terminaron) > 0:
                terminaron = [client for client in terminaron if not
                              client.ocupado]
                for client in terminaron:
                    self.atendiendose.remove(client)

    def jugar(self, cliente, retornado):
        """El cliente juega a la ruleta."""
        if cliente.dinero >= 1:
            self.clientes_historico[self.dia_actual].add(cliente)
            jugada, dinero = retornado
            if jugada in "verdenumero":
                probabilidad = ((1 / (GAMMA + 1)) +
                                0.2 * cliente.suerte - 0.1)
                monto = dinero * 5
            if jugada in "negrorojo":
                probabilidad = ((GAMMA / 2 * (GAMMA
                                              + 1)) + 0.2 *
                                cliente.suerte - 0.1)
                monto = dinero * 1.5
            resultado = random.random()
            cliente.dinero -= dinero
            self.balance += dinero
            self.dinero_ganado += dinero
            if 0 < resultado < probabilidad:
                cliente.dinero += monto
                self.balance -= monto
                self.dinero_entregado += monto

    def entregar_ganancia(self):
        """Método para entregar el balance al Casino."""
        a_entregar = self.balance
        self.balance = 0
        return a_entregar

    def tick(self):
        """Funcion tick para la ruleta."""
        self.interfaz.angle += 0
        self.atender()


class Restobar:
    """Clase Restobar para comer y tomar."""

    def __init__(self, code, l_nomb=NOMBRES):
        """Inicializador para un Restobar."""
        self._id = code
        self.nombre = random.choice(l_nomb)
        self.cola = deque()
        self.capacidad_max = 20
        self.costo = 2
        self.personal = set()
        self.funcionando = False
        self._ganancias = 0
        self.atendiendose = set()
        self._duracion = 0
        self.interfaz = Building("restobar")
        gui.add_entity(self.interfaz)
        self.interfaz.x = 575
        self.interfaz.y = 200
        self.interfaz.angle = 0
        self.clientes_historico = [set()]
        self.dia_actual = 0

    @property
    def duracion(self):
        """Property para la duracion de la estadia en el Restobar."""
        duracion = 100 / (len(self.personal) + 1)
        if duracion < 10:
            duracion = 10
        return duracion

    @property
    def ganancias(self):
        """Property para las ganancias del Restobar."""
        return self._ganancias

    @ganancias.setter
    def ganancias(self, arg):
        self._ganancias = arg

    def agregar_personal(self, barman):
        """Entra un barman a trabajar."""
        self.personal.add(barman)

    def sale_personal(self, barman):
        """Sale un barman para descansar."""
        self.personal.remove(barman)

    def check_abrir(self):
        """Abre el restobar con dos barman."""
        if len(self.personal) < 2:
            self.funcionando = False
        else:
            self.funcionando = True

    def entrar(self, cliente):
        """Método para hacer entrar a un cliente."""
        self.check_abrir()
        if self.funcionando:
            self.cola.append(cliente)

    def revisar_cola(self):
        """Revisa si se puede atender a alguien."""
        if len(self.atendiendose) < self.capacidad_max:
            if len(self.cola) > 0:
                cliente_ = self.cola.popleft()
                self.atendiendose.add(cliente_)
                self.atender(cliente_)
        if len(self.atendiendose) > 0:
            terminaron = [client for client in self.atendiendose if
                          client.personaje]
            if len(terminaron) > 0:
                terminaron = [client for client in terminaron if not
                              client.ocupado]
                for client in terminaron:
                    self.atendiendose.remove(client)

    def atender(self, cliente):
        """Método para atender a un cliente en el Restobar."""
        if cliente.dinero >= self.costo:
            self.clientes_historico[self.dia_actual].add(cliente)
            if cliente.lucidez > cliente.ansiedad:
                cliente.tomar(self.duracion)
            else:
                cliente.comer(self.duracion)
            cliente.dinero -= self.costo
            self.ganancias += self.costo
            cliente.minutos_restantes = self.duracion
        if self.cola:
            self.atender(self.cola.popleft())

    def entregar_ganancia(self):
        """Método para que el restobar entregue sus ganancias al casino."""
        a_entregar = self.ganancias
        self.ganancias = 0
        return a_entregar

    def tick(self):
        """Funcion tick para el Restobar."""
        self.interfaz.angle += 0
        self.revisar_cola()


class Tarot:
    """Clase que molela el Tarot del casino."""

    def __init__(self, code, l_nomb=NOMBRES):
        """Inicializador del Tarot."""
        self._id = code
        self.nombre = random.choice(l_nomb)  # tienen nombre (Personificado ;)
        self.cola = deque()
        self.capacidad_max = 1  # no la uso pero hay que ponerla
        self.costo = 10
        self.personal = None
        self.funcionando = False
        self._ganancias = 0
        self.atendiendose = None
        self.interfaz = Building("tarot")
        gui.add_entity(self.interfaz)
        self.interfaz.x = 300
        self.interfaz.y = 300
        self.interfaz.angle = 0
        self.clientes_historico = [set()]
        self.dia_actual = 0
        self.tiempo_anterior = 0
        self.duracion_actual = 0
        self.inicio_ultima_sesion = 0

    def entra_mr_t(self, mr_t):
        """Entra un Mr T al Tarot (debe ser solo 1)."""
        if self.personal:
            self.funcionando = False
            self.personal = None
        else:
            self.personal = mr_t
            self.funcionando = True

    def entrar(self, cliente):
        """Metodo para entrar al Tarot."""
        if self.funcionando:
            if cliente not in self.cola:
                if not cliente.moviendose:
                    self.cola.append(cliente)
                    #self.cola[0].personaje.add_decoration("gui/assets/buildings/building_baños.png")
                    #cliente.haciendo_algo = True
        else:
            pass

    def atender(self):
        """Se atiende a un solo cliente a la vez."""
        if self.funcionando:
            if not self.ocupado:
                if not self.atendiendose:
                    if len(self.cola) > 0:
                        if type(self.cola[0]) is Cliente:
                            pass
                        self.leer_suerte(self.cola.popleft())

    def leer_suerte(self, cliente):
        """Se lee la suerte del cliente."""
        self.clientes_historico[self.dia_actual].add(cliente)
        self.atendiendose = cliente
        cliente.dinero -= self.costo
        self.ganancias += self.costo
        fortuna = random.randint(0, 1)
        resultado = random.random() * 0.2
        if fortuna:
            cliente.suerte += resultado
        else:
            cliente.stamina -= resultado
        self.duracion_actual = self.duracion
        self.inicio_ultima_sesion = time.time()
        cliente.proxima_duracion = self.duracion_actual

    @property
    def duracion(self):
        """Duracion varía según distribución normal."""
        return random.normalvariate(3, 5)

    @property
    def ocupado(self):
        """Property que indica si esta ocupado o no."""
        if time.time() - self.inicio_ultima_sesion >= self.duracion_actual:
            self.atendiendose = None
            return False
        return True

    @property
    def ganancias(self):
        """Property para las ganancias del Tarot."""
        return self._ganancias

    @ganancias.setter
    def ganancias(self, arg):
        self._ganancias = arg

    def entregar_ganancia(self):
        """Método para que el restobar entregue sus ganancias al casino."""
        a_entregar = self.ganancias
        self.ganancias = 0
        return a_entregar

    def tick(self):
        """Funcion tick para el Tarot."""
        if self.funcionando:
            self.atender()
        self.interfaz.angle += 0
        self.tiempo_anterior = time.time()


class Bano:
    """Baño del casino."""

    def __init__(self, code, l_nomb=NOMBRES):
        """Inicializador para los baños del Casino."""
        self.nombre = random.choice(l_nomb)  # tienen nombre (Personificado ;)
        self.code = code
        self.cola = deque()
        self.capacidad_max = 20
        self.costo = 0.2
        self.personal = None  # No requiere personal : )
        self.funcionando = False
        self._ganancias = 0
        self.atendiendose = set()
        self.interfaz = Building("baños")
        gui.add_entity(self.interfaz)
        self.interfaz.x = 40
        self.interfaz.y = 410
        self.interfaz.angle = 0
        self.clientes_historico = [set()]
        self.dia_actual = 0

    @property
    def ganancias(self):
        """Property para las ganancias del Restobar."""
        return self._ganancias

    @ganancias.setter
    def ganancias(self, arg):
        self._ganancias = arg

    def entregar_ganancia(self):
        """Método para que el restobar entregue sus ganancias al casino."""
        a_entregar = self.ganancias
        self.ganancias = 0
        return a_entregar

    def entrar(self, cliente):
        """Método para hacer entrar a un cliente."""
        self.cola.append(cliente)

    def atender(self):
        """Método para atender a un cliente en el Restobar."""
        if self.funcionando:
            if len(self.atendiendose) < self.capacidad_max:
                if len(self.cola) > 0:
                    cliente = self.cola.popleft
                    self.hacer_necesidades(cliente)
                    self.atendiendose.add(cliente)
        terminaron = [client for client in self.atendiendose if not
                      client.ocupado]
        for client in terminaron:
            self.atendiendose.remove(client)

    def hacer_necesidades(self, cliente):
        """El cliente hace sus necesidades."""
        if cliente.dinero >= self.costo:
            self.clientes_historico[self.dia_actual].add(cliente)
            cliente.ir_al_bano()
            cliente.dinero -= self.costo
            self.ganancias += self.costo

    def tick(self):
        """Funcion tick para el baño del Casino."""
        self.interfaz.angle += 0
        self.atender()
