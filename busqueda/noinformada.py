#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diferentes algoritmos de búsqueda no informada en grafos.
La principla diferencia es el tipo de lista a usar para almacenar el siguiente
nodo a visitar (FIFO, LIFO, prioridad, etc.).
"""
from grafos import Accion, Estado, Problema, Nodo


# %% --- PRIMERO EN ANCHURA ---

def anchura(
        problema,
        log=False,
        paso_a_paso=False):
    """
    Búsqueda en grafos primero en anchura (breadth-first search).
    Se expande al completo cada nivel antes de expandir los del siguiente.
    Para ello, se usará una "Lista FIFO".
    Este algoritmo no tiene en cuenta los costes.
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
        raise "No se indicó una definición de problema a resolver"

    # Obtenemos el nodo raíz.
    estado = problema.estado_inicial.nombre
    acciones = problema.acciones[estado] if problema.acciones else {}
    raiz = Nodo(estado=problema.estado_inicial,
                acciones=acciones)

    # Miramos si el raíz es ya un objetivo.
    if problema.es_objetivo(estado=raiz.estado):
        if log:
            msg = "Objetivo: {0}"
            print(msg.format(raiz.estado.nombre))
        return raiz

    # Definimos la frontera (FIFO) y agregamos el nodo raíz.
    frontera = [raiz, ]

    # Definimos el conjunto de los estados explorados.
    explorados = set()

    # Entramos en el bucle principal.
    while True:
        # Mostramos la frontera y explorada.
        if log:
            log_frnt = [n.estado.nombre
                        for n in frontera]
            log_xplr = [e.nombre
                        for e in explorados]
            print("----- NUEVO CICLO -----")
            msg = "Frontera: {0}"
            print(msg.format(log_frnt))
            msg = "Explorados: {0}"
            print(msg.format(log_xplr))

        # Si frontera está vacía, terminamos.
        if not frontera:
            return None

        # Obtenemos el siguiente nodo.
        nodo = frontera.pop(0)
        if log:
            msg = "Nodo: {0}"
            print(msg.format(nodo.estado.nombre))
            log_frnt = [n.estado.nombre
                        for n in frontera]
            msg = "Frontera: {0}"
            print(msg.format(log_frnt))

        # Agregamos su estado al conjunto de explorados.
        explorados.add(nodo.estado)
        if log:
            log_xplr = [e.nombre
                        for e in explorados]
            msg = "Explorados: {0}"
            print(msg.format(log_xplr))

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
            if (hijo.estado not in explorados and
                hijo.estado not in estados_frontera):
                # Si el estado del hijo es un objetivo, lo devolvemos.
                es_objetivo = problema.es_objetivo(estado=hijo.estado)
                if es_objetivo:
                    if log:
                        msg = "Objetivo: {0}"
                        print(msg.format(nombre_hijo))
                    return hijo

                # Sino, lo agregamos a la frontera.
                frontera.append(hijo)
                if log:
                    msg = "   Añade Frontera: {0}"
                    print(msg.format(nombre_hijo))

        # Si nos piden ir paso a paso.
        if paso_a_paso:
            input("Pulse cualquier tecla para continuar.")


# %% --- COSTE UNIFORME ---

def coste_uniforme(
        problema,
        log=False,
        paso_a_paso=False):
    """
    Búsqueda en grafos de coste uniforme (uniform-cost search).
    Basado en primero en anchura pero teniendo en cuenta los costes.
    Expande el nodo con menor coste asociado.
    Para ello, se usará una FIFO.
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
        raise "No se indicó una definición de problema a resolver"

    # Obtenemos el nodo raíz.
    estado = problema.estado_inicial.nombre
    acciones = problema.acciones[estado] if problema.acciones else {}
    raiz = Nodo(estado=problema.estado_inicial,
                acciones=acciones)

    # Definimos la frontera (FIFO) y agregamos el nodo raíz.
    frontera = [raiz, ]

    # Definimos el conjunto de los estados explorados.
    explorados = set()

    # Entramos en el bucle principal.
    while True:
        # Mostramos la frontera y explorada.
        if log:
            log_frnt = [n.estado.nombre
                        for n in frontera]
            log_xplr = [e.nombre
                        for e in explorados]
            print("----- NUEVO CICLO -----")
            msg = "Frontera: {0}"
            print(msg.format(log_frnt))
            msg = "Explorados: {0}"
            print(msg.format(log_xplr))

        # Si frontera está vacía, terminamos.
        if not frontera:
            return None

        # Obtenemos el siguiente nodo.
        nodo = frontera.pop(0)
        if log:
            msg = "Nodo: {0}"
            print(msg.format(nodo.estado.nombre))
            log_frnt = [n.estado.nombre
                        for n in frontera]
            msg = "Frontera: {0}"
            print(msg.format(log_frnt))

        # Miramos si el nodo es ya un objetivo.
        if problema.es_objetivo(estado=nodo.estado):
            if log:
                msg = "Objetivo: {0}"
                print(msg.format(nodo.estado.nombre))
            return nodo

        # Agregamos su estado al conjunto de explorados.
        explorados.add(nodo.estado)
        if log:
            log_xplr = [e.nombre
                        for e in explorados]
            msg = "Explorados: {0}"
            print(msg.format(log_xplr))

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
            if (hijo.estado not in explorados and
                hijo.estado not in estados_frontera):
                # Lo agregamos a la frontera.
                frontera.append(hijo)
                if log:
                    msg = "   Añade Frontera: {0}"
                    print(msg.format(nombre_hijo))
            else:
                # Miramos si el estado está en algún nodo de la frontera.
                buscar = [n
                          for n in frontera
                          if n.estado == hijo.estado]
                if buscar:
                    # Indicamos que el estado ya existía en la frontera.
                    if log:
                        msg = "   Estado En Frontera: {0}"
                        print(msg.format(nombre_hijo))

                    # Si tiene mejor coste el hijo que el de la frontera.
                    if log:
                        msg = "      Coste Hijo: {0}"
                        print(msg.format(hijo.coste))
                        msg = "      Coste Frontera: {0}"
                        print(msg.format(buscar[0].coste))
                    if hijo.coste < buscar[0].coste:
                        # Indicamos que vamos a sustituir el nodo frontera.
                        if log:
                            print("      Sustituido: SÍ")

                        # Sustituimos el de la frontera por el del hijo.
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
                        if log:
                            msg = "      Nuevo Coste: {0}"
                            print(msg.format(frontera[indice].coste))
                    else:
                        # Indicamos que no se sustituye.
                        if log:
                            print("      Sustituido: NO")

        # Si nos piden ir paso a paso.
        if paso_a_paso:
            input("Pulse cualquier tecla para continuar.")


# %% --- PRIMERO EN PROFUNDIDAD ---

def profundidad(
        problema,
        log=False,
        paso_a_paso=False):
    """
    Búsqueda en grafos primero en profundidad (depth-first search).
    Se expande el nodo raíz, luego uno de sus hijos, luego uno de los hijos
    del hijo hasta llegar a un nodo hoja. Si no hay solución, se retrocede
    y se prueba con el siguiente hijo.
    Para ello, se usará una "Lista LIFO".
    Este algoritmo no tiene en cuenta los costes.
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
        raise "No se indicó una definición de problema a resolver"

    # Obtenemos el nodo raíz.
    estado = problema.estado_inicial.nombre
    acciones = problema.acciones[estado] if problema.acciones else {}
    raiz = Nodo(estado=problema.estado_inicial,
                acciones=acciones)

    # Miramos si el raíz es ya un objetivo.
    if problema.es_objetivo(estado=raiz.estado):
        if log:
            msg = "Objetivo: {0}"
            print(msg.format(raiz.estado.nombre))
        return raiz

    # Definimos la frontera (LIFO) y agregamos el nodo raíz.
    frontera = [raiz, ]

    # Definimos el conjunto de los estados explorados.
    explorados = set()

    # Entramos en el bucle principal.
    while True:
        # Mostramos la frontera y explorada.
        if log:
            log_frnt = [n.estado.nombre
                        for n in frontera]
            log_xplr = [e.nombre
                        for e in explorados]
            print("----- NUEVO CICLO -----")
            msg = "Frontera: {0}"
            print(msg.format(log_frnt))
            msg = "Explorados: {0}"
            print(msg.format(log_xplr))

        # Si frontera está vacía, terminamos.
        if not frontera:
            return None

        # Obtenemos el siguiente nodo.
        nodo = frontera.pop()
        if log:
            msg = "Nodo: {0}"
            print(msg.format(nodo.estado.nombre))
            log_frnt = [n.estado.nombre
                        for n in frontera]
            msg = "Frontera: {0}"
            print(msg.format(log_frnt))

        # Agregamos su estado al conjunto de explorados.
        explorados.add(nodo.estado)
        if log:
            log_xplr = [e.nombre
                        for e in explorados]
            msg = "Explorados: {0}"
            print(msg.format(log_xplr))

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
            if (hijo.estado not in explorados and
                hijo.estado not in estados_frontera):
                # Si el estado del hijo es un objetivo, lo devolvemos.
                es_objetivo = problema.es_objetivo(estado=hijo.estado)
                if es_objetivo:
                    if log:
                        msg = "Objetivo: {0}"
                        print(msg.format(nombre_hijo))
                    return hijo

                # Sino, lo agregamos a la frontera.
                frontera.append(hijo)
                if log:
                    msg = "   Añade Frontera: {0}"
                    print(msg.format(nombre_hijo))

        # Si nos piden ir paso a paso.
        if paso_a_paso:
            input("Pulse cualquier tecla para continuar.")


def profundidad_recursiva(
        problema,
        log=False,
        paso_a_paso=False):
    """
    Versión recursiva de la búsqueda en grafos primero en profundidad.
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
        raise "No se indicó una definición de problema a resolver"

    # Obtenemos el nodo raíz.
    estado = problema.estado_inicial.nombre
    acciones = problema.acciones[estado] if problema.acciones else {}
    raiz = Nodo(estado=problema.estado_inicial,
                acciones=acciones)

    # Definimos el conjunto de los estados explorados.
    explorados = set()

    # Invocamos la función recursiva y devolvemos su resultado.
    return _bpp_recursiva(nodo=raiz,
                          problema=problema,
                          explorados=explorados,
                          log=log,
                          paso_a_paso=paso_a_paso)


def _bpp_recursiva(nodo,
                   problema,
                   explorados,
                   log=False,
                   paso_a_paso=False):
    """
    Función recursiva para realizar la búsqueda primero en profundidad.
    """
    # Mostramos la situación actual.
    print("----- NUEVA LLAMADA RECURSIVA -----")
    if not nodo.padre:
        msg = "Estado Raíz: {0}"
        print(msg.format(nodo.estado.nombre))
    else:
        msg = "Padre: {0} --- {1} ---> Estado: {2}"
        print(msg.format(nodo.padre.estado.nombre,
                         nodo.accion.nombre,
                         nodo.estado.nombre))

    # Miramos si el raíz es ya un objetivo.
    if problema.es_objetivo(estado=nodo.estado):
        if log:
            msg = "Objetivo: {0}"
            print(msg.format(nodo.estado.nombre))
        return nodo

    # Agregamos su estado al conjunto de explorados.
    explorados.add(nodo.estado)
    if log:
        log_xplr = [e.nombre
                    for e in explorados]
        msg = "Explorados: {0}"
        print(msg.format(log_xplr))

    # Si el nodo no tiene acciones, pasamos al siguiente.
    if not nodo.acciones:
        if log:
            print("No hay Acciones")
        return None

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
        if hijo.estado not in explorados:
            # Si nos piden ir paso a paso.
            if paso_a_paso:
                input("Pulse cualquier tecla para continuar.")

            # Invocamos la recursiva para cada hijo.
            resultado = _bpp_recursiva(nodo=hijo,
                                       problema=problema,
                                       explorados=explorados,
                                       log=log,
                                       paso_a_paso=paso_a_paso)

            # Si nos devuelve la solución, la devolvemos.
            if resultado:
                return resultado

    # Si llegamos aquí es que no hay solución en ninguno de los hijos.
    return None


# %% --- PRIMERO EN PROFUNDIDAD LIMITADA ---

def profundidad_limitada(
        problema,
        log=False,
        paso_a_paso=False):
    pass


# %% --- PRIMERO EN PROFUNDIDAD ITERATIVA ---

def profundidad_iterativa(
        problema,
        log=False,
        paso_a_paso=False):
    pass


# %% --- BIDIRECCIONAL ---

def bidireccional(
        problema,
        log=False,
        paso_a_paso=False):
    pass


# %% --- FUNCIONES AUXILIARES ---

def crea_nodo_hijo(problema,
                   padre,
                   accion):
    """
    Método auxiliar que ayudará a crear nodos hijos a los métodos que
    implementan algoritmos de búsqueda no informada.
    """
    # Comprobaciones.
    if not problema:
        raise "No se indicó una definición de problema"
    if not padre:
        raise "No se indicó el nodo padre"
    if not accion:
        raise "No se indicó la acción"

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

    # Lo agregamos al nodo actual como hijo.
    padre.agregar(hijo=hijo)

    # Devolvemos el hijo.
    return hijo


def muestra_solucion(objetivo,
                     segundos=0):
    """
    Muestra la solución encuentrada a partir de un nodo objetivo.
    Argumentos:
    - objetivo: nodo objetivo encontrado por un algoritmo.
    - tiempo: cantidad de tiempo que ha tardado en ejecutarse el algoritmo.
    """
    # Mostramos la solución.
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

    # Recorremos desde el nodo objetivo al nodo raíz.
    nodo = objetivo
    while nodo:
        # Mostramos los datos de ese nodo.
        msg = "Estado: {0}, Coste Total: {1}"
        estado = nodo.estado.nombre
        coste_total = nodo.coste
        print(msg.format(estado, coste_total))

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
    Ejemplos de búsqueda no informada en grafos.
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

    # Definimos el problema: ir de Lanoi a Kosos.
    problema = Problema(estado_inicial=lanoi,
                        estados_objetivos=[kosos],
                        acciones=acciones,
                        costes=costes)

    # ------------------------------------------------------------------------
    # ALGORITMOS DE BÚSQUEDA NO INFORMADA
    # ------------------------------------------------------------------------

    # Indicamos los algoritmos que queremos lanzar.
    lanza_anchura = False
    lanza_coste_uniforme = False
    lanza_profundidad = False
    lanza_profundidad_recursiva = False

    # Indica si se mostrará lo que hace cada algoritmo.
    log = True
    paso_a_paso = True

    # Poder medir los tiempos.
    from time import time

    # Búsqueda primero en anchura.
    if lanza_anchura:
        print("******************************")
        print("***** PRIMERO EN ANCHURA *****")
        print("******************************")
        inicio = time()
        solucion = anchura(problema=problema,
                           log=log,
                           paso_a_paso=paso_a_paso)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda coste uniforme.
    if lanza_coste_uniforme:
        print("**************************")
        print("***** COSTE UNIFORME *****")
        print("**************************")
        inicio = time()
        solucion = coste_uniforme(problema=problema,
                                  log=log,
                                  paso_a_paso=paso_a_paso)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda primero en profundidad.
    if lanza_profundidad:
        print("**********************************")
        print("***** PRIMERO EN PROFUNDIDAD *****")
        print("**********************************")
        inicio = time()
        solucion = profundidad(problema=problema,
                               log=log,
                               paso_a_paso=paso_a_paso)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda primero en profundidad (versión recursiva).
    if lanza_profundidad_recursiva:
        print("**********************************************")
        print("***** PRIMERO EN PROFUNDIDAD (RECURSIVA) *****")
        print("**********************************************")
        inicio = time()
        solucion = profundidad_recursiva(problema=problema,
                                         log=log,
                                         paso_a_paso=paso_a_paso)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)
