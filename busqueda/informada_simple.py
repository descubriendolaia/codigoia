#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diferentes algoritmos de búsqueda informada en grafos.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""
from grafos import Accion
from grafos import Estado
from grafos import Nodo
from grafos import Problema


# %%
def voraz(problema):
    """Búsqueda en grafos voraz (greedy search)."""
    raiz = crea_nodo_raiz(problema)
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = sacar_siguiente(frontera, 'heuristica',
                               objetivos=problema.estados_objetivos)
        if problema.es_objetivo(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if hijo.estado in explorados or hijo.estado in estados_frontera:
                buscar = [nodo for nodo in frontera
                          if nodo.estado == hijo.estado]
                if buscar:
                    heuristic_hijo = [hijo.heuristicas[objetivo.nombre]
                                      for objetivo
                                      in problema.estados_objetivos]
                    heuristic_buscar = [buscar[0].heuristicas[objetivo.nombre]
                                        for objetivo
                                        in problema.estados_objetivos]
                    minimo_hijo = min(heuristic_hijo)
                    minimo_buscar = min(heuristic_buscar)
                    if minimo_hijo < minimo_buscar:
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
            else:
                frontera.append(hijo)


# %%
def a_estrella(problema):
    """Búsqueda A* (que se lee 'A estrella')."""
    raiz = crea_nodo_raiz(problema)
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = sacar_siguiente(frontera, 'valor',
                               objetivos=problema.estados_objetivos)
        if problema.es_objetivo(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if hijo.estado in explorados or hijo.estado in estados_frontera:
                buscar = [nodo for nodo in frontera
                          if nodo.estado == hijo.estado]
                if buscar:
                    valores_hijo = [hijo.valores[objetivo.nombre]
                                    for objetivo
                                    in problema.estados_objetivos]
                    valores_buscar = [buscar[0].valores[objetivo.nombre]
                                      for objetivo
                                      in problema.estados_objetivos]
                    minimo_hijo = min(valores_hijo)
                    minimo_buscar = min(valores_buscar)
                    if minimo_hijo < minimo_buscar:
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
            else:
                frontera.append(hijo)


# %%
def a_estrella_iterativa(problema, nodo=None, limite=0, explorados=None):
    """Búsqueda A* iterativa que buscará hasta un límite máximo."""
    if not nodo:
        nodo = crea_nodo_raiz(problema)
    if explorados is None:
        explorados = set()
    else:
        explorados.add(nodo.estado)
    if limite <= 0:
        limite = problema.infinito
    valor_nodo = min([nodo.valores[objetivo.nombre]
                      for objetivo in problema.estados_objetivos])
    if valor_nodo > limite:
        return None, valor_nodo
    if problema.es_objetivo(nodo.estado):
        return nodo, limite
    if not nodo.acciones:
        return None, limite
    minimo = problema.infinito
    for nombre_accion in nodo.acciones.keys():
        accion = Accion(nombre_accion)
        hijo = crea_nodo_hijo(problema, nodo, accion)
        if hijo.estado not in explorados:
            nod_hijo, lim_hijo = a_estrella_iterativa(problema, hijo,
                                                      limite, explorados)
            if nod_hijo:
                return nod_hijo, lim_hijo
            if lim_hijo < minimo:
                minimo = lim_hijo
    return None, minimo


# %%
def ida_estrella(problema):
    """Búsqueda IDA* (Iterative Deepening A*)."""
    raiz = crea_nodo_raiz(problema)
    limite = min([raiz.heuristicas[objetivo.nombre]
                  for objetivo in problema.estados_objetivos])
    while True:
        explorados = set()
        nodo, limite = a_estrella_iterativa(problema, raiz, limite,
                                            explorados)
        if nodo:
            return nodo
        if limite == problema.infinito:
            return None


# %%
def recursiva_primero_mejor(problema):
    """Búsqueda recursiva primero el mejor (Recursive Best-First Search)."""
    raiz = crea_nodo_raiz(problema)
    raiz.alfa = 0
    limite = problema.infinito
    explorados = set()
    return _brpm_recursiva(problema, raiz, limite, explorados)


def _brpm_recursiva(problema, nodo, limite, explorados):
    """Función recursiva para búsqueda recursiva primero el mejor."""
    explorados.add(nodo.estado)
    if limite <= 0:
        limite = problema.infinito
    if problema.es_objetivo(nodo.estado):
        return nodo, limite
    if not nodo.acciones:
        return None, limite
    for nombre_accion in nodo.acciones.keys():
        accion = Accion(nombre_accion)
        hijo = crea_nodo_hijo(problema, nodo, accion, False)
        if hijo.estado not in explorados:
            hijo.padre = nodo
            nodo.hijos.append(hijo)
            maximo = max([hijo.valores[objetivo.nombre]
                          for objetivo in problema.estados_objetivos])
            hijo.alfa = max(maximo, nodo.alfa)
    if not nodo.hijos:
        return None, problema.infinito
    while True:
        objetivos = problema.estados_objetivos
        mejor = nodo.hijo_mejor(problema, metrica='alfa')
        if mejor.alfa > limite:
            return None, mejor.alfa
        hijos = nodo.hijos.copy()
        nodo.hijos.remove(mejor)
        alfa = limite
        if nodo.hijos:
            alternativa = nodo.hijo_mejor(problema, metrica='alfa')
            alfa = min(limite, alternativa.alfa)
        nodo.hijos = hijos
        resultado, mejor.alfa = _brpm_recursiva(problema, mejor, alfa,
                                                explorados)
        if resultado:
            return resultado, mejor.alfa


# %%
def sma_estrella(problema, maximo_nodos=10):
    """Búsqueda A* para memoria limitada (Simplified Memory-Bounded A*)."""
    raiz = crea_nodo_raiz(problema)
    frontera = [raiz, ]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = sacar_siguiente(frontera, 'valor',
                               objetivos=problema.estados_objetivos)
        if problema.es_objetivo(nodo.estado):
            return nodo
        explorados.add(nodo.estado)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            estados_frontera = [nodo.estado for nodo in frontera]
            if hijo.estado in explorados or hijo.estado in estados_frontera:
                buscar = [nodo for nodo in frontera
                          if nodo.estado == hijo.estado]
                if buscar:
                    valores_hijo = [hijo.valores[objetivo.nombre]
                                    for objetivo
                                    in problema.estados_objetivos]
                    valores_buscar = [buscar[0].valores[objetivo.nombre]
                                      for objetivo
                                      in problema.estados_objetivos]
                    minimo_hijo = min(valores_hijo)
                    minimo_buscar = min(valores_buscar)
                    if minimo_hijo < minimo_buscar:
                        indice = frontera.index(buscar[0])
                        frontera[indice] = hijo
            else:
                if len(frontera) > maximo_nodos:
                    ordenador = lambda x: [x.valores[objetivo.nombre]
                                           for objetivo
                                           in problema.estados_objetivos]
                    frontera = sorted(frontera, key=ordenador)
                    frontera.pop()
                frontera.append(hijo)


# %%
def crea_nodo_raiz(problema):
    """Método auxiliar que ayudará a crear nodos raíz."""
    estado_raiz = problema.estado_inicial
    acciones_raiz = {}
    if estado_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[estado_raiz.nombre]
    raiz = Nodo(estado_raiz, acciones=acciones_raiz)
    raiz.coste = 0
    raiz.heuristicas = problema.heuristicas[estado_raiz.nombre]
    raiz.valores = dict(raiz.heuristicas.items())
    return raiz


def crea_nodo_hijo(problema, padre, accion, agregar=True):
    """Creación de nodos hijos."""
    nuevo_estado = problema.resultado(padre.estado, accion)
    acciones_nuevo = {}
    if nuevo_estado.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nuevo_estado.nombre]
    hijo = Nodo(nuevo_estado, accion, acciones_nuevo)
    coste = padre.coste
    coste += problema.coste_accion(padre.estado, accion)
    hijo.coste = coste
    hijo.heuristicas = problema.heuristicas[hijo.estado.nombre]
    hijo.valores = {estado: heuristica + hijo.coste
                    for estado, heuristica
                    in hijo.heuristicas.items()}
    if agregar:
        hijo.padre = padre
        padre.hijos.append(hijo)
    return hijo


def sacar_siguiente(frontera, metrica='valor', criterio='menor',
                    objetivos=None):
    """Devuelve el siguiente nodo de la frontera según un criterio."""
    if not frontera:
        return None
    mejor = frontera[0]
    for nodo in frontera[1:]:
        for objetivo in objetivos:
            if metrica == 'valor':
                valor_nodo = nodo.valores[objetivo.nombre]
                valor_mejor = mejor.valores[objetivo.nombre]
                if(criterio == 'menor' and
                   valor_nodo < valor_mejor):
                    mejor = nodo
                elif(criterio == 'mayor' and
                     valor_nodo > valor_mejor):
                    mejor = nodo
            elif metrica == 'heuristica':
                heuristica_nodo = nodo.heuristicas[objetivo.nombre]
                heuristica_mejor = mejor.heuristicas[objetivo.nombre]
                if(criterio == 'menor' and
                   heuristica_nodo < heuristica_mejor):
                    mejor = nodo
                elif(criterio == 'mayor' and
                     heuristica_nodo > heuristica_mejor):
                    mejor = nodo
            elif metrica == 'coste':
                if(criterio == 'menor' and
                   nodo.coste_camino < mejor.coste_camino):
                    mejor = nodo
                elif(criterio == 'mayor' and
                     nodo.coste_camino > mejor.coste_camino):
                    mejor = nodo
    frontera.remove(mejor)
    return mejor


def muestra_solucion(objetivo=None):
    """Muestra la solución encuentrada a partir de un nodo objetivo."""
    if not objetivo:
        print("No hay solución")
        return
    nodo = objetivo
    while nodo:
        msg = "Estado {0}, Valor {1}"
        estado = nodo.estado.nombre
        valores = [nodo.valores[objetivo.nombre]
                   for objetivo
                   in problema_resolver.estados_objetivos]
        valor = min(valores)
        print(msg.format(estado, valor))
        msg = "  Coste: {0}"
        coste_total = nodo.coste
        print(msg.format(coste_total))
        msg = "  Heurística: {0}"
        heuristicas_objetivos = [nodo.heuristicas[objetivo.nombre]
                                 for objetivo
                                 in problema_resolver.estados_objetivos]
        heuristica = min(heuristicas_objetivos)
        print(msg.format(heuristica))
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

    heuristicas = {'Lanoi': {'Lanoi': 0,
                             'Nohoi': 32,
                             'Ruun': 43,
                             'Milos': 90,
                             'Ghiido': 81,
                             'Kuart': 50,
                             'Boomon': 90,
                             'Goorum': 95,
                             'Shiphos': 84,
                             'Nokshos': 108,
                             'Pharis': 111,
                             'Khamin': 124,
                             'Tarios': 145,
                             'Peranna': 157,
                             'Khandan': 182,
                             'Tawa': 180,
                             'Theer': 183,
                             'Roria': 174,
                             'Kosos': 224},
                   'Nohoi': {'Lanoi': 32,
                             'Nohoi': 0,
                             'Ruun': 12,
                             'Milos': 72,
                             'Ghiido': 73,
                             'Kuart': 18,
                             'Boomon': 57,
                             'Goorum': 63,
                             'Shiphos': 56,
                             'Nokshos': 93,
                             'Pharis': 97,
                             'Khamin': 107,
                             'Tarios': 117,
                             'Peranna': 125,
                             'Khandan': 150,
                             'Tawa': 153,
                             'Theer': 154,
                             'Roria': 143,
                             'Kosos': 191},
                   'Ruun': {'Lanoi': 43,
                            'Nohoi': 12,
                            'Ruun': 0,
                            'Milos': 71,
                            'Ghiido': 75,
                            'Kuart': 6,
                            'Boomon': 45,
                            'Goorum': 50,
                            'Shiphos': 45,
                            'Nokshos': 87,
                            'Pharis': 89,
                            'Khamin': 100,
                            'Tarios': 105,
                            'Peranna': 103,
                            'Khandan': 140,
                            'Tawa': 140,
                            'Theer': 142,
                            'Roria': 131,
                            'Kosos': 179},
                   'Milos': {'Lanoi': 90,
                             'Nohoi': 72,
                             'Ruun': 71,
                             'Milos': 0,
                             'Ghiido': 145,
                             'Kuart': 70,
                             'Boomon': 76,
                             'Goorum': 81,
                             'Shiphos': 103,
                             'Nokshos': 156,
                             'Pharis': 157,
                             'Khamin': 165,
                             'Tarios': 138,
                             'Peranna': 116,
                             'Khandan': 122,
                             'Tawa': 176,
                             'Theer': 174,
                             'Roria': 159,
                             'Kosos': 172},
                   'Ghiido': {'Lanoi': 81,
                              'Nohoi': 73,
                              'Ruun': 75,
                              'Milos': 145,
                              'Ghiido': 0,
                              'Kuart': 75,
                              'Boomon': 94,
                              'Goorum': 93,
                              'Shiphos': 61,
                              'Nokshos': 34,
                              'Pharis': 37,
                              'Khamin': 53,
                              'Tarios': 112,
                              'Peranna': 150,
                              'Khandan': 187,
                              'Tawa': 134,
                              'Theer': 140,
                              'Roria': 136,
                              'Kosos': 211},
                   'Kuart': {'Lanoi': 50,
                             'Nohoi': 18,
                             'Ruun': 6,
                             'Milos': 70,
                             'Ghiido': 75,
                             'Kuart': 0,
                             'Boomon': 38,
                             'Goorum': 43,
                             'Shiphos': 42,
                             'Nokshos': 87,
                             'Pharis': 89,
                             'Khamin': 98,
                             'Tarios': 98,
                             'Peranna': 107,
                             'Khandan': 134,
                             'Tawa': 135,
                             'Theer': 137,
                             'Roria': 124,
                             'Kosos': 173},
                   'Boomon': {'Lanoi': 90,
                              'Nohoi': 57,
                              'Ruun': 45,
                              'Milos': 76,
                              'Ghiido': 94,
                              'Kuart': 38,
                              'Boomon': 0,
                              'Goorum': 6,
                              'Shiphos': 36,
                              'Nokshos': 91,
                              'Pharis': 91,
                              'Khamin': 95,
                              'Tarios': 67,
                              'Peranna': 68,
                              'Khandan': 98,
                              'Tawa': 105,
                              'Theer': 104,
                              'Roria': 91,
                              'Kosos': 134},
                   'Goorum': {'Lanoi': 95,
                              'Nohoi': 63,
                              'Ruun': 50,
                              'Milos': 81,
                              'Ghiido': 93,
                              'Kuart': 43,
                              'Boomon': 6,
                              'Goorum': 0,
                              'Shiphos': 33,
                              'Nokshos': 88,
                              'Pharis': 87,
                              'Khamin': 92,
                              'Tarios': 62,
                              'Peranna': 64,
                              'Khandan': 97,
                              'Tawa': 98,
                              'Theer': 98,
                              'Roria': 85,
                              'Kosos': 132},
                   'Shiphos': {'Lanoi': 84,
                               'Nohoi': 56,
                               'Ruun': 45,
                               'Milos': 103,
                               'Ghiido': 61,
                               'Kuart': 42,
                               'Boomon': 36,
                               'Goorum': 33,
                               'Shiphos': 0,
                               'Nokshos': 55,
                               'Pharis': 55,
                               'Khamin': 63,
                               'Tarios': 64,
                               'Peranna': 92,
                               'Khandan': 127,
                               'Tawa': 97,
                               'Theer': 101,
                               'Roria': 92,
                               'Kosos': 156},
                   'Nokshos': {'Lanoi': 108,
                               'Nohoi': 93,
                               'Ruun': 87,
                               'Milos': 156,
                               'Ghiido': 34,
                               'Kuart': 87,
                               'Boomon': 91,
                               'Goorum': 88,
                               'Shiphos': 55,
                               'Nokshos': 0,
                               'Pharis': 3,
                               'Khamin': 18,
                               'Tarios': 86,
                               'Peranna': 133,
                               'Khandan': 171,
                               'Tawa': 103,
                               'Theer': 109,
                               'Roria': 109,
                               'Kosos': 189},
                   'Pharis': {'Lanoi': 111,
                              'Nohoi': 97,
                              'Ruun': 89,
                              'Milos': 157,
                              'Ghiido': 37,
                              'Kuart': 89,
                              'Boomon': 91,
                              'Goorum': 87,
                              'Shiphos': 55,
                              'Nokshos': 3,
                              'Pharis': 0,
                              'Khamin': 14,
                              'Tarios': 83,
                              'Peranna': 132,
                              'Khandan': 170,
                              'Tawa': 100,
                              'Theer': 107,
                              'Roria': 105,
                              'Kosos': 186},
                   'Khamin': {'Lanoi': 124,
                              'Nohoi': 107,
                              'Ruun': 100,
                              'Milos': 165,
                              'Ghiido': 53,
                              'Kuart': 98,
                              'Boomon': 95,
                              'Goorum': 92,
                              'Shiphos': 63,
                              'Nokshos': 18,
                              'Pharis': 14,
                              'Khamin': 0,
                              'Tarios': 77,
                              'Peranna': 128,
                              'Khandan': 168,
                              'Tawa': 89,
                              'Theer': 97,
                              'Roria': 97,
                              'Kosos': 182},
                   'Tarios': {'Lanoi': 145,
                              'Nohoi': 117,
                              'Ruun': 105,
                              'Milos': 138,
                              'Ghiido': 112,
                              'Kuart': 98,
                              'Boomon': 67,
                              'Goorum': 62,
                              'Shiphos': 64,
                              'Nokshos': 86,
                              'Pharis': 83,
                              'Khamin': 77,
                              'Tarios': 0,
                              'Peranna': 55,
                              'Khandan': 94,
                              'Tawa': 38,
                              'Theer': 38,
                              'Roria': 27,
                              'Kosos': 104},
                   'Peranna': {'Lanoi': 157,
                               'Nohoi': 125,
                               'Ruun': 103,
                               'Milos': 116,
                               'Ghiido': 150,
                               'Kuart': 107,
                               'Boomon': 68,
                               'Goorum': 64,
                               'Shiphos': 92,
                               'Nokshos': 133,
                               'Pharis': 132,
                               'Khamin': 128,
                               'Tarios': 55,
                               'Peranna': 0,
                               'Khandan': 38,
                               'Tawa': 80,
                               'Theer': 73,
                               'Roria': 59,
                               'Kosos': 66},
                   'Khandan': {'Lanoi': 182,
                               'Nohoi': 150,
                               'Ruun': 140,
                               'Milos': 122,
                               'Ghiido': 187,
                               'Kuart': 134,
                               'Boomon': 98,
                               'Goorum': 97,
                               'Shiphos': 127,
                               'Nokshos': 171,
                               'Pharis': 170,
                               'Khamin': 168,
                               'Tarios': 94,
                               'Peranna': 38,
                               'Khandan': 0,
                               'Tawa': 113,
                               'Theer': 107,
                               'Roria': 92,
                               'Kosos': 52},
                   'Tawa': {'Lanoi': 180,
                            'Nohoi': 153,
                            'Ruun': 140,
                            'Milos': 176,
                            'Ghiido': 134,
                            'Kuart': 135,
                            'Boomon': 105,
                            'Goorum': 98,
                            'Shiphos': 97,
                            'Nokshos': 103,
                            'Pharis': 100,
                            'Khamin': 89,
                            'Tarios': 38,
                            'Peranna': 80,
                            'Khandan': 113,
                            'Tawa': 0,
                            'Theer': 9,
                            'Roria': 21,
                            'Kosos': 105},
                   'Theer': {'Lanoi': 183,
                             'Nohoi': 154,
                             'Ruun': 142,
                             'Milos': 174,
                             'Ghiido': 140,
                             'Kuart': 137,
                             'Boomon': 104,
                             'Goorum': 98,
                             'Shiphos': 101,
                             'Nokshos': 109,
                             'Pharis': 107,
                             'Khamin': 97,
                             'Tarios': 38,
                             'Peranna': 73,
                             'Khandan': 107,
                             'Tawa': 9,
                             'Theer': 0,
                             'Roria': 16,
                             'Kosos': 96},
                   'Roria': {'Lanoi': 174,
                             'Nohoi': 143,
                             'Ruun': 131,
                             'Milos': 159,
                             'Ghiido': 136,
                             'Kuart': 124,
                             'Boomon': 91,
                             'Goorum': 85,
                             'Shiphos': 92,
                             'Nokshos': 109,
                             'Pharis': 105,
                             'Khamin': 97,
                             'Tarios': 27,
                             'Peranna': 59,
                             'Khandan': 92,
                             'Tawa': 21,
                             'Theer': 16,
                             'Roria': 0,
                             'Kosos': 87},
                   'Kosos': {'Lanoi': 224,
                             'Nohoi': 191,
                             'Ruun': 179,
                             'Milos': 172,
                             'Ghiido': 211,
                             'Kuart': 173,
                             'Boomon': 134,
                             'Goorum': 132,
                             'Shiphos': 156,
                             'Nokshos': 189,
                             'Pharis': 186,
                             'Khamin': 182,
                             'Tarios': 104,
                             'Peranna': 66,
                             'Khandan': 52,
                             'Tawa': 105,
                             'Theer': 96,
                             'Roria': 87,
                             'Kosos': 0}}

    objetivo_1 = [kosos]
    problema_1 = Problema(lanoi, objetivo_1, acciones, costes, heuristicas)

    objetivo_2 = [goorum]
    problema_2 = Problema(lanoi, objetivo_2, acciones, costes, heuristicas)

    objetivo_3 = [boomon, goorum]
    problema_3 = Problema(lanoi, objetivo_3, acciones, costes, heuristicas)

    LANZA_VORAZ = True
    LANZA_A_ESTRELLA = True
    LANZA_IDA_ESTRELLA = True
    LANZA_RECURSIVA_PRIMER_MEJOR = True
    LANZA_SMA_ESTRELLA = True

    problema_resolver = problema_1

    if LANZA_VORAZ:
        print("***** VORAZ *****")
        solucion = voraz(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_A_ESTRELLA:
        print("***** A* *****")
        solucion = a_estrella(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_IDA_ESTRELLA:
        print("***** IDA* *****")
        solucion = ida_estrella(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_RECURSIVA_PRIMER_MEJOR:
        print("***** RECURSIVA PRIMERO MEJOR *****")
        solucion, _ = recursiva_primero_mejor(problema_resolver)
        muestra_solucion(solucion)

    if LANZA_SMA_ESTRELLA:
        print("***** SMA* *****")
        solucion = sma_estrella(problema_resolver, maximo_nodos=1)
        muestra_solucion(solucion,)
