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
            raise ValueError("No se ha indicado el nombre de la acción")

        # Guardamos los parámetros pasados.
        self.nombre = nombre

    def __str__(self):
        """
        Representación en modo texto de la acción.
        """
        return self.nombre

    def __repr__(self):
        """
        Representación de la acción para depuración.
        """
        return "Accion({0})".format(self)


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
            raise ValueError("No se ha indicado el nombre del estado")

        # Puede que no haya acciones a aplicar.
        if acciones is None:
            acciones = []

        # Guardamos los parámetros pasados.
        self.nombre = nombre
        self.acciones = acciones

    def __str__(self):
        """
        Representación en modo texto del estado.
        """
        return self.nombre

    def __repr__(self):
        """
        Representación del texto para depuración.
        """
        return "Estado({0})".format(self)


# %% --- PROBLEMA ---

class Problema:
    """
    Clase que representa un problema a resolver con un grafo.
    """

    def __init__(self,
                 estado_inicial,
                 estados_objetivos,
                 acciones,
                 costes=None,
                 heuristicas=None,
                 infinito=99999):
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
        - heuristicas: diccionario donde la clave es el nombre de un estado y
                       el valor es otro diccionario con la clave el nombre de
                       un estado objetivo y como valor un número.
        - infinito: mayor cantidad posible a manejar (costes, heurísticas...)
        """
        # Comprobaciones.
        if not estado_inicial:
            raise ValueError("No se ha indicado un estado inicial")
        if not estados_objetivos:
            raise ValueError("No se ha indicado al menos un estado objetivo")
        if not acciones:
            raise ValueError("No se ha indicado ninguna acción")

        # Guardamos los parámetros pasados.
        self.estado_inicial = estado_inicial
        self.estados_objetivos = estados_objetivos
        self.acciones = acciones
        self.costes = costes
        self.heuristicas = heuristicas
        self.infinito = infinito

        # Si no hay costes, ponemos todos los costes a 1.
        if not self.costes:
            self.costes = {}
            for estado in self.acciones.keys():
                self.costes[estado] = {}
                for accion in self.acciones[estado].keys():
                    self.costes[estado][accion] = 1

        # Si no hay heurísticas, ponemos todas a infinito.
        if not self.heuristicas:
            self.heuristicas = {}
            for estado in self.acciones.keys():
                self.heuristicas[estado] = {}
                for objetivo in self.estados_objetivos:
                    self.heuristicas[estado][objetivo] = infinito

    def __str__(self):
        """
        Representación en modo texto del problema.
        """
        msg = "Estado Inicial: {0}; Objetivos: {1}"
        return msg.format(self.estado_inicial.nombre,
                          self.estados_objetivos)

    def __repr__(self):
        """
        Representación del problema para depuración.
        """
        return "Problema({0})".format(self)

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
            raise ValueError("No se indicó estado al que aplicar acción")
        if not accion:
            raise ValueError("No se indicó acción a aplicar")

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
            raise ValueError("No se ha indicado estado a calcular un coste")
        if not accion:
            raise ValueError("No se ha indicado acción para calcular su coste")

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
            raise ValueError("No se indicó nodo a calcular su coste de camino")

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
            raise ValueError("No ha indicado el estado asociado el nodo")

        # Pueden no indicar hijos.
        if hijos is None:
            hijos = []

        # Guardamos los parámetros pasados.
        self.estado = estado
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos = []
        self.hijos.extend(hijos)

        # Coste de camino hasta nodo (evitar repetir cálculos)
        # Irá aumentando cuando se llame al método "expandir".
        self.coste = 0

        # Heurísticas estimadas hasta los nodos objetivos.
        # Irá disminuyendo cuando se llame al método "expandir".
        self.heuristicas = {}

        # Suma del coste más las heurísticas.
        # Irá recalculándose cuando se llame al método "expandir".
        self.valores = {}

        # En algunos algoritmos se necesitan valores auxiliares.
        # Los vamos a llamar por las letras del alfabeto griego.
        self.alfa = 0
        self.beta = 0

    def __str__(self):
        """
        Representación en modo texto del nodo.
        """
        return self.estado.nombre

    def __repr__(self):
        """
        Representación del nodo para depuración.
        """
        return "Nodo({0})".format(self)

    def expandir(self,
                 problema):
        """
        Se encarga de crear todos los nodos hijos aplicando todas las
        acciones posibles.
        Argumentos:
        - problema: definición de problema con acciones, costes y heurísticas.
        Devuelve: lista con los hijos generados.
        """
        # Comprobaciones.
        if not problema:
            raise ValueError("No se ha indicado una defición de problema")
        if not problema.acciones:
            raise ValueError("El problema no tiene definidas las acciones")
        if not problema.costes:
            raise ValueError("El problema no tiene definidos los costes")
        if not problema.heuristicas:
            raise ValueError("El problema no tiene definidas las heurísticas")

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

            # Obtenemos las heurísticas hasta los objetivos.
            hijo.heuristicas = problema.heuristicas[hijo.estado.nombre]

            # Calculamos el valor.
            hijo.valores = {estado: heuristica + hijo.coste
                            for estado, heuristica
                            in hijo.heuristicas.items()}

            # Lo agregamos al nodo actual como hijo.
            hijo.padre = self
            self.hijos.append(hijo)

        # Devolvemos los hijos generados.
        return self.hijos

    def hijo_mejor(self,
                   metrica="valor",
                   criterio="menor",
                   objetivos=None):
        """
        De todos los hijos, devuelve el que tiene mejor cantidad a los
        objetivos indicados (necesita que ya se hayan expandido antes).
        Argumentos:
        - metrica: con qué cantidad se calculará el menor. Los valores posibles
                   son 'valor', 'heuristica', 'coste', 'alfa', 'beta'.
        - criterio: si se obtendrá el 'menor' o el 'mayor'.
        - objetivos: estados objetivos para los que hacer los cálculos en caso
                     de que la métrica no sea 'coste', 'alfa' o 'beta'.
        """
        # Comprobaciones.
        if metrica not in ("valor", "heuristica", "coste", "alfa", "beta"):
            msg = "Se indicó una métrica desconocida: {0}"
            raise ValueError(msg.format(metrica))
        if criterio not in ("menor", "mayor"):
            msg = "Se indicó un criterio desconocido: {0}"
            raise ValueError(msg.format(criterio))
        if metrica in ("valor", "heuristica") and not objetivos:
            raise ValueError("No se indicó objetivo")

        # Si no hay hijos aun, terminamos.
        if not self.hijos:
            return None

        # Cogemos el primer hijo como el mejor, de momento.
        mejor = self.hijos[0]

        # Recorremos el resto de hijos para ver si alguno es mejor.
        for hijo in self.hijos:
            # Por cada uno de los objetivos.
            for objetivo in objetivos:
                # Si nos piden el valor
                if "valor" == metrica:
                    # Si este hijo es mejor que el actual, lo cogemos.
                    valor_hijo = hijo.valores[objetivo]
                    valor_mejor = mejor.valores[objetivo]
                    if("menor" == criterio and
                       valor_hijo < valor_mejor):
                        mejor = hijo
                    elif("mayor" == criterio and
                         valor_hijo > valor_mejor):
                        mejor = hijo
                # Si nos piden la heurística.
                elif "heuristica" == metrica:
                    # Si este hijo es mejor que el actual, lo cogemos.
                    heuristica_hijo = hijo.heuristicas[objetivo]
                    heuristica_mejor = mejor.heuristicas[objetivo]
                    if("menor" == criterio and
                       heuristica_hijo < heuristica_mejor):
                        mejor = hijo
                    elif("mayor" == criterio and
                         heuristica_hijo > heuristica_mejor):
                        mejor = hijo
                # Si nos piden el coste
                elif "coste" == metrica:
                    # Si este hijo es mejor que el actual, lo cogemos.
                    if("menor" == criterio and
                       hijo.coste_camino < mejor.coste_camino):
                        mejor = hijo
                    elif("mayor" == criterio and
                         hijo.coste_camino > mejor.coste_camino):
                        mejor = hijo
                # Si nos piden el auxiliar alfa
                elif "alfa" == metrica:
                    # Si este hijo es mejor que el actual, lo cogemos.
                    if("menor" == criterio and
                       hijo.alfa < mejor.alfa):
                        mejor = hijo
                    elif("mayor" == criterio and
                         hijo.alfa > mejor.alfa):
                        mejor = hijo
                # Si nos piden el auxiliar beta
                elif "beta" == metrica:
                    # Si este hijo es mejor que el actual, lo cogemos.
                    if("menor" == criterio and
                       hijo.beta < mejor.beta):
                        mejor = hijo
                    elif("mayor" == criterio and
                         hijo.beta > mejor.beta):
                        mejor = hijo

        # Devolvemos el mejor.
        return mejor


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

    # Definimos las hurísticas para ir entre cada par de estados.
    heuristicas = {"A Coruña": {"A Coruña": 0,
                                "Bilbao": 443,
                                "Barcelona": 895,
                                "Lisboa": 522,
                                "Madrid": 509,
                                "Valencia": 797,
                                "Faro": 687,
                                "Sevilla": 696,
                                "Granada": 799},
                   "Bilbao": {"A Coruña": 443,
                              "Bilbao": 0,
                              "Barcelona": 468,
                              "Lisboa": 725,
                              "Madrid": 323,
                              "Valencia": 473,
                              "Faro": 807,
                              "Sevilla": 703,
                              "Granada": 678},
                   "Barcelona": {"A Coruña": 895,
                                 "Bilbao": 468,
                                 "Barcelona": 0,
                                 "Lisboa": 1005,
                                 "Madrid": 504,
                                 "Valencia": 303,
                                 "Faro": 1003,
                                 "Sevilla": 828,
                                 "Granada": 681},
                   "Lisboa": {"A Coruña": 522,
                              "Bilbao": 725,
                              "Barcelona": 1005,
                              "Lisboa": 0,
                              "Madrid": 502,
                              "Valencia": 760,
                              "Faro": 189,
                              "Sevilla": 314,
                              "Granada": 513},
                   "Madrid": {"A Coruña": 509,
                              "Bilbao": 323,
                              "Barcelona": 504,
                              "Lisboa": 502,
                              "Madrid": 0,
                              "Valencia": 303,
                              "Faro": 527,
                              "Sevilla": 390,
                              "Granada": 359},
                   "Valencia": {"A Coruña": 797,
                                "Bilbao": 473,
                                "Barcelona": 303,
                                "Lisboa": 760,
                                "Madrid": 303,
                                "Valencia": 0,
                                "Faro": 725,
                                "Sevilla": 540,
                                "Granada": 379},
                   "Faro": {"A Coruña": 708,
                            "Bilbao": 807,
                            "Barcelona": 1003,
                            "Lisboa": 189,
                            "Madrid": 527,
                            "Valencia": 725,
                            "Faro": 0,
                            "Sevilla": 195,
                            "Granada": 404},
                   "Sevilla": {"A Coruña": 696,
                               "Bilbao": 703,
                               "Barcelona": 828,
                               "Lisboa": 314,
                               "Madrid": 390,
                               "Valencia": 540,
                               "Faro": 195,
                               "Sevilla": 0,
                               "Granada": 210},
                   "Granada": {"A Coruña": 799,
                               "Bilbao": 678,
                               "Barcelona": 681,
                               "Lisboa": 513,
                               "Madrid": 359,
                               "Valencia": 379,
                               "Faro": 404,
                               "Sevilla": 210,
                               "Granada": 0}}

    # Definimos el problema: ir de Faro a Barcelona.
    problema = Problema(estado_inicial=faro,
                        estados_objetivos=[barcelona],
                        acciones=acciones,
                        costes=costes,
                        heuristicas=heuristicas)

    # ------------------------------------------------------------------------
    # Más adelante usaremos algoritmos, pero de momento vamos a construir
    # un árbol cuya raíz sea Faro y cuyo objetivo (hoja) sea Barcelona.
    # ------------------------------------------------------------------------

    # El nodo raíz del árbol estará en Faro.
    acciones_faro = problema.acciones["Faro"]
    nodo_faro = Nodo(estado=faro,
                     acciones=acciones_faro)

    # Probamos a expandir sus hijos.
    hijos_faro = nodo_faro.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_faro.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_faro])

    # Mostramos el hijo con menor valor.
    menor = nodo_faro.hijo_mejor(objetivos=["Barcelona"])
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores["Barcelona"]))

    # Aplicamos la acción de ir al este para llegar a Sevilla.
    este_sevilla = problema.resultado(faro, accE)
    print("{0}".format(este_sevilla.nombre))

    # Agregamos Sevilla a los hijos del nodo de Faro.
    acciones_sevilla = problema.acciones["Sevilla"]
    nodo_sevilla = Nodo(estado=este_sevilla,
                        accion=accE,
                        acciones=acciones_sevilla)
    nodo_sevilla.padre = nodo_faro
    nodo_faro.hijos.append(nodo_sevilla)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_sevilla)
    print("Coste: {0}".format(kms))

    # Indicamos la heurística hasta el objetivo.
    heuristica = problema.heuristicas["Sevilla"]["Barcelona"]
    print("Heurística: {0}".format(heuristica))

    # Indicamos la suma del coste más la heurística.
    valor = heuristica + kms
    print("Valor: {0}".format(valor))

    # Probamos a expandir sus hijos.
    hijos_sevilla = nodo_sevilla.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_sevilla.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_sevilla])

    # Mostramos el hijo con menor valor.
    menor = nodo_sevilla.hijo_mejor(objetivos=["Barcelona"])
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores["Barcelona"]))

    # Aplicamos la acción de ir al norte para llegar a Madrid.
    norte_madrid = problema.resultado(nodo_sevilla.estado, accN)
    print("{0}".format(norte_madrid.nombre))

    # Agregamos Madrid a los hijos del nodo de Sevilla.
    acciones_madrid = problema.acciones["Madrid"]
    nodo_madrid = Nodo(estado=norte_madrid,
                       accion=accN,
                       acciones=acciones_madrid)
    nodo_madrid.padre = nodo_sevilla
    nodo_sevilla.hijos.append(nodo_madrid)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_madrid)
    print("Coste: {0}".format(kms))

    # Indicamos la heurística hasta el objetivo.
    heuristica = problema.heuristicas["Madrid"]["Barcelona"]
    print("Heurística: {0}".format(heuristica))

    # Indicamos la suma del coste más la heurística.
    valor = heuristica + kms
    print("Valor: {0}".format(valor))

    # Todavía no hemos llegado.
    no_fin = problema.es_objetivo(nodo_madrid.estado)
    print("Destino: {0}".format(no_fin))

    # Probamos a expandir sus hijos.
    hijos_madrid = nodo_madrid.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_madrid.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_madrid])

    # Mostramos el hijo con menor valor.
    menor = nodo_madrid.hijo_mejor(objetivos=["Barcelona"])
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores["Barcelona"]))

    # Aplicamos la acción de ir al este para llegar a Valencia.
    este_valencia = problema.resultado(nodo_madrid.estado, accE)
    print("{0}".format(este_valencia.nombre))

    # Agregamos Valencia a los hijos del nodo Madrid.
    acciones_valencia = problema.acciones["Valencia"]
    nodo_valencia = Nodo(estado=este_valencia,
                         accion=accE,
                         acciones=acciones_valencia)
    nodo_valencia.padre = nodo_madrid
    nodo_madrid.hijos.append(nodo_valencia)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_valencia)
    print("Coste: {0}".format(kms))

    # Indicamos la heurística hasta el objetivo.
    heuristica = problema.heuristicas["Valencia"]["Barcelona"]
    print("Heurística: {0}".format(heuristica))

    # Indicamos la suma del coste más la heurística.
    valor = heuristica + kms
    print("Valor: {0}".format(valor))

    # Probamos a expandir sus hijos.
    hijos_valencia = nodo_valencia.expandir(problema=problema)
    print("Hijos de {0}:".format(nodo_valencia.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_valencia])

    # Mostramos el hijo con menor valor.
    menor = nodo_valencia.hijo_mejor(objetivos=["Barcelona"])
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores["Barcelona"]))

    # Aplicamos la acción de ir al norte para llegar a Barcelona.
    norte_barcelona = problema.resultado(nodo_valencia.estado, accN)
    print("{0}".format(norte_barcelona.nombre))

    # Agregamos Barcelona a los hijos del nodo Valencia.
    acc_barcelona = problema.acciones["Barcelona"]
    nodo_barcelona = Nodo(estado=norte_barcelona,
                          accion=accN,
                          acciones=acc_barcelona)
    nodo_barcelona.padre = nodo_valencia
    nodo_valencia.hijos.append(nodo_barcelona)

    # Indicamos el coste de camino recorrido.
    kms = problema.coste_camino(nodo_barcelona)
    print("Coste: {0}".format(kms))

    # Indicamos la heurística hasta el objetivo.
    heuristica = problema.heuristicas["Barcelona"]["Barcelona"]
    print("Heurística: {0}".format(heuristica))

    # Indicamos la suma del coste más la heurística.
    valor = heuristica + kms
    print("Valor: {0}".format(valor))

    # Ahora si que hemos llegado.
    fin = problema.es_objetivo(nodo_barcelona.estado)
    print("Destino: {0}".format(fin))
