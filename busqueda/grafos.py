#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clases con los objetos que se van a usar en los algoritmos de búsquedas en
grafos, tanto informada como no informada.
"""


# %% --- ACCIÓN ---

class Accion:
    """
    Clase que representa una acción que se puede llevar a cabo en un estado
    para alcanzar otro estado.
    """

    def __init__(self,
                 nombre):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - nombre: nombre identificativo de la acción.
        """
        # Comprobaciones.
        if not nombre:
            raise "No se ha indicado el nombre de la acción"

        # Guardamos los parámetros pasados.
        self.nombre = nombre


# %% --- ESTADO ---

class Estado:
    """
    Clase que representa un estado en el que se pueden encontrar el problema.
    """

    def __init__(self,
                 nombre,
                 acciones):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - nombre: nombre identificativo del nodo.
        - acciones: lista con las acciones que se pueden aplicar.
        """
        # Comprobaciones.
        if not nombre:
            raise "No se ha indicado el nombre del estado"

        # Puede que no haya acciones a aplicar.
        if acciones is None:
            acciones = []

        # Guardamos los parámetros pasados.
        self.nombre = nombre
        self.acciones = acciones


# %% --- PROBLEMA ---

class Problema:
    """
    Clase que representa un problema a resolver con un grafo.
    """

    def __init__(self,
                 estado_inicial,
                 estados_objetivos,
                 acciones,
                 costes,
                 coste_infinito=99999):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - estado_inicial: el etado desde el que comenzará a resolverse.
        - estados_objetivos: lista de estados a alcanzar.
        - acciones: diccionario donde la clave es el nombre de un estado y
                    el valor es otro diccionario con clave el nombre de una
                    acción y como valor un referencia al nuevo estado.
        - costes: diccionario donde la clave es el nombre de un estado y
                  el valor es otro diccionario con clave el nombre de una
                  acción y como valor un número.
        - coste_infinito: valor del mayor coste posible.
        """
        # Comprobaciones.
        if not estado_inicial:
            raise "No se ha indicado un estado inicial"
        if not estados_objetivos:
            raise "No se ha indicado al menos un estado objetivo"
        if not acciones:
            raise "No se ha indicado ninguna acción"

        # Si no hay costes, ponemos todos los costes a 1.
        if not costes:
            for estado in self.acciones.keys():
                self.costes[estado] = {}
                for accion in self.acciones[estado].keys():
                    self.costes[estado][accion] = 1

        # Guardamos los parámetros pasados.
        self.estado_inicial = estado_inicial
        self.estados_objetivos = estados_objetivos
        self.acciones = acciones
        self.costes = costes
        self.coste_infinito = coste_infinito

    def es_objetivo(self,
                    estado):
        """
        Indica si el estado indicado es uno de los estados objetivos.
        Devuelve: booleano indicando si el estado está entre los estados
                  objetivos o no.
        """
        # Debe estar dentro de la lista de estados objetivos.
        return estado in self.estados_objetivos

    def resultado(self,
                  estado,
                  accion):
        """
        Devuelve el nuevo estado que se obtiene de aplicar la acción indicada
        en el estado actual.
        Argumentos:
        - estado: estado sobre el que aplicar la acción.
        - accion: acción a aplicar sobre el estado indicado.
        Devuelve: estado resultado de aplicar la acción sobre el estado.
        """
        # Comprobaciones.
        if not estado:
            raise "No se indicó estado al que aplicar acción"
        if not accion:
            raise "No se indicó acción a aplicar"

        # Miramos si está definido ese estado en las acciones.
        if estado.nombre not in self.acciones.keys():
            return None

        # Obtenemos las acciones de ese estado.
        acciones_estado = self.acciones[estado.nombre]

        # Miramos si está definido esa acción en ese estado.
        if accion.nombre not in acciones_estado.keys():
            return None

        # Devolvemos el nodo resultado de aplicar la acción.
        return acciones_estado[accion.nombre]

    def coste_accion(self,
                     estado,
                     accion):
        """
        Devuelve el coste de aplicar una acción en un estado.
        Argumentos:
        - estado: estado sobre el que aplicar la acción.
        - accion: accion a aplicar sobre un estado.
        """
        # Comprobaciones.
        if not estado:
            raise "No se ha indicado estado a calcular un coste de acción"
        if not accion:
            raise "No se ha indicado acción para calcular su coste"

        # El estado debe estar en la tabla de costes.
        if estado.nombre not in self.costes.keys():
            return self.coste_infinito

        # Obtenemos los costes de ese estado.
        costes_estado = self.costes[estado.nombre]

        # La acción debe estar en la tabla de costes.
        if accion.nombre not in costes_estado.keys():
            return self.coste_infinito

        # Devolvemos el coste de aplicar esa acción en el estado.
        return costes_estado[accion.nombre]

    def coste_camino(self,
                     nodo):
        """
        Devuelve el coste total de recorrer el camino hasta un estado.
        Argumentos:
        - nodo: coste de alcanzar el nodo indicado desde la ráiz.
        """
        # Comprobaciones.
        if not nodo:
            raise "No se ha indicado un nodo para calcular el coste de camino"

        # Coste total a devolver.
        total = 0

        # Mientrar no lleguemos al nodo raíz (no tiene padre)
        while nodo.padre:
            # Coste de aplicar la acción que generó el nodo.
            total += self.coste_accion(estado=nodo.padre.estado,
                                       accion=nodo.accion)

            # Subimos al nodo padre.
            nodo = nodo.padre

        # Devolvemos el coste.
        return total


# %% --- NODO ---

class Nodo:
    """
    Clase que representa un nodo del árbol que se irá construyendo para
    alcanzar una solución al problema.
    """

    def __init__(self,
                 estado,
                 accion=None,
                 acciones=None,
                 padre=None,
                 hijos=[]):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - estado: estado que representa el nodo.
        - accion: acción que llevó a crear este nodo desde su nodo padre.
        - acciones: diccionario con clave el nombre de una acción y como valor
                    un referencia al nuevo estado.
        - padre: enlace al nodo padre dentro del árbol.
        - hijos: enlace a los nodos hijos dentro del árbol.
        """
        # Comprobaciones.
        if not estado:
            raise "No ha indicado el estado asociado el nodo"

        # Pueden no indicar hijos.
        if hijos is None:
            hijos = []

        # Guardamos los parámetros pasados.
        self.estado = estado
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos = hijos

        # Coste de camino hasta nodo (evitar repetir cálculos)
        # Irá aumentando cuando se llame al método "expandir".
        self.coste = 0

    def agregar(self,
                hijo):
        """
        Agrega el nodo hijo indicado a los hijos del nodo actual.
        Argumentos:
        - hijo: nodo a agregar a los hijos del nodo actual.
        Devuelve: referencia al nodo hijo agregado.
        """
        # Comprobaciones
        if not hijo:
            raise "No se ha indicado nodo hijo a agregar"

        # Indicamos que el padre será el nodo actual.
        hijo.padre = self

        # Agregamos el nodo indicado a los hijos del nodo.
        self.hijos.append(hijo)

        # Devolvemos el nodo hijo agregado.
        return hijo

    def expandir(self,
                 problema):
        """
        Se encarga de crear todos los nodos hijos aplicando todas las
        acciones posibles.
        Argumentos:
        - problema: definición de problema con acciones y costes.
        Devuelve: lista con los hijos generados.
        """
        # Comprobaciones.
        if not problema:
            raise "No se ha indicado una defición de problema"
        if not problema.acciones:
            raise "El problema no tiene definidas las acciones"
        if not problema.costes:
            raise "El problema no tiene definidos los costes"

        # Reiniciamos la lista de los hijos.
        self.hijos = []

        # Si aún no tenemos acciones
        if not self.acciones:
            # Miramos si el estado está en las acciones del problema.
            if self.estado.nombre not in problema.acciones.keys():
                return self.hijos

            # Obtenemos las acciones del estado.
            self.acciones = problema.acciones[self.estado.nombre]

        # Por cada acción que se puede llevar a cabo.
        for accion in self.acciones.keys():
            # Aplicamos la acción para ver el resultado.
            accion_hijo = Accion(nombre=accion)
            nuevo_estado = problema.resultado(estado=self.estado,
                                              accion=accion_hijo)

            # Miramos si el nuevo estado tiene acciones asociadas.
            acciones_nuevo = {}
            if nuevo_estado.nombre in problema.acciones.keys():
                acciones_nuevo = problema.acciones[nuevo_estado.nombre]

            # Creamos el nodo hijo.
            hijo = Nodo(estado=nuevo_estado,
                        accion=accion_hijo,
                        acciones=acciones_nuevo)

            # Calculamos el coste del camino (para ahorrar cálculos)
            coste = self.padre.coste if self.padre else 0
            coste += problema.coste_accion(estado=self.estado,
                                           accion=accion_hijo)
            hijo.coste = coste

            # Lo agregamos al nodo actual como hijo.
            self.agregar(hijo=hijo)

        # Devolvemos los hijos generados.
        return self.hijos


# %% --- MAIN ---

if __name__ == "__main__":
    """
    Ejemplos de problemas, estados, acciones y árboles.
    """
    # Se va a definir un mapa simplificado de la Península Ibérica.
    # Con varias ciudades destacadas y sus distancias por carretera.

    # Definimos las acciones.
    accN = Accion("norte")
    accS = Accion("sur")
    accE = Accion("este")
    accO = Accion("oeste")

    # Definimos los estados (ciudades).
    coruna = Estado(nombre="A Coruña",
                    acciones=[accS, accE])

    bilbao = Estado(nombre="Bilbao",
                    acciones=[accS, accE, accO])

    barcelona = Estado(nombre="Barcelona",
                       acciones=[accS, accO])

    lisboa = Estado(nombre="Lisboa",
                    acciones=[accN, accS, accE])

    madrid = Estado(nombre="Madrid",
                    acciones=[accN, accS, accE, accO])

    valencia = Estado(nombre="Valencia",
                      acciones=[accN, accS, accO])

    faro = Estado(nombre="Faro",
                  acciones=[accN, accE])

    sevilla = Estado(nombre="Sevilla",
                     acciones=[accN, accE, accO])

    granada = Estado(nombre="Granada",
                     acciones=[accN, accO])

    # Definimos las acciones de cada nodo (viajes entre ciudades).
    acciones = {"A Coruña": {"sur": lisboa,
                             "este": bilbao},
                "Bilbao": {"sur": madrid,
                           "este": barcelona,
                           "oeste": coruna},
                "Barcelona": {"sur": valencia,
                              "oeste": bilbao},
                "Lisboa": {"norte": coruna,
                           "sur": faro,
                           "este": madrid},
                "Madrid": {"norte": bilbao,
                           "sur": sevilla,
                           "este": valencia,
                           "oeste": lisboa},
                "Valencia": {"norte": barcelona,
                             "sur": granada,
                             "oeste": madrid},
                "Faro": {"norte": lisboa,
                         "este": sevilla},
                "Sevilla": {"norte": madrid,
                            "este": granada,
                            "oeste": faro},
                "Granada": {"norte": valencia,
                            "oeste": sevilla}}

    # Definimos los costes de aplicar cada acción en cada estado.
    # En este caso, son los kilómetros por carretera entre ciudades.
    costes = {"A Coruña": {"sur": 608,
                           "este": 545},
              "Bilbao": {"sur": 408,
                         "este": 613,
                         "oeste": 545},
              "Barcelona": {"sur": 350,
                            "oeste": 613},
              "Lisboa": {"norte": 608,
                         "sur": 278,
                         "este": 624},
              "Madrid": {"norte": 408,
                         "sur": 534,
                         "este": 357,
                         "oeste": 624},
              "Valencia": {"norte": 350,
                           "sur": 487,
                           "oeste": 357},
              "Faro": {"norte": 278,
                       "este": 200},
              "Sevilla": {"norte": 534,
                          "este": 252,
                          "oeste": 200},
              "Granada": {"norte": 487,
                          "oeste": 252}}

    # Definimos el problema: ir de Faro a Barcelona.
    problema = Problema(estado_inicial=faro,
                        estados_objetivos=[barcelona],
                        acciones=acciones,
                        costes=costes)

    # ------------------------------------------------------------------------
    # Más adelante usaremos algoritmos, pero de momento vamos a construir
    # un árbol cuya raíz sea Faro y cuyo objetivo (hoja) sea Barcelona.
    # ------------------------------------------------------------------------

    # El nodo raíz del árbol estará en Faro.
    acciones_faro = problema.acciones["Faro"]
    n_faro = Nodo(estado=faro,
                  acciones=acciones_faro)

    # Probamos a expandir sus hijos.
    hijos_faro = n_faro.expandir(problema=problema)
    print("Hijos de {0}:".format(n_faro.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_faro])

    # Aplicamos la acción de ir al este para llegar a Sevilla.
    este_sevilla = problema.resultado(faro, accE)
    print("{0}".format(este_sevilla.nombre))

    # Agregamos Sevilla a los hijos del nodo de Faro.
    acciones_sevilla = problema.acciones["Sevilla"]
    nodo_sevilla = Nodo(estado=este_sevilla,
                        accion=accE,
                        acciones=acciones_sevilla)
    n_faro.agregar(nodo_sevilla)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_sevilla)
    print("Coste: {0}".format(kms))

    # Probamos a expandir sus hijos.
    hijos_sevila = nodo_sevilla.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_sevilla.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_sevila])

    # Aplicamos la acción de ir al norte para llegar a Madrid.
    norte_madrid = problema.resultado(nodo_sevilla.estado, accN)
    print("{0}".format(norte_madrid.nombre))

    # Agregamos Madrid a los hijos del nodo de Sevilla.
    acciones_madrid = problema.acciones["Madrid"]
    nodo_madrid = Nodo(estado=norte_madrid,
                       accion=accN,
                       acciones=acciones_madrid)
    nodo_sevilla.agregar(nodo_madrid)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_madrid)
    print("Coste: {0}".format(kms))

    # Todavía no hemos llegado.
    no_fin = problema.es_objetivo(nodo_madrid.estado)
    print("Destino: {0}".format(no_fin))

    # Probamos a expandir sus hijos.
    hijos_madrid = nodo_madrid.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_madrid.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_madrid])

    # Aplicamos la acción de ir al este para llegar a Valencia.
    este_valencia = problema.resultado(nodo_madrid.estado, accE)
    print("{0}".format(este_valencia.nombre))

    # Agregamos Valencia a los hijos del nodo Madrid.
    acciones_valencia = problema.acciones["Valencia"]
    nodo_valencia = Nodo(estado=este_valencia,
                         accion=accE,
                         acciones=acciones_valencia)
    nodo_madrid.agregar(nodo_valencia)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_valencia)
    print("Coste: {0}".format(kms))

    # Probamos a expandir sus hijos.
    hijos_valencia = nodo_valencia.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_valencia.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_valencia])

    # Aplicamos la acción de ir al norte para llegar a Barcelona.
    norte_barcelona = problema.resultado(nodo_valencia.estado, accN)
    print("{0}".format(norte_barcelona.nombre))

    # Agregamos Barcelona a los hijos del nodo Valencia.
    acc_barcelona = problema.acciones["Barcelona"]
    nodo_barcelona = Nodo(estado=norte_barcelona,
                          accion=accN,
                          acciones=acc_barcelona)
    nodo_valencia.agregar(nodo_barcelona)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_barcelona)
    print("Coste: {0}".format(kms))

    # Ahora si que hemos llegado.
    fin = problema.es_objetivo(nodo_barcelona.estado)
    print("Destino: {0}".format(fin))
