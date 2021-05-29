# :heavy_dollar_sign: :heavy_dollar_sign: Tarea 02  __ DCCasino :heavy_dollar_sign: :heavy_dollar_sign:

### ``pgarnham``

## Consideraciones generales :pencil:

* Es una buena idea correr mi programa en la consola :smile:

* Usé la librería ``time`` para controlar el paso del tiempo, y no los ticks (que si usé para los movimientos). Esto con la finalidad de que los tiempos fueran mas exactos (los primeros ticks son mas rapidos que los ultimos, puesto que realizan mas acciones). Espero que no cause un inconveniente haberlo hecho así.

* Lamentablemente modelé el problema de manera circular, y cuando me di cuenta de que no era conveniente ya era demasiado tarde. En mi diagrama de clases, todas las clases apuntan a la clase Casino, puesto que esta contiene objetos de todas las demas clases. Lo cierto es que los clientes tambien poseen al casino, y las instalaciones como atributos. Se que no es una buena practica pero me preocupé de que no generara un inconveniente a la hora de correr la simulacion.

-------

### Cosas no completadas   :x:


* :man: Solo alcancé a controlar los choques con el tragamonedas :sunglasses:. Los clientes chocan con los demas elementos. Y se me ocurrió al final disponer todo de manera que fuera imposible chocar :cry:

* :a: Si bien hay properties que controlan si las instalaciones pueden funcionar o no, no implementé los horarios de los funcionarios.

* No realizé la estadística que revisaba el tiempo sin funcionar de las instalaciones :cry:


-------

## Ejecución :computer:
* El módulo principal de la tarea a ejecutar es  ```simulacion.py```

* Los módulos donde se implementan las clases son ```clases.py```  ,  ```clientes.py``` y ```casino.py```

* Se utiliza ``funciones.py`` para controlar el input de tiempo y controlar los movimientos.

* El archivo ``resultados.txt`` no es necesario. Si no existe el programa creará uno desde cero. Si existe uno, seguirá completandolo desde la ultima simulacion guardada (no fue subido ese archivo) :wink:

* El archivo ``parametros.py`` tiene los parametros externos del enunciado con los nombres en latin correspondientes. :wink:


-------

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

```python

import random
import time
from math import pi, fabs
from functools import reduce
from collections import deque

```


-------

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### ```clientes.py```   *Contiene:*
  Contiene la clase Cliente, que modela a la gente que asistirá al Casino.

#### ```clases.py```   *Contiene:*
  Contiene las clases Personal, Tarot, Tragamonedas, Ruleta, Bano, Restobar

#### ```casino.py```   *Contiene:*
  Contiene la clase Casino, que modela el DCCasino y controla bastantes aspectos del funcionamiento del mismo.

-------

## Supuestos y consideraciones adicionales :bulb:
Los supuestos que realicé durante la tarea son los siguientes:

1. Use ```time.time()``` para controlar el paso del tiempo. Me pareció que tenía sus ventajas, por lo que cambié todo a segundos reales (al principio lo había hecho con ticks). La verdad es que no se si fue la mejor decision, pero ya está hecho.

2. Me pareció mas real :sunglasses: asignar un sector para cada actividad (ya sea jugar u otra cosa), por lo que usé un ``random`` para determinar las coordenadas de destino de los clientes (dentro de un rango), y de esta manera los clientes no siguen todos una misma linea.

3. Cuando la gente va a conversar con tini, va cerca del restobar (a la izquierda mirando la pantalla :wink:).

4. La gente conversa entre ellas entre al entrada y el tragamonedas.

5. En *general* usé  ``Docstring``, por lo que las funciones deberían ser autoexplicativas.

6. Los metodos de la clase Casino para realizar las estadisticas retornan strings. En este caso sobrepasé el limite de lineas :cold_sweat:, pero fue porque al imprimir los resultados en ``resultados.txt`` me tomaba saltos de linea y quedaba todo horrible, y ``strip("\n")`` no me quizo ayudar :cold_sweat:


...

-------




## Referencias de código externo :book: :wink: :boat:


* No usé codigo de otras paginas externas :smile:


-------

## Descuentos :smile:

* Intenté cumplir con **PEP 8** siempre, linea a linea. Agregué Docstrings a todas las funciones y métodos, pero a su vez no comenté practicamente ninguna linea. Sólo me pasé de las 80 lineas un par de veces pero solo por la razon expuesta anteriormente.

* Usé muy pocas variables no aclarativas, pero también fue en pocas ocasiones, y para variables que se usaban muy poco, o un par de contadores auxiliares.
