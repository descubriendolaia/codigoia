#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diferentes algoritmos de búsqueda informada en grafos.
Parten del algoritmo de búsqueda en grafos de coste uniforme y lo amplían.
Aparte del coste del camino, se usará una función heurística que estimará el
coste hasta los objetivos y calculará un valor por el cual se escogerá el
siguiente nodo a expandir y visitar.
"""
from grafos import Accion, Estado, Problema, Nodo


# %% --- VORAZ / GRADIENTE / MÁXIMA PENDIENTE ---

def voraz(
        problema,
        log=False,
        paso_a_paso=False):
    """
    Búsqueda en grafos voraz (greedy search).
    No tiene en cuenta el coste del camino recorrido, sólo la heurística.
    Argumentos:
    - problema: definición del problema a resolver.
    - log: Si se mostrarán los pasos que se van realizando.
    - paso_a_paso: si se detendrá en cada paso para poder analizarlo.
    Devuelve: referencia al nodo con uno de los estado objetivo. A partir de
              él y siguiendo sus nodos padres, se obtendrá la solución.
              Si no encuentra solución, devuelve "None".
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema a resolver")

    # Obtenemos el nodo raíz.
    raiz = crea_nodo_raiz(problema=problema)

    # Definimos la frontera y agregamos el nodo raíz.
    frontera = [raiz, ]

    # Definimos el conjunto de los estados explorados.
    explorados = set()

    # Entramos en el bucle principal.
    while True:
        # Mostramos la frontera y explorada.
        if log:
            log_frontera = [nodo.estado.nombre
                            for nodo in frontera]
            log_explorados = [estado.nombre
                              for estado in explorados]
            print("----- NUEVO CICLO -----")
            msg = "Frontera: {0}"
            print(msg.format(log_frontera))
            msg = "Explorados: {0}"
            print(msg.format(log_explorados))

        # Si frontera está vacía, terminamos.
        if not frontera:
            return None

        # Obtenemos el siguiente nodo.
        nodo = frontera.pop(0)
        if log:
            msg = "Nodo: {0}"
            print(msg.format(nodo.estado.nombre))
            log_frontera = [nodo.estado.nombre
                            for nodo in frontera]
            msg = "Frontera: {0}"
            print(msg.format(log_frontera))

        # Miramos si el nodo es ya un objetivo.
        if problema.es_objetivo(estado=nodo.estado):
            if log:
                msg = "Objetivo: {0}"
                print(msg.format(nodo.estado.nombre))
            return nodo

        # Agregamos su estado al conjunto de explorados.
        explorados.add(nodo.estado)
        if log:
            log_explorados = [estado.nombre
                              for estado in explorados]
            msg = "Explorados: {0}"
            print(msg.format(log_explorados))

        # Si el nodo no tiene acciones, pasamos al siguiente.
        if not nodo.acciones:
            if log:
                print("No hay Acciones")
            continue

        # Por cada una de las acciones que se pueden hacer.
        for nombre_accion in nodo.acciones.keys():
            # Indicamos la acción.
            if log:
                msg = "   Accion: {0}"
                print(msg.format(nombre_accion))

            # Creamos un nodo hijo.
            accion = Accion(nombre=nombre_accion)
            hijo = crea_nodo_hijo(problema=problema,
                                  padre=nodo,
                                  accion=accion)
            nombre_hijo = hijo.estado.nombre
            if log:
                msg = "   Hijo: {0}"
                print(msg.format(nombre_hijo))

            # Si el estado del hijo no ha sido explorado
            # y tampoco está en la frontera.
            estados_frontera = [nodo.estado
                                for nodo in frontera]
            if hijo.estado in explorados or hijo.estado in estados_frontera:
                # Miramos si el estado está en algún nodo de la frontera.
                buscar = [nodo
                          for nodo in frontera
                          if nodo.estado == hijo.estado]
                if buscar:
                    # Indicamos que el estado ya existía en la frontera.
                    if log:
                        msg = "   Estado En Frontera: {0}"
                        print(msg.format(nombre_hijo))

                    # Obtenemos las mejores heurísticas.
                    heuristic_hijo = [hijo.heuristicas[objetivo.nombre]
                                      for objetivo
                                      in problema.estados_objetivos]
                    heuristic_buscar = [buscar[0].heuristicas[objetivo.nombre]
                                        for objetivo
                                        in problema.estados_objetivos]
                    minimo_hijo = min(heuristic_hijo)
                    minimo_buscar = min(heuristic_buscar)

                    # Si tiene mejor heurística el hijo que el de la frontera.
                    if log:
                        msg = "      Heurística Hijo: {0}"
                        print(msg.format(minimo_hijo))
                        msg = "      Heurística Frontera: {0}"
                        print(msg.format(minimo_buscar))
                    if minimo_hijo < minimo_buscar:
                        # Indicamos que vamos a sustituir el nodo frontera.
                        if log:
                            print("      Sustituido: SÍ")

                        # Sustituimos el de la frontera por el del hijo.
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
                        if log:
                            msg = "      Nueva Heurística: {0}"
                            print(msg.format(minimo_hijo))
                    else:
                        # Indicamos que no se sustituye.
                        if log:
                            print("      Sustituido: NO")
            else:
                # Lo agregamos a la frontera.
                frontera.append(hijo)
                if log:
                    msg = "   Añade Frontera: {0}"
                    print(msg.format(nombre_hijo))

        # Si nos piden ir paso a paso.
        if paso_a_paso:
            input("Pulsa la tecla 'Enter' para continuar.")


# %% --- FUNCIONES AUXILIARES ---

def crea_nodo_raiz(problema):
    """
    Método auxiliar que ayudará a crear nodos raíz de los métodos que
    implementan algoritmos de búsqueda informada.
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema")

    # Obtenemos el estado inicial del problema.
    estado_raiz = problema.estado_inicial

    # Miramos si el estado tiene acciones asociadas.
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]

    # Creamos el nodo raíz.
    raiz = Nodo(estado=estado_raiz,
                acciones=acciones_raiz)

    # No habrá aun coste de camino.
    raiz.coste = 0

    # Obtenemos las heurísticas hasta los objetivos.
    raiz.heuristicas = problema.heuristicas[estado_raiz.nombre]

    # Calculamos el valor sólo con la heurística.
    raiz.valores = {estado: heuristica
                    for estado, heuristica
                    in raiz.heuristicas.items()}

    # Devolvemos el nodo raíz creado.
    return raiz


def crea_nodo_hijo(problema,
                   padre,
                   accion):
    """
    Método auxiliar que ayudará a crear nodos hijos a los métodos que
    implementan algoritmos de búsqueda informada.
    Argumentos:
    - problema: definición del problema a resolver.
    - padre: nodo padre del nodo hijo a crear. Se agrega a los hijos de él.
    - accion: acción que ha provocado la creación de este nodo hijo.
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema")
    if not padre:
        raise ValueError("No se indicó el nodo padre")
    if not accion:
        raise ValueError("No se indicó la acción")

    # Creamos el nuevo estado.
    nuevo_estado = problema.resultado(estado=padre.estado,
                                      accion=accion)

    # Miramos si el nuevo estado tiene acciones asociadas.
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]

    # Creamos el nodo hijo.
    hijo = Nodo(estado=nuevo_estado,
                accion=accion,
                acciones=acciones_nuevo)

    # Calculamos el coste del camino (para ahorrar cálculos)
    coste = padre.coste
    coste += problema.coste_accion(estado=padre.estado,
                                   accion=accion)
    hijo.coste = coste

    # Obtenemos las heurísticas hasta los objetivos.
    hijo.heuristicas = problema.heuristicas[hijo.estado.nombre]

    # Calculamos el valor.
    hijo.valores = {estado: heuristica + hijo.coste
                    for estado, heuristica
                    in hijo.heuristicas.items()}

    # Lo agregamos al nodo actual como hijo.
    padre.agregar(hijo=hijo)

    # Devolvemos el hijo.
    return hijo


def muestra_solucion(objetivo=None,
                     es_bidireccional=False,
                     bidireccional=(None, None),
                     segundos=0):
    """
    Muestra la solución encuentrada a partir de un nodo objetivo.
    Argumentos:
    - objetivo: nodo objetivo encontrado por un algoritmo.
    - es_bidireccional: la solución es diferente al resto.
    - bidireccional: esta búsqueda devuelve un par de nodos con estados comunes
                     que deben combinarse para obtener la solución final.
    - tiempo: cantidad de tiempo que ha tardado en ejecutarse el algoritmo.
    """
    # Mostramos la solución.
    print()
    print("--------------------")
    print("----- SOLUCIÓN -----")
    print("--------------------")

    # Si nos pasan el tiempo.
    if tiempo > 0:
        msg = "Tiempo: {0} milisegundos"
        print(msg.format(tiempo*1000))
        print("--------------------")

    # Si no hay objetivo, no hay solución.
    if not objetivo:
        print("No hay solución")
        return

    # Recorremos desde el nodo objetivo al nodo raíz.
    nodo = objetivo
    while nodo:
        # Mostramos los datos de ese nodo.
        msg = "Estado {0}, Valor {1}"
        estado = nodo.estado.nombre
        valores = [nodo.valores[objetivo.nombre]
                   for objetivo
                   in problema.estados_objetivos]
        valor = min(valores)
        print(msg.format(estado, valor))

        msg = "  Coste: {0}"
        coste_total = nodo.coste
        print(msg.format(coste_total))

        msg = "  Heurística: {0}"
        heuristicas = [nodo.heuristicas[objetivo.nombre]
                       for objetivo
                       in problema.estados_objetivos]
        heuristica = min(heuristicas)
        print(msg.format(heuristica))

        # Mostramos la acción que llevó a ese nodo.
        if nodo.accion:
            accion = nodo.accion.nombre
            padre = nodo.padre.estado
            coste = problema.coste_accion(estado=padre,
                                          accion=nodo.accion)
            if accion:
                msg = "<--- {0} [{1}] ---"
                print(msg.format(accion, coste))

        # Pasamos al nodo padre.
        nodo = nodo.padre


# %% --- MAIN ---

if __name__ == "__main__":
    """
    Ejemplos de búsqueda informada en grafos.
    """
    # ------------------------------------------------------------------------
    # DEFINICIÓN DEL PROGRAMA
    # ------------------------------------------------------------------------

    # El problema consiste en buscar ruta para viajar entre ciudades.
    # Esta búsqueda se realizará con varios algoritmos para ver diferencias.

    # Definimos las acciones (direcciones de puntos cardinales).
    accN = Accion("N")
    accS = Accion("S")
    accE = Accion("E")
    accO = Accion("O")
    accNE = Accion("NE")
    accNO = Accion("NO")
    accSE = Accion("SE")
    accSO = Accion("SO")

    # Definimos los estados (ciudades).
    lanoi = Estado(nombre="Lanoi",
                   acciones=[accNE])
    nohoi = Estado(nombre="Nohoi",
                   acciones=[accSO, accNO, accNE])
    ruun = Estado(nombre="Ruun",
                  acciones=[accNO, accNE, accE, accSE])
    milos = Estado(nombre="Milos",
                   acciones=[accO, accSO, accN])
    ghiido = Estado(nombre="Ghiido",
                    acciones=[accN, accE, accSE])
    kuart = Estado(nombre="Kuart",
                   acciones=[accO, accSO, accNE])
    boomon = Estado(nombre="Boomon",
                    acciones=[accN, accSO])
    goorum = Estado(nombre="Goorum",
                    acciones=[accO, accS])
    shiphos = Estado(nombre="Shiphos",
                     acciones=[accO, accE])
    nokshos = Estado(nombre="Nokshos",
                     acciones=[accNO, accS, accE])
    pharis = Estado(nombre="Pharis",
                    acciones=[accNO, accSO])
    khamin = Estado(nombre="Khamin",
                    acciones=[accSE, accNO, accO])
    tarios = Estado(nombre="Tarios",
                    acciones=[accO, accNO, accNE, accE])
    peranna = Estado(nombre="Peranna",
                     acciones=[accO, accE])
    khandan = Estado(nombre="Khandan",
                     acciones=[accO, accS])
    tawa = Estado(nombre="Tawa",
                  acciones=[accSO, accSE, accNE])
    theer = Estado(nombre="Theer",
                   acciones=[accSO, accSE])
    roria = Estado(nombre="Roria",
                   acciones=[accNO, accSO, accE])
    kosos = Estado(nombre="Kosos",
                   acciones=[accO])

    # Definimos las acciones de cada nodo (viajes entre ciudades).
    acciones = {"Lanoi": {"NE": nohoi},
                "Nohoi": {"SO": lanoi,
                          "NO": ruun,
                          "NE": milos},
                "Ruun": {"NO": ghiido,
                         "NE": kuart,
                         "E": milos,
                         "SE": nohoi},
                "Milos": {"O": ruun,
                          "SO": nohoi,
                          "N": khandan},
                "Ghiido": {"N": nokshos,
                           "E": kuart,
                           "SE": ruun},
                "Kuart": {"O": ghiido,
                          "SO": ruun,
                          "NE": boomon},
                "Boomon": {"N": goorum,
                           "SO": kuart},
                "Goorum": {"O": shiphos,
                           "S": boomon},
                "Shiphos": {"O": nokshos,
                            "E": goorum},
                "Nokshos": {"NO": pharis,
                            "S": ghiido,
                            "E": shiphos},
                "Pharis": {"NO": khamin,
                           "SO": nokshos},
                "Khamin": {"SE": pharis,
                           "NO": tawa,
                           "O": tarios},
                "Tarios": {"O": khamin,
                           "NO": tawa,
                           "NE": roria,
                           "E": peranna},
                "Peranna": {"O": tarios,
                            "E": khandan},
                "Khandan": {"O": peranna,
                            "S": milos},
                "Tawa": {"SO": khamin,
                         "SE": tarios,
                         "NE": theer},
                "Theer": {"SO": tawa,
                          "SE": roria},
                "Roria": {"NO": theer,
                          "SO": tarios,
                          "E": kosos},
                "Kosos": {"O": roria}}

    # Definimos los costes de aplicar cada acción en cada estado.
    # En este caso, son los kilómetros por carretera entre ciudades.
    costes = {"Lanoi": {"NE": 42},
              "Nohoi": {"SO": 42,
                        "NO": 21,
                        "NE": 95},
              "Ruun": {"NO": 88,
                       "NE": 16,
                       "E": 90,
                       "SE": 21},
              "Milos": {"O": 90,
                        "SO": 95,
                        "N": 133},
              "Ghiido": {"N": 17,
                         "E": 92,
                         "SE": 88},
              "Kuart": {"O": 92,
                        "SO": 16,
                        "NE": 83},
              "Boomon": {"N": 8,
                         "SO": 83},
              "Goorum": {"O": 59,
                         "S": 8},
              "Shiphos": {"O": 71,
                          "E": 59},
              "Nokshos": {"NO": 5,
                          "S": 17,
                          "E": 71},
              "Pharis": {"NO": 29,
                         "SO": 5},
              "Khamin": {"SE": 29,
                         "NO": 121,
                         "O": 98},
              "Tarios": {"O": 98,
                         "NO": 83,
                         "NE": 57,
                         "E": 82},
              "Peranna": {"O": 82,
                          "E": 44},
              "Khandan": {"O": 44,
                          "S": 133},
              "Tawa": {"SO": 121,
                       "SE": 83,
                       "NE": 11},
              "Theer": {"SO": 11,
                        "SE": 36},
              "Roria": {"NO": 36,
                        "SO": 57,
                        "E": 104},
              "Kosos": {"O": 104}}

    # Definimos las hurísticas para ir entre cada par de estados.
    heuristicas = {"Lanoi": {"Lanoi": 0,
                             "Nohoi": 32,
                             "Ruun": 43,
                             "Milos": 90,
                             "Ghiido": 81,
                             "Kuart": 50,
                             "Boomon": 90,
                             "Goorum": 95,
                             "Shiphos": 84,
                             "Nokshos": 108,
                             "Pharis": 111,
                             "Khamin": 124,
                             "Tarios": 145,
                             "Peranna": 157,
                             "Khandan": 182,
                             "Tawa": 180,
                             "Theer": 183,
                             "Roria": 174,
                             "Kosos": 224},
                   "Nohoi": {"Lanoi": 32,
                             "Nohoi": 0,
                             "Ruun": 12,
                             "Milos": 72,
                             "Ghiido": 73,
                             "Kuart": 18,
                             "Boomon": 57,
                             "Goorum": 63,
                             "Shiphos": 56,
                             "Nokshos": 93,
                             "Pharis": 97,
                             "Khamin": 107,
                             "Tarios": 117,
                             "Peranna": 125,
                             "Khandan": 150,
                             "Tawa": 153,
                             "Theer": 154,
                             "Roria": 143,
                             "Kosos": 191},
                   "Ruun": {"Lanoi": 43,
                            "Nohoi": 12,
                            "Ruun": 0,
                            "Milos": 71,
                            "Ghiido": 75,
                            "Kuart": 6,
                            "Boomon": 45,
                            "Goorum": 50,
                            "Shiphos": 45,
                            "Nokshos": 87,
                            "Pharis": 89,
                            "Khamin": 100,
                            "Tarios": 105,
                            "Peranna": 103,
                            "Khandan": 140,
                            "Tawa": 140,
                            "Theer": 142,
                            "Roria": 131,
                            "Kosos": 179},
                   "Milos": {"Lanoi": 90,
                             "Nohoi": 72,
                             "Ruun": 71,
                             "Milos": 0,
                             "Ghiido": 145,
                             "Kuart": 70,
                             "Boomon": 76,
                             "Goorum": 81,
                             "Shiphos": 103,
                             "Nokshos": 156,
                             "Pharis": 157,
                             "Khamin": 165,
                             "Tarios": 138,
                             "Peranna": 116,
                             "Khandan": 122,
                             "Tawa": 176,
                             "Theer": 174,
                             "Roria": 159,
                             "Kosos": 172},
                   "Ghiido": {"Lanoi": 81,
                              "Nohoi": 73,
                              "Ruun": 75,
                              "Milos": 145,
                              "Ghiido": 0,
                              "Kuart": 75,
                              "Boomon": 94,
                              "Goorum": 93,
                              "Shiphos": 61,
                              "Nokshos": 34,
                              "Pharis": 37,
                              "Khamin": 53,
                              "Tarios": 112,
                              "Peranna": 150,
                              "Khandan": 187,
                              "Tawa": 134,
                              "Theer": 140,
                              "Roria": 136,
                              "Kosos": 211},
                   "Kuart": {"Lanoi": 50,
                             "Nohoi": 18,
                             "Ruun": 6,
                             "Milos": 70,
                             "Ghiido": 75,
                             "Kuart": 0,
                             "Boomon": 38,
                             "Goorum": 43,
                             "Shiphos": 42,
                             "Nokshos": 87,
                             "Pharis": 89,
                             "Khamin": 98,
                             "Tarios": 98,
                             "Peranna": 107,
                             "Khandan": 134,
                             "Tawa": 135,
                             "Theer": 137,
                             "Roria": 124,
                             "Kosos": 173},
                   "Boomon": {"Lanoi": 90,
                              "Nohoi": 57,
                              "Ruun": 45,
                              "Milos": 76,
                              "Ghiido": 94,
                              "Kuart": 38,
                              "Boomon": 0,
                              "Goorum": 6,
                              "Shiphos": 36,
                              "Nokshos": 91,
                              "Pharis": 91,
                              "Khamin": 95,
                              "Tarios": 67,
                              "Peranna": 68,
                              "Khandan": 98,
                              "Tawa": 105,
                              "Theer": 104,
                              "Roria": 91,
                              "Kosos": 134},
                   "Goorum": {"Lanoi": 95,
                              "Nohoi": 63,
                              "Ruun": 50,
                              "Milos": 81,
                              "Ghiido": 93,
                              "Kuart": 43,
                              "Boomon": 6,
                              "Goorum": 0,
                              "Shiphos": 33,
                              "Nokshos": 88,
                              "Pharis": 87,
                              "Khamin": 92,
                              "Tarios": 62,
                              "Peranna": 64,
                              "Khandan": 97,
                              "Tawa": 98,
                              "Theer": 98,
                              "Roria": 85,
                              "Kosos": 132},
                   "Shiphos": {"Lanoi": 84,
                               "Nohoi": 56,
                               "Ruun": 45,
                               "Milos": 103,
                               "Ghiido": 61,
                               "Kuart": 42,
                               "Boomon": 36,
                               "Goorum": 33,
                               "Shiphos": 0,
                               "Nokshos": 55,
                               "Pharis": 55,
                               "Khamin": 63,
                               "Tarios": 64,
                               "Peranna": 92,
                               "Khandan": 127,
                               "Tawa": 97,
                               "Theer": 101,
                               "Roria": 92,
                               "Kosos": 156},
                   "Nokshos": {"Lanoi": 108,
                               "Nohoi": 93,
                               "Ruun": 87,
                               "Milos": 156,
                               "Ghiido": 34,
                               "Kuart": 87,
                               "Boomon": 91,
                               "Goorum": 88,
                               "Shiphos": 55,
                               "Nokshos": 0,
                               "Pharis": 3,
                               "Khamin": 18,
                               "Tarios": 86,
                               "Peranna": 133,
                               "Khandan": 171,
                               "Tawa": 103,
                               "Theer": 109,
                               "Roria": 109,
                               "Kosos": 189},
                   "Pharis": {"Lanoi": 111,
                              "Nohoi": 97,
                              "Ruun": 89,
                              "Milos": 157,
                              "Ghiido": 37,
                              "Kuart": 89,
                              "Boomon": 91,
                              "Goorum": 87,
                              "Shiphos": 55,
                              "Nokshos": 3,
                              "Pharis": 0,
                              "Khamin": 14,
                              "Tarios": 83,
                              "Peranna": 132,
                              "Khandan": 170,
                              "Tawa": 100,
                              "Theer": 107,
                              "Roria": 105,
                              "Kosos": 186},
                   "Khamin": {"Lanoi": 124,
                              "Nohoi": 107,
                              "Ruun": 100,
                              "Milos": 165,
                              "Ghiido": 53,
                              "Kuart": 98,
                              "Boomon": 95,
                              "Goorum": 92,
                              "Shiphos": 63,
                              "Nokshos": 18,
                              "Pharis": 14,
                              "Khamin": 0,
                              "Tarios": 77,
                              "Peranna": 128,
                              "Khandan": 168,
                              "Tawa": 89,
                              "Theer": 97,
                              "Roria": 97,
                              "Kosos": 182},
                   "Tarios": {"Lanoi": 145,
                              "Nohoi": 117,
                              "Ruun": 105,
                              "Milos": 138,
                              "Ghiido": 112,
                              "Kuart": 98,
                              "Boomon": 67,
                              "Goorum": 62,
                              "Shiphos": 64,
                              "Nokshos": 86,
                              "Pharis": 83,
                              "Khamin": 77,
                              "Tarios": 0,
                              "Peranna": 55,
                              "Khandan": 94,
                              "Tawa": 38,
                              "Theer": 38,
                              "Roria": 27,
                              "Kosos": 104},
                   "Peranna": {"Lanoi": 157,
                               "Nohoi": 125,
                               "Ruun": 103,
                               "Milos": 116,
                               "Ghiido": 150,
                               "Kuart": 107,
                               "Boomon": 68,
                               "Goorum": 64,
                               "Shiphos": 92,
                               "Nokshos": 133,
                               "Pharis": 132,
                               "Khamin": 128,
                               "Tarios": 55,
                               "Peranna": 0,
                               "Khandan": 38,
                               "Tawa": 80,
                               "Theer": 73,
                               "Roria": 59,
                               "Kosos": 66},
                   "Khandan": {"Lanoi": 182,
                               "Nohoi": 150,
                               "Ruun": 140,
                               "Milos": 122,
                               "Ghiido": 187,
                               "Kuart": 134,
                               "Boomon": 98,
                               "Goorum": 97,
                               "Shiphos": 127,
                               "Nokshos": 171,
                               "Pharis": 170,
                               "Khamin": 168,
                               "Tarios": 94,
                               "Peranna": 38,
                               "Khandan": 0,
                               "Tawa": 113,
                               "Theer": 107,
                               "Roria": 92,
                               "Kosos": 52},
                   "Tawa": {"Lanoi": 180,
                            "Nohoi": 153,
                            "Ruun": 140,
                            "Milos": 176,
                            "Ghiido": 134,
                            "Kuart": 135,
                            "Boomon": 105,
                            "Goorum": 98,
                            "Shiphos": 97,
                            "Nokshos": 103,
                            "Pharis": 100,
                            "Khamin": 89,
                            "Tarios": 38,
                            "Peranna": 80,
                            "Khandan": 113,
                            "Tawa": 0,
                            "Theer": 9,
                            "Roria": 21,
                            "Kosos": 105},
                   "Theer": {"Lanoi": 183,
                             "Nohoi": 154,
                             "Ruun": 142,
                             "Milos": 174,
                             "Ghiido": 140,
                             "Kuart": 137,
                             "Boomon": 104,
                             "Goorum": 98,
                             "Shiphos": 101,
                             "Nokshos": 109,
                             "Pharis": 107,
                             "Khamin": 97,
                             "Tarios": 38,
                             "Peranna": 73,
                             "Khandan": 107,
                             "Tawa": 9,
                             "Theer": 0,
                             "Roria": 16,
                             "Kosos": 96},
                   "Roria": {"Lanoi": 174,
                             "Nohoi": 143,
                             "Ruun": 131,
                             "Milos": 159,
                             "Ghiido": 136,
                             "Kuart": 124,
                             "Boomon": 91,
                             "Goorum": 85,
                             "Shiphos": 92,
                             "Nokshos": 109,
                             "Pharis": 105,
                             "Khamin": 97,
                             "Tarios": 27,
                             "Peranna": 59,
                             "Khandan": 92,
                             "Tawa": 21,
                             "Theer": 16,
                             "Roria": 0,
                             "Kosos": 87},
                   "Kosos": {"Lanoi": 224,
                             "Nohoi": 191,
                             "Ruun": 179,
                             "Milos": 172,
                             "Ghiido": 211,
                             "Kuart": 173,
                             "Boomon": 134,
                             "Goorum": 132,
                             "Shiphos": 156,
                             "Nokshos": 189,
                             "Pharis": 186,
                             "Khamin": 182,
                             "Tarios": 104,
                             "Peranna": 66,
                             "Khandan": 52,
                             "Tawa": 105,
                             "Theer": 96,
                             "Roria": 87,
                             "Kosos": 0}}

    # Definimos varios problemas.
    problema_1 = Problema(estado_inicial=lanoi,
                          estados_objetivos=[kosos],
                          acciones=acciones,
                          costes=costes,
                          heuristicas=heuristicas)

    problema_2 = Problema(estado_inicial=lanoi,
                          estados_objetivos=[goorum],
                          acciones=acciones,
                          costes=costes,
                          heuristicas=heuristicas)

    problema_3 = Problema(estado_inicial=lanoi,
                          estados_objetivos=[boomon, goorum],
                          acciones=acciones,
                          costes=costes,
                          heuristicas=heuristicas)

    # ------------------------------------------------------------------------
    # ALGORITMOS DE BÚSQUEDA INFORMADA
    # ------------------------------------------------------------------------

    # Indicamos los algoritmos que queremos lanzar.
    lanza_voraz = True

    # Indica si se mostrará lo que hace cada algoritmo.
    log = True
    paso_a_paso = False

    # Indicamos el problema a resolver.
    problema = problema_1

    # Poder medir los tiempos.
    from time import time

    # Búsqueda voraz.
    if lanza_voraz:
        print("*****************")
        print("***** VORAZ *****")
        print("*****************")
        inicio = time()
        solucion = voraz(problema=problema,
                         log=log,
                         paso_a_paso=paso_a_paso)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)
