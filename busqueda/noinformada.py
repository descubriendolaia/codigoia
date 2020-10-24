#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diferentes algoritmos de búsqueda no informada en grafos.

La principal diferencia es el tipo de lista a usar para almacenar el siguiente
nodo a visitar (FIFO, LIFO, prioridad, etc.).
"""
from grafos import Accion
from grafos import Estado
from grafos import Nodo
from grafos import Problema


# %% --- PRIMERO EN ANCHURA ---------------------------------------------------

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
        raise ValueError("No se indicó una definición de problema a resolver")

    # Obtenemos el nodo raíz.
    raiz = crea_nodo_raiz(problema=problema)

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
                # Indicamos que ya estaba.
                if log:
                    if hijo.estado in explorados:
                        msg = "   {0} ya ha sido explorado"
                        print(msg.format(hijo.estado.nombre))
                    if hijo.estado in estados_frontera:
                        msg = "   {0} ya está en la frontera"
                        print(msg.format(hijo.estado.nombre))
            else:
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
            input("Pulsa la tecla 'Enter' para continuar.")


# %% --- COSTE UNIFORME -------------------------------------------------------

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
        raise ValueError("No se indicó una definición de problema a resolver")

    # Obtenemos el nodo raíz.
    raiz = crea_nodo_raiz(problema=problema)

    # Definimos la frontera (FIFO) y agregamos el nodo raíz.
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
            else:
                # Lo agregamos a la frontera.
                frontera.append(hijo)
                if log:
                    msg = "   Añade Frontera: {0}"
                    print(msg.format(nombre_hijo))

        # Si nos piden ir paso a paso.
        if paso_a_paso:
            input("Pulsa la tecla 'Enter' para continuar.")


# %% --- PRIMERO EN PROFUNDIDAD -----------------------------------------------

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
        raise ValueError("No se indicó una definición de problema a resolver")

    # Obtenemos el nodo raíz.
    raiz = crea_nodo_raiz(problema=problema)

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
        nodo = frontera.pop()
        if log:
            msg = "Nodo: {0}"
            print(msg.format(nodo.estado.nombre))
            log_frontera = [nodo.estado.nombre
                            for nodo in frontera]
            msg = "Frontera: {0}"
            print(msg.format(log_frontera))

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
                # Indicamos que ya ha sido explorado.
                if log:
                    if hijo.estado in explorados:
                        msg = "   {0} ya ha sido explorado"
                        print(msg.format(hijo.estado.nombre))
                    if hijo.estado in estados_frontera:
                        msg = "   {0} ya está en la frontera"
                        print(msg.format(hijo.estado.nombre))
            else:
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
            input("Pulsa la tecla 'Enter' para continuar.")


def profundidad_recursiva(
        problema,
        limite=None,
        tipo_limite="profundidad",
        log=False,
        paso_a_paso=False):
    """
    Versión recursiva de la búsqueda en grafos primero en profundidad.

    También permite la búsqueda en profundidad limitada (Depth-Limited Search)
    si se indica un valor positivo en 'limite'.

    Argumentos:
    - problema: definición del problema a resolver.
    - limite: profundidad máxima de expansión del árbol en una rama, es decir,
              número máximo de veces que invocará a la función de forma
              recursiva. Si se indica None no habrá límite.
    - tipo_limite: si es por 'profundidad' o por 'coste'. La primera resta
                   1 cada vez que se crean hijos. La segunda resta el coste
                   de realizar esa acción.
    - log: Si se mostrarán los pasos que se van realizando.
    - paso_a_paso: si se detendrá en cada paso para poder analizarlo.

    Devuelve: referencia al nodo con uno de los estado objetivo. A partir de
              él y siguiendo sus nodos padres, se obtendrá la solución.
              Si no encuentra solución, devuelve "None".
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema a resolver")
    if isinstance(limite, int) and limite < 0:
        raise ValueError("Debe indicar un límite positivo")
    if tipo_limite not in ("profundidad", "coste"):
        raise ValueError("El tipo de límite debe ser 'profundidad' o 'coste'")

    # Obtenemos el nodo raíz.
    raiz = crea_nodo_raiz(problema=problema)

    # Definimos el conjunto de los estados explorados.
    explorados = set()

    # Invocamos la función recursiva y devolvemos su resultado.
    return _bpp_recursiva(nodo=raiz,
                          problema=problema,
                          limite=limite,
                          tipo_limite=tipo_limite,
                          explorados=explorados,
                          log=log,
                          paso_a_paso=paso_a_paso)


def _bpp_recursiva(nodo,
                   problema,
                   limite,
                   tipo_limite,
                   explorados,
                   log,
                   paso_a_paso):
    """
    Función recursiva para realizar la búsqueda primero en profundidad.

    Argumentos:
    - nodo: nodo a expandir sus hijos de forma recursiva.
    - problema: definición del problema a resolver.
    - limite: profundidad máxima de expansión del árbol en una rama, es decir,
              número máximo de veces que invocará a la función de forma
              recursiva. Si se indica None no habrá límite.
    - tipo_limite: si es por 'profundidad' o por 'coste'. La primera resta
                   1 cada vez que se crean hijos. La segunda resta el coste
                   de realizar esa acción.
    - explorados: conjunto de estados ya explorados.
    - log: Si se mostrarán los pasos que se van realizando.
    - paso_a_paso: si se detendrá en cada paso para poder analizarlo.

    Devuelve: referencia al nodo con uno de los estado objetivo. A partir de
              él y siguiendo sus nodos padres, se obtendrá la solución.
              Si no encuentra solución, devuelve "None".
    """
    # Mostramos la situación actual.
    if log:
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
        log_explorados = [estado.nombre
                          for estado in explorados]
        msg = "Explorados: {0}"
        print(msg.format(log_explorados))

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
        if hijo.estado in explorados:
            # Indicamos que ese estado ya ha sido explorado.
            if log:
                msg = "   {0} ya ha sido explorado"
                print(msg.format(hijo.estado.nombre))
        else:
            # Si nos piden ir paso a paso.
            if paso_a_paso:
                input("Pulsa la tecla 'Enter' para continuar.")

            # Si se indicó un límite máximo
            lim = None
            if isinstance(limite, int):
                # Si se indicó log, mostrar el límite.
                if log:
                    msg = "   Limite: {0}"
                    print(msg.format(limite))

                # Si se ha traspasado al límite, terminamos.
                if limite <= 0:
                    if log:
                        print("   Límite máximo alcanzado (corte)")
                    return None

                # Indicamos el tipo de límite.
                if log:
                    msg = "   Tipo de Límite: {0}"
                    print(msg.format(tipo_limite))

                # Si es límite por profundidad
                if tipo_limite == 'profundidad':
                    # Descenderemos un nivel.
                    lim = limite - 1
                elif tipo_limite == 'coste':
                    # Restamos el coste de realizar la acción.
                    coste = problema.coste_accion(estado=nodo.estado,
                                                  accion=accion)
                    lim = limite - coste

                    # Indicamos el coste.
                    if log:
                        msg = "   Coste Acción: {0}"
                        print(msg.format(coste))
                else:
                    err = "'tipo_limite' debe ser 'profundidad' o 'coste'"
                    raise ValueError(err)

                # Indicamos el nuevo límite.
                if log:
                    msg = "   Nuevo Límite: {0}"
                    print(msg.format(lim))

            # Invocamos la recursiva para cada hijo.
            resultado = _bpp_recursiva(nodo=hijo,
                                       problema=problema,
                                       limite=lim,
                                       tipo_limite=tipo_limite,
                                       explorados=explorados,
                                       log=log,
                                       paso_a_paso=paso_a_paso)

            # Si ya tenemos la solución, la devolvemos.
            if resultado:
                return resultado

    # Si llegamos aquí es que no hay solución en ninguno de los hijos.
    return None


# %% --- PRIMERO EN PROFUNDIDAD ITERATIVA -------------------------------------

def profundidad_iterativa(
        problema,
        limite,
        log=False,
        paso_a_paso=False):
    """
    Versión iterativa de la búsqueda en profundidad.

    Irá aumentando el límite máximo de la búsqueda en profundidad limitada
    hasta alcanzar un objetivo o hasta alcancar un límite máximo.

    Argumentos:
    - problema: definición del problema a resolver.
    - limite: profundidad máxima de expansión del árbol. None es sin límite.
    - log: Si se mostrarán los pasos que se van realizando.
    - paso_a_paso: si se detendrá en cada paso para poder analizarlo.

    Devuelve: referencia al nodo con uno de los estado objetivo. A partir de
              él y siguiendo sus nodos padres, se obtendrá la solución.
              Si no encuentra solución, devuelve "None".
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema a resolver")
    if isinstance(limite, int) and limite < 0:
        raise ValueError("Debe indicar un límite positivo")

    # Si no indican límite, es una búsqueda en profundidad normal.
    if limite is None:
        if log:
            print("--- No se ha indicado límite ---")
        return profundidad_recursiva(problema=problema,
                                     log=log,
                                     paso_a_paso=paso_a_paso)

    # Vamos ampliando el límite poco a poco.
    for i in range(1, limite + 1):
        # Indicamos el límite a probar.
        if log:
            print()
            print("***********************")
            msg = "*** Límite {0} "
            print(msg.format(i))
            print("***********************")

        # Lanzamos la recursiva con cada uno de los límites.
        resultado = profundidad_recursiva(problema=problema,
                                          limite=i,
                                          tipo_limite="profundidad",
                                          log=log,
                                          paso_a_paso=paso_a_paso)

        # Si ha solución, la devolvemos.
        if resultado:
            return resultado

    # Si llegamos aquí es que no hay solución.
    return None


# %% --- COSTE ITERATIVO ------------------------------------------------------

def coste_iterativo(
        problema,
        limite,
        paso=1,
        log=False,
        paso_a_paso=False):
    """
    Búsqueda en profundidad iterativa pero con costes.

    Versión de búsqueda en profundidad iterativa pero teniendo en cuenta los
    costes de las acciones. Aquí el límite se refiere a un coste de camino
    máximo, en vez de una profundidad máxima.

    Argumentos:
    - problema: definición del problema a resolver.
    - limite: coste máximo de camino. None es sin límite.
    - paso: en cuanto se ampliará el límite en cada iteración.
    - log: Si se mostrarán los pasos que se van realizando.
    - paso_a_paso: si se detendrá en cada paso para poder analizarlo.

    Devuelve: referencia al nodo con uno de los estado objetivo. A partir de
              él y siguiendo sus nodos padres, se obtendrá la solución.
              Si no encuentra solución, devuelve "None".
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema a resolver")
    if isinstance(limite, int) and limite < 0:
        raise ValueError("Debe indicar un límite positivo")

    # Si no indican límite, es una búsqueda en profundidad normal.
    if limite is None:
        if log:
            print("--- No se ha indicado límite ---")
        return profundidad_recursiva(problema=problema,
                                     log=log,
                                     paso_a_paso=paso_a_paso)

    # Vamos ampliando el límite poco a poco.
    for i in range(1, limite + 1, paso):
        # Indicamos el límite a probar.
        if log:
            print()
            print("***********************")
            msg = "*** Límite {0}"
            print(msg.format(i))
            print("***********************")

        # Lanzamos la recursiva con cada uno de los límites.
        resultado = profundidad_recursiva(problema=problema,
                                          limite=i,
                                          tipo_limite="coste",
                                          log=log,
                                          paso_a_paso=paso_a_paso)

        # Si ha solución, la devolvemos.
        if resultado:
            return resultado

    # Si llegamos aquí es que no hay solución.
    return None


# %% --- BIDIRECCIONAL --------------------------------------------------------

def bidireccional(
        problema,
        log=False,
        paso_a_paso=False):
    """
    Búsqueda que comienza en los nodos inicial y final a la vez.

    No sólo se lanzará una búsqueda desde el origen, también se lanzará otra
    búsqueda desde el objetivo. Este generará 2 árboles de búsqueda que, si
    en sus fronteras hay algún estado común, entonces habrán encontrado un
    camino entre ambos estatos. En esta implementación se usará la búsqueda
    en anchura para ambos árboles, aunque uno de los árboles podría ser una
    búsqueda en profundidad iterativa.

    Argumentos:
    - problema: definición del problema a resolver.
    - log: Si se mostrarán los pasos que se van realizando.
    - paso_a_paso: si se detendrá en cada paso para poder analizarlo.

    Devuelve: referencia a los nodos con el estado común. A partir de
              ellos y siguiendo sus nodos padres, se obtendrá la solución.
              Si no encuentra solución, devuelve "(None, None)".
    """
    # Comprobaciones.
    if not problema:
        raise ValueError("No se indicó una definición de problema a resolver")
    if len(problema.estados_objetivos) > 1:
        raise ValueError("El problema sólo puede tener un único objetivo")

    # Obtenemos el nodo raíz del primer árbol.
    estado_i = problema.estado_inicial.nombre
    acciones_i = problema.acciones[estado_i] if problema.acciones else {}
    raiz_i = Nodo(estado=problema.estado_inicial,
                  acciones=acciones_i)

    # Obtenemos el nodo raíz del segundo árbol.
    estado_f = problema.estados_objetivos[0].nombre
    acciones_f = problema.acciones[estado_f] if problema.acciones else {}
    raiz_f = Nodo(estado=problema.estados_objetivos[0],
                  acciones=acciones_f)

    # Miramos si la primera raíz es ya un objetivo.
    if problema.es_objetivo(estado=raiz_i.estado):
        if log:
            msg = "Objetivo: {0}"
            print(msg.format(raiz_i.estado.nombre))
        return (raiz_i, raiz_f)

    # Miramos si la segunda raíz es ya el inicio.
    if problema.estado_inicial == raiz_f.estado:
        if log:
            msg = "Inicio: {0}"
            print(msg.format(raiz_f.estado.nombre))
        return (raiz_i, raiz_f)

    # Definimos las fronteras (FIFO) y agregamos los nodos raíz.
    frontera_i = [raiz_i, ]
    frontera_f = [raiz_f, ]

    # Definimos las listas de nodos de los estados explorados.
    explorados_i = []
    explorados_f = []

    # Entramos en el bucle principal.
    while True:
        # Mostramos las frontera y los explorados.
        if log:
            log_frontera_i = [nodo.estado.nombre
                              for nodo in frontera_i]
            log_frontera_f = [nodo.estado.nombre
                              for nodo in frontera_f]
            log_explorados_i = {nodo.estado.nombre
                                for nodo
                                in explorados_i}
            log_explorados_f = {nodo.estado.nombre
                                for nodo
                                in explorados_f}
            print("----- NUEVO CICLO -----")
            msg = "Frontera Inicial: {0}"
            print(msg.format(log_frontera_i))
            msg = "Frontera Objetivo: {0}"
            print(msg.format(log_frontera_f))
            msg = "Explorados Inicial: {0}"
            print(msg.format(log_explorados_i))
            msg = "Explorados Objetivo: {0}"
            print(msg.format(log_explorados_f))

        # Si alguna frontera está vacía, terminamos.
        if not frontera_i or not frontera_f:
            return (None, None)

        # Obtenemos el siguiente nodo del primer árbol.
        nodo_i = frontera_i.pop(0)
        if log:
            msg = "Nodo Inicial: {0}"
            print(msg.format(nodo_i.estado.nombre))
            log_frontera_i = [nodo.estado.nombre
                              for nodo in frontera_i]
            msg = "Frontera Inicial: {0}"
            print(msg.format(log_frontera_i))

        # Obtenemos el siguiente nodo del segundo árbol.
        nodo_f = frontera_f.pop(0)
        if log:
            msg = "Nodo Objetivo: {0}"
            print(msg.format(nodo_f.estado.nombre))
            log_frontera_f = [nodo.estado.nombre
                              for nodo in frontera_f]
            msg = "Frontera Objetivo: {0}"
            print(msg.format(log_frontera_f))

        # Agregamos su estado al conjunto de explorados del primero.
        explorados_i.append(nodo_i)
        if log:
            log_explorados_i = [nodo.estado.nombre
                                for nodo in explorados_i]
            msg = "Explorados Inicial: {0}"
            print(msg.format(log_explorados_i))

        # Agregamos su estado al conjunto de explorados del segundo.
        explorados_f.append(nodo_f)
        if log:
            log_explorados_f = [nodo.estado.nombre
                                for nodo in explorados_f]
            msg = "Explorados Objetivo: {0}"
            print(msg.format(log_explorados_f))

        # Si alguno de los nodos no tiene acciones, lo indicamos.
        if not nodo_i.acciones:
            if log:
                print("No hay Acciones (Inicial)")
        if not nodo_f.acciones:
            if log:
                print("No hay Acciones (Objetivo)")

        # Por cada una de las acciones del primer árbol que se pueden hacer.
        for nombre_accion in nodo_i.acciones.keys():
            # Indicamos la acción.
            if log:
                msg = "   Accion (Inicial): {0}"
                print(msg.format(nombre_accion))

            # Creamos un nodo hijo.
            accion = Accion(nombre=nombre_accion)
            hijo = crea_nodo_hijo(problema=problema,
                                  padre=nodo_i,
                                  accion=accion)
            nombre_hijo = hijo.estado.nombre
            if log:
                msg = "   Hijo (Inicial): {0}"
                print(msg.format(nombre_hijo))

            # Si el estado del hijo no ha sido explorado
            # y tampoco está en la frontera.
            estados_frontera = [nodo.estado
                                for nodo in frontera_i]
            estados_explorados = [nodo.estado
                                  for nodo in explorados_i]
            if(hijo.estado in estados_explorados or
               hijo.estado in estados_frontera):
                # Indicamos que ya estaba.
                if log:
                    if hijo.estado in estados_explorados:
                        msg = "   {0} ya ha sido explorado (Inicial)"
                        print(msg.format(hijo.estado.nombre))
                    if hijo.estado in estados_frontera:
                        msg = "   {0} ya está en la frontera (Inicial)"
                        print(msg.format(hijo.estado.nombre))
            else:
                # Si el estado del hijo es un objetivo, lo devolvemos.
                es_objetivo = problema.es_objetivo(estado=hijo.estado)
                if es_objetivo:
                    if log:
                        msg = "Objetivo (Inicial): {0}"
                        print(msg.format(nombre_hijo))
                    return (hijo, None)

                # Sino, lo agregamos a la frontera.
                frontera_i.append(hijo)
                if log:
                    msg = "   Añade Frontera (Inicial): {0}"
                    print(msg.format(nombre_hijo))

        # Por cada una de las acciones del segundo árbol que se pueden hacer.
        for nombre_accion in nodo_f.acciones.keys():
            # Indicamos la acción.
            if log:
                msg = "   Accion (Objetivo): {0}"
                print(msg.format(nombre_accion))

            # Creamos un nodo hijo.
            accion = Accion(nombre=nombre_accion)
            hijo = crea_nodo_hijo(problema=problema,
                                  padre=nodo_f,
                                  accion=accion)
            nombre_hijo = hijo.estado.nombre
            if log:
                msg = "   Hijo (Objetivo): {0}"
                print(msg.format(nombre_hijo))

            # Si el estado del hijo no ha sido explorado
            # y tampoco está en la frontera.
            estados_frontera = [nodo.estado
                                for nodo in frontera_f]
            estados_explorados = [nodo.estado
                                  for nodo in explorados_f]
            if(hijo.estado in estados_explorados or
               hijo.estado in estados_frontera):
                # Indicamos que ya estaba.
                if log:
                    if hijo.estado in explorados_f:
                        msg = "   {0} ya ha sido explorado (Objetivo)"
                        print(msg.format(hijo.estado.nombre))
                    if hijo.estado in estados_frontera:
                        msg = "   {0} ya está en la frontera (Objetivo)"
                        print(msg.format(hijo.estado.nombre))
            else:
                # Si el estado del hijo es un objetivo, lo devolvemos.
                es_objetivo = problema.es_objetivo(estado=hijo.estado)
                if es_objetivo:
                    if log:
                        msg = "Objetivo (Objetivo): {0}"
                        print(msg.format(nombre_hijo))
                    return (None, hijo)

                # Sino, lo agregamos a la frontera.
                frontera_f.append(hijo)
                if log:
                    msg = "   Añade Frontera (Objetivo): {0}"
                    print(msg.format(nombre_hijo))

        # Miramos si en las fronteras o explorados hay algún estado común.
        estados_i = set(nodo.estado
                        for nodo in frontera_i)
        estados_f = set(nodo.estado
                        for nodo in frontera_f)
        estados_i = estados_i.union(set(nodo.estado
                                        for nodo in explorados_i))
        estados_f = estados_f.union(set(nodo.estado
                                        for nodo in explorados_f))
        comunes = estados_i.intersection(estados_f)

        # Si hay comunes, los devolvemos como la solución.
        if comunes:
            # Obtenemos el estado común.
            comun = comunes.pop()

            # Obtenemos los frontera y explorados de cada árbol.
            nodos_arbol_i = []
            nodos_arbol_f = []
            nodos_arbol_i.extend(frontera_i)
            nodos_arbol_f.extend(frontera_f)
            nodos_arbol_i.extend(explorados_i)
            nodos_arbol_f.extend(explorados_f)

            # Obtenemos el común del primer árbol.
            comun_i = [nodo
                       for nodo in nodos_arbol_i
                       if nodo.estado == comun][0]

            # Obtenemos el común del segundo árbol.
            comun_f = [nodo
                       for nodo in nodos_arbol_f
                       if nodo.estado == comun][0]

            # Devolvemos los nodos con el estado común.
            return (comun_i, comun_f)

        # Si nos piden ir paso a paso.
        if paso_a_paso:
            input("Pulsa la tecla 'Enter' para continuar.")


# %% --- FUNCIONES AUXILIARES -------------------------------------------------

def crea_nodo_raiz(problema):
    """
    Crea y devuelve el nodo raíz del problema indicado.

    Método auxiliar que ayudará a crear nodos raíz de los métodos que
    implementan algoritmos de búsqueda informada.

    Argumentos:
    - problema: problema a obtener su nodo raíz.

    Devuelve: nodo raíz creado.
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

    # Devolvemos el nodo raíz creado.
    return raiz


def crea_nodo_hijo(problema,
                   padre,
                   accion):
    """
    Crea y devuelve el nodo hijo.

    Método auxiliar que ayudará a crear nodos hijos a los métodos que
    implementan algoritmos de búsqueda no informada.

    Argumentos:
    - problema: definición del problema a resolver.
    - padre: nodo padre del nodo hijo a crear. Se agrega a los hijos de él.
    - accion: acción que ha provocado la creación de este nodo hijo.

    Devuelve: nodo hijo creado tras aplicar acción al padre.
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

    # Le asignamos el nodo padre.
    hijo.padre = padre

    # Agregamos el hijo.
    padre.hijos.append(hijo)

    # Devolvemos el hijo.
    return hijo


def muestra_solucion(objetivo=None,
                     es_bidireccional=False,
                     nodos_bidireccional=(None, None),
                     segundos=0):
    """
    Muestra la solución encuentrada a partir de un nodo objetivo.

    Argumentos:
    - objetivo: nodo objetivo encontrado por un algoritmo.
    - es_bidireccional: la solución es diferente al resto.
    - nodos_bidireccional: esta búsqueda devuelve un par de nodos con estados
                           comunes que deben combinarse para obtener la
                           solución final.
    - segundos: cantidad de tiempo que ha tardado en ejecutarse el algoritmo.

    Devuelve: nada.
    """
    # Mostramos la solución.
    print()
    print("--------------------")
    print("----- SOLUCIÓN -----")
    print("--------------------")

    # Si nos pasan el tiempo.
    if segundos > 0:
        msg = "Tiempo: {0} milisegundos"
        print(msg.format(segundos*1000))
        print("--------------------")

    # ------------------- #
    # -- BIDIRECCIONAL -- #
    # ------------------- #

    # Si nos pasan la solución de la bidireccional.
    if es_bidireccional:
        # Obtenemos los nodos con el estado común.
        nodo_i = nodos_bidireccional[0]
        nodo_f = nodos_bidireccional[1]

        # Guardamos los costes para mostrarlos al final.
        coste_i = nodo_i.coste if nodo_i else 0
        coste_f = nodo_f.coste if nodo_f else 0

        # Definimos una lista que indicará el camino completo.
        camino = []

        # Si hay nodo en el primer árbol
        if nodo_i:
            # Lo recorremos hasta la raíz
            while nodo_i:
                # Agregamos cada nodo al camino (orden inverso).
                camino.insert(0, nodo_i)

                # Ascendemos en el árbol.
                nodo_i = nodo_i.padre

        # Si hay nodo en el segúndo árbol.
        if nodo_f:
            # No repetimos el nodo común.
            nodo_f = nodo_f.padre

            # Lo recorremos hasta la raíz.
            while nodo_f:
                # Agregamos cada nodo al camino.
                camino.append(nodo_f)

                # Ascendemos en el árbol.
                nodo_f = nodo_f.padre

        # Si no hay camino, lo indicamos.
        if not camino:
            print("No hay solución")
            return

        # Recorremos el camino.
        for nodo in camino:
            # Mostramos el estado de cada nodo.
            msg = "Estado: {0}"
            print(msg.format(nodo.estado.nombre))

        # Mostramos al final el coste total.
        msg = "Coste Total: {0}"
        print(msg.format(coste_i + coste_f))

    # --------------------- #
    # -- RESTO BÚSQUEDAS -- #
    # --------------------- #

    else:
        # Si no hay objetivo, no hay solución.
        if not objetivo:
            print("No hay solución")
            return

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
                coste = problema_resolver.coste_accion(estado=padre,
                                                       accion=nodo.accion)
                if accion:
                    msg = "<--- {0} [{1}] ---"
                    print(msg.format(accion, coste))

            # Pasamos al nodo padre.
            nodo = nodo.padre


# %% --- MAIN -----------------------------------------------------------------

if __name__ == "__main__":
    # Ejemplos de búsqueda no informada en grafos.

    # Poder medir los tiempos.
    from time import time

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

    # Definimos varios problemas.
    problema_1 = Problema(estado_inicial=lanoi,
                          estados_objetivos=[kosos],
                          acciones=acciones,
                          costes=costes)

    problema_2 = Problema(estado_inicial=lanoi,
                          estados_objetivos=[goorum],
                          acciones=acciones,
                          costes=costes)

    problema_3 = Problema(estado_inicial=lanoi,
                          estados_objetivos=[boomon, goorum],
                          acciones=acciones,
                          costes=costes)

    # ------------------------------------------------------------------------
    # ALGORITMOS DE BÚSQUEDA NO INFORMADA
    # ------------------------------------------------------------------------

    # Indicamos los algoritmos que queremos lanzar.
    LANZA_ANCHURA = True
    LANZA_COSTE_UNIFORME = True
    LANZA_PROFUNDIDAD = True
    LANZA_PROFUNDIDAD_RECURSIVA = True
    LANZA_PROFUNDIDAD_LIMITADA = True
    LANZA_PROFUNDIDAD_ITERATIVA = True
    LANZA_COSTE_ITERATIVO = True
    LANZA_BIDIRECCIONAL = True

    # Indica si se mostrará lo que hace cada algoritmo.
    LOG = False
    PASO_A_PASO = False

    # Indicamos el problema a resolver.
    problema_resolver = problema_1

    # Búsqueda primero en anchura.
    if LANZA_ANCHURA:
        print()
        print("******************************")
        print("***** PRIMERO EN ANCHURA *****")
        print("******************************")
        inicio = time()
        solucion = anchura(problema=problema_resolver,
                           log=LOG,
                           paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda coste uniforme.
    if LANZA_COSTE_UNIFORME:
        print()
        print("**************************")
        print("***** COSTE UNIFORME *****")
        print("**************************")
        inicio = time()
        solucion = coste_uniforme(problema=problema_resolver,
                                  log=LOG,
                                  paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda primero en profundidad.
    if LANZA_PROFUNDIDAD:
        print()
        print("**********************************")
        print("***** PRIMERO EN PROFUNDIDAD *****")
        print("**********************************")
        inicio = time()
        solucion = profundidad(problema=problema_resolver,
                               log=LOG,
                               paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda primero en profundidad (versión recursiva).
    if LANZA_PROFUNDIDAD_RECURSIVA:
        print()
        print("**********************************************")
        print("***** PRIMERO EN PROFUNDIDAD (RECURSIVA) *****")
        print("**********************************************")
        inicio = time()
        solucion = profundidad_recursiva(problema=problema_resolver,
                                         log=LOG,
                                         paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda primero en profundidad (versión limitada).
    if LANZA_PROFUNDIDAD_LIMITADA:
        print()
        print("*********************************************")
        print("***** PRIMERO EN PROFUNDIDAD (LIMITADA) *****")
        print("*********************************************")
        inicio = time()
        LIMITE = 10  # Indicar un número mayor que cero.
        solucion = profundidad_recursiva(problema=problema_resolver,
                                         limite=LIMITE,
                                         log=LOG,
                                         paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda primero en profundidad (versión iterativa).
    if LANZA_PROFUNDIDAD_ITERATIVA:
        print()
        print("**********************************************")
        print("***** PRIMERO EN PROFUNDIDAD (ITERATIVA) *****")
        print("**********************************************")
        inicio = time()
        LIMITE = 10  # Indicar un número mayor que cero.
        solucion = profundidad_iterativa(problema=problema_resolver,
                                         limite=LIMITE,
                                         log=LOG,
                                         paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda coste iterativo.
    if LANZA_COSTE_ITERATIVO:
        print()
        print("***************************")
        print("***** COSTE ITERATIVO *****")
        print("***************************")
        inicio = time()
        LIMITE = 500  # Indicar un número mayor que cero.
        solucion = coste_iterativo(problema=problema_resolver,
                                   limite=LIMITE,
                                   paso=100,
                                   log=LOG,
                                   paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(objetivo=solucion,
                         segundos=tiempo)

    # Búsqueda bidireccional.
    if LANZA_BIDIRECCIONAL:
        print()
        print("**************************")
        print("***** BIDIRECCIONAL *****")
        print("**************************")
        inicio = time()
        solucion = bidireccional(problema=problema_resolver,
                                 log=LOG,
                                 paso_a_paso=PASO_A_PASO)
        tiempo = time() - inicio
        muestra_solucion(es_bidireccional=True,
                         nodos_bidireccional=solucion,
                         segundos=tiempo)
