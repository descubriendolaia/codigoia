#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diferentes algoritmos de búsqueda no informada en grafos.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""
from grafos import Accion
from grafos import Estado
from grafos import Nodo
from grafos import Problema


# %%
def anchura(problema):
    """Búsqueda en grafos primero en anchura (breadth-first search)."""
    raiz = crea_nodo_raiz(problema)
    if problema.es_objetivo(raiz.estado):
        return raiz
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = frontera.pop(0)
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if(hijo.estado not in explorados and
               hijo.estado not in estados_frontera):
                es_objetivo = problema.es_objetivo(hijo.estado)
                if es_objetivo:
                    return hijo
                frontera.append(hijo)


# %%
def coste_uniforme(problema):
    """Búsqueda en grafos de coste uniforme (uniform-cost search)."""
    raiz = crea_nodo_raiz(problema)
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = frontera.pop(0)
        if problema.es_objetivo(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if(hijo.estado not in explorados and
               hijo.estado not in estados_frontera):
                frontera.append(hijo)
            else:
                buscar = [nodo for nodo in frontera
                          if nodo.estado == hijo.estado]
                if buscar:
                    if hijo.coste < buscar[0].coste:
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
            frontera.sort(key=lambda nodo: nodo.coste)


# %%
def profundidad(problema):
    """Búsqueda en grafos primero en profundidad (depth-first search)."""
    raiz = crea_nodo_raiz(problema)
    if problema.es_objetivo(raiz.estado):
        return raiz
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = frontera.pop()
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if(hijo.estado not in explorados and
               hijo.estado not in estados_frontera):
                es_objetivo = problema.es_objetivo(hijo.estado)
                if es_objetivo:
                    return hijo
                frontera.append(hijo)


def profundidad_recursiva(problema, limite=99999):
    """Versión recursiva de la búsqueda en grafos primero en profundidad."""
    raiz = crea_nodo_raiz(problema)
    explorados = set()
    return __bpp_recursiva(raiz, problema, limite, explorados)


def __bpp_recursiva(nodo, problema, limite, explorados):
    """Función recursiva para realizar la búsqueda primero en profundidad."""
    if problema.es_objetivo(nodo.estado):
        return nodo
    if limite == 0:
        return None
    explorados.add(nodo.estado)
    if not nodo.acciones:
        return None
    for nombre_accion in nodo.acciones.keys():
        accion = Accion(nombre_accion)
        hijo = crea_nodo_hijo(problema, nodo, accion)
        if hijo.estado not in explorados:
            resultado = __bpp_recursiva(hijo, problema, limite - 1,
                                        explorados.copy())
            if resultado:
                return resultado
    return None


# %%
def profundidad_iterativa(problema, limite):
    """Versión iterativa de la búsqueda en profundidad."""
    if limite is None:
        return profundidad_recursiva(problema)
    for i in range(1, limite + 1):
        resultado = profundidad_recursiva(problema, i)
        if resultado:
            return resultado
    return None


# %%
def profundidad_iterativa_coste(problema, limite=99999, paso=1):
    """Búsqueda en profundidad iterativa pero con costes."""
    for i in range(1, limite + 1, paso):
        raiz = crea_nodo_raiz(problema)
        explorados = set()
        soluciones = []
        __coste_recursivo(raiz, problema, i, explorados, soluciones)
        if soluciones:
            mejor = min(soluciones, key=lambda nodo: nodo.coste)
            return mejor
    return None


def __coste_recursivo(nodo, problema, limite, explorados, soluciones):
    """Función recursiva de la busqueda en profundidad iterativa con costes."""
    if limite <= 0:
        return None
    if problema.es_objetivo(nodo.estado):
        soluciones.append(nodo)
        return nodo
    explorados.add(nodo.estado)
    if not nodo.acciones:
        return None
    for nombre_accion in nodo.acciones.keys():
        accion = Accion(nombre_accion)
        hijo = crea_nodo_hijo(problema, nodo, accion)
        if hijo.estado not in explorados:
            coste = problema.coste_accion(nodo.estado, accion)
            __coste_recursivo(hijo, problema, limite - coste,
                                          explorados.copy(), soluciones)
    return None


# %%
def bidireccional(problema):
    """Búsqueda que comienza en los nodos inicial y final a la vez."""
    raiz_i = crea_nodo_raiz(problema, problema.estado_inicial)
    raiz_f = crea_nodo_raiz(problema, problema.estados_objetivos[0])
    if problema.es_objetivo(raiz_i.estado):
        return (raiz_i, raiz_f)
    if problema.estado_inicial == raiz_f.estado:
        return (raiz_i, raiz_f)
    frontera_i = [raiz_i, ]
    frontera_f = [raiz_f, ]
    explorados_i = []
    explorados_f = []
    while True:
        if not frontera_i or not frontera_f:
            return (None, None)
        nodo_i = frontera_i.pop(0)
        nodo_f = frontera_f.pop(0)
        explorados_i.append(nodo_i)
        explorados_f.append(nodo_f)
        resultado_i = amplia_frontera(problema, nodo_i,
                                      problema.estados_objetivos[0],
                                      frontera_i, explorados_i)
        if resultado_i:
            return (resultado_i, None)
        resultado_f = amplia_frontera(problema, nodo_f,
                                      problema.estado_inicial,
                                      frontera_f, explorados_f)
        if resultado_f:
            return (None, resultado_f)
        estados_i = set(nodo.estado for nodo in frontera_i)
        estados_f = set(nodo.estado for nodo in frontera_f)
        estados_i = estados_i.union(set(nodo.estado for nodo in explorados_i))
        estados_f = estados_f.union(set(nodo.estado for nodo in explorados_f))
        comunes = estados_i.intersection(estados_f)
        if comunes:
            comun = comunes.pop()
            nodos_arbol_i = []
            nodos_arbol_f = []
            nodos_arbol_i.extend(frontera_i)
            nodos_arbol_f.extend(frontera_f)
            nodos_arbol_i.extend(explorados_i)
            nodos_arbol_f.extend(explorados_f)
            comun_i = [nodo for nodo in nodos_arbol_i
                       if nodo.estado == comun][0]
            comun_f = [nodo for nodo in nodos_arbol_f
                       if nodo.estado == comun][0]
            return (comun_i, comun_f)


def amplia_frontera(problema, nodo, objetivo, frontera, explorados):
    for nombre_accion in nodo.acciones.keys():
        accion = Accion(nombre_accion)
        hijo = crea_nodo_hijo(problema, nodo, accion)
        estados_frontera = [nodo.estado for nodo in frontera]
        estados_explorados = [nodo.estado for nodo in explorados]
        if(hijo.estado not in estados_explorados and
           hijo.estado not in estados_frontera):
            if objetivo == hijo.estado:
                return hijo
            frontera.append(hijo)
    return None


# %%
def crea_nodo_raiz(problema, estado=None):
    """Crea y devuelve el nodo raíz del problema indicado."""
    estado_raiz = estado or problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, acciones=acciones_raiz)
    raiz.coste = 0
    return raiz


def crea_nodo_hijo(problema, padre, accion):
    """Crea y devuelve el nodo hijo."""
    nuevo_estado = problema.resultado(padre.estado, accion)
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo, padre)
    coste = padre.coste
    coste += problema.coste_accion(padre.estado, accion)
    hijo.coste = coste
    padre.hijos.append(hijo)
    return hijo


def muestra_solucion(objetivo=None, es_bidireccional=False,
                     nodos_bidireccional=(None, None)):
    """Muestra la solución encuentrada a partir de un nodo objetivo."""
    if es_bidireccional:
        nodo_i = nodos_bidireccional[0]
        nodo_f = nodos_bidireccional[1]
        coste_i = nodo_i.coste if nodo_i else 0
        coste_f = nodo_f.coste if nodo_f else 0
        camino = []
        if nodo_i:
            while nodo_i:
                camino.insert(0, nodo_i)
                nodo_i = nodo_i.padre
        if nodo_f:
            nodo_f = nodo_f.padre
            while nodo_f:
                camino.append(nodo_f)
                nodo_f = nodo_f.padre
        if not camino:
            print("No hay solución")
            return
        for nodo in camino:
            msg = "Estado: {0}"
            print(msg.format(nodo.estado.nombre))
        msg = "Coste Total: {0}"
        print(msg.format(coste_i + coste_f))
    else:
        if not objetivo:
            print("No hay solución")
            return
        nodo = objetivo
        while nodo:
            msg = "Estado: {0}, Coste Total: {1}"
            estado = nodo.estado.nombre
            coste_total = nodo.coste
            print(msg.format(estado, coste_total))
            if nodo.accion:
                accion = nodo.accion.nombre
                padre = nodo.padre.estado
                coste = problema_resolver.coste_accion(padre, nodo.accion)
                if accion:
                    msg = "<--- {0} [{1}] ---"
                    print(msg.format(accion, coste))
            nodo = nodo.padre


# %%
if __name__ == '__main__':
    accN = Accion('N')
    accS = Accion('S')
    accE = Accion('E')
    accO = Accion('O')
    accNE = Accion('NE')
    accNO = Accion('NO')
    accSE = Accion('SE')
    accSO = Accion('SO')

    lanoi = Estado('Lanoi', [accNE])
    nohoi = Estado('Nohoi', [accSO, accNO, accNE])
    ruun = Estado('Ruun', [accNO, accNE, accE, accSE])
    milos = Estado('Milos', [accO, accSO, accN])
    ghiido = Estado('Ghiido', [accN, accE, accSE])
    kuart = Estado('Kuart', [accO, accSO, accNE])
    boomon = Estado('Boomon', [accN, accSO])
    goorum = Estado('Goorum', [accO, accS])
    shiphos = Estado('Shiphos', [accO, accE])
    nokshos = Estado('Nokshos', [accNO, accS, accE])
    pharis = Estado('Pharis', [accNO, accSO])
    khamin = Estado('Khamin', [accSE, accNO, accO])
    tarios = Estado('Tarios', [accO, accNO, accNE, accE])
    peranna = Estado('Peranna', [accO, accE])
    khandan = Estado('Khandan', [accO, accS])
    tawa = Estado('Tawa', [accSO, accSE, accNE])
    theer = Estado('Theer', [accSO, accSE])
    roria = Estado('Roria', [accNO, accSO, accE])
    kosos = Estado('Kosos', [accO])

    acciones = {'Lanoi': {'NE': nohoi},
                'Nohoi': {'SO': lanoi,
                          'NO': ruun,
                          'NE': milos},
                'Ruun': {'NO': ghiido,
                         'NE': kuart,
                         'E': milos,
                         'SE': nohoi},
                'Milos': {'O': ruun,
                          'SO': nohoi,
                          'N': khandan},
                'Ghiido': {'N': nokshos,
                           'E': kuart,
                           'SE': ruun},
                'Kuart': {'O': ghiido,
                          'SO': ruun,
                          'NE': boomon},
                'Boomon': {'N': goorum,
                           'SO': kuart},
                'Goorum': {'O': shiphos,
                           'S': boomon},
                'Shiphos': {'O': nokshos,
                            'E': goorum},
                'Nokshos': {'NO': pharis,
                            'S': ghiido,
                            'E': shiphos},
                'Pharis': {'NO': khamin,
                           'SO': nokshos},
                'Khamin': {'SE': pharis,
                           'NO': tawa,
                           'O': tarios},
                'Tarios': {'O': khamin,
                           'NO': tawa,
                           'NE': roria,
                           'E': peranna},
                'Peranna': {'O': tarios,
                            'E': khandan},
                'Khandan': {'O': peranna,
                            'S': milos},
                'Tawa': {'SO': khamin,
                         'SE': tarios,
                         'NE': theer},
                'Theer': {'SO': tawa,
                          'SE': roria},
                'Roria': {'NO': theer,
                          'SO': tarios,
                          'E': kosos},
                'Kosos': {'O': roria}}

    costes = {'Lanoi': {'NE': 42},
              'Nohoi': {'SO': 42,
                        'NO': 21,
                        'NE': 95},
              'Ruun': {'NO': 88,
                       'NE': 16,
                       'E': 90,
                       'SE': 21},
              'Milos': {'O': 90,
                        'SO': 95,
                        'N': 133},
              'Ghiido': {'N': 17,
                         'E': 92,
                         'SE': 88},
              'Kuart': {'O': 92,
                        'SO': 16,
                        'NE': 83},
              'Boomon': {'N': 8,
                         'SO': 83},
              'Goorum': {'O': 59,
                         'S': 8},
              'Shiphos': {'O': 71,
                          'E': 59},
              'Nokshos': {'NO': 5,
                          'S': 17,
                          'E': 71},
              'Pharis': {'NO': 29,
                         'SO': 5},
              'Khamin': {'SE': 29,
                         'NO': 121,
                         'O': 98},
              'Tarios': {'O': 98,
                         'NO': 83,
                         'NE': 57,
                         'E': 82},
              'Peranna': {'O': 82,
                          'E': 44},
              'Khandan': {'O': 44,
                          'S': 133},
              'Tawa': {'SO': 121,
                       'SE': 83,
                       'NE': 11},
              'Theer': {'SO': 11,
                        'SE': 36},
              'Roria': {'NO': 36,
                        'SO': 57,
                        'E': 104},
              'Kosos': {'O': 104}}

    objetivo_1 = [kosos]
    problema_1 = Problema(lanoi, objetivo_1, acciones, costes)

    objetivo_2 = [goorum]
    problema_2 = Problema(lanoi, objetivo_2, acciones, costes)

    objetivo_3 = [boomon, goorum]
    problema_3 = Problema(lanoi, objetivo_3, acciones, costes)

    LANZA_ANCHURA = True
    LANZA_COSTE_UNIFORME = True
    LANZA_PROFUNDIDAD = True
    LANZA_PROFUNDIDAD_RECURSIVA = True
    LANZA_PROFUNDIDAD_LIMITADA = True
    LANZA_PROFUNDIDAD_ITERATIVA = True
    LANZA_PROFUNDIDAD_ITERATIVA_COSTES = True
    LANZA_BIDIRECCIONAL = True

    problema_resolver = problema_1

    if LANZA_ANCHURA:
        print("***** PRIMERO EN ANCHURA *****")
        solucion = anchura(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_COSTE_UNIFORME:
        print("***** COSTE UNIFORME *****")
        solucion = coste_uniforme(problema_resolver)
        muestra_solucion(solucion,)

    if LANZA_PROFUNDIDAD:
        print("***** PRIMERO EN PROFUNDIDAD *****")
        solucion = profundidad(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_PROFUNDIDAD_RECURSIVA:
        print("***** PRIMERO EN PROFUNDIDAD (RECURSIVA) *****")
        solucion = profundidad_recursiva(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_PROFUNDIDAD_LIMITADA:
        print("***** PRIMERO EN PROFUNDIDAD (LIMITADA) *****")
        LIMITE = 10
        solucion = profundidad_recursiva(problema_resolver, LIMITE)
        muestra_solucion(solucion)

    if LANZA_PROFUNDIDAD_ITERATIVA:
        print("***** PRIMERO EN PROFUNDIDAD (ITERATIVA) *****")
        LIMITE = 10
        solucion = profundidad_iterativa(problema_resolver, LIMITE)
        muestra_solucion(solucion)

    if LANZA_PROFUNDIDAD_ITERATIVA_COSTES:
        print("***** PRIMERO EN PROFUNDIDAD (ITERATIVA) CON COSTES *****")
        LIMITE = 1000
        PASO = 100
        solucion = profundidad_iterativa_coste(problema_resolver, LIMITE, PASO)
        muestra_solucion(solucion)

    if LANZA_BIDIRECCIONAL:
        print("***** BIDIRECCIONAL *****")
        solucion = bidireccional(problema_resolver)
        muestra_solucion(es_bidireccional=True,
                         nodos_bidireccional=solucion)
