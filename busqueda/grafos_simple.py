#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estructura de Datos para Búsquedas.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""


# %%
class Accion:
    """Acción que se lleva a cabo en un estado para alcanzar otro estado."""

    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        """Representación en modo texto de la acción."""
        return self.nombre


# %%
class Estado:
    """Estado en el que se pueden encontrar el problema."""

    def __init__(self, nombre, acciones):
        self.nombre = nombre
        self.acciones = acciones

    def __str__(self):
        """Representación en modo texto del estado."""
        return self.nombre


# %%
class Problema:
    """Problema a resolver con un grafo."""

    def __init__(self, estado_inicial, estados_objetivos, acciones,
                 costes=None, heuristicas=None, infinito=99999):
        self.estado_inicial = estado_inicial
        self.estados_objetivos = estados_objetivos
        self.acciones = acciones
        self.costes = costes
        self.heuristicas = heuristicas
        self.infinito = infinito
        if not self.costes:
            self.costes = {}
            for estado in self.acciones.keys():
                self.costes[estado] = {}
                for accion in self.acciones[estado].keys():
                    self.costes[estado][accion] = 1
        if not self.heuristicas:
            self.heuristicas = {}
            for estado in self.acciones.keys():
                self.heuristicas[estado] = {}
                for objetivo in self.estados_objetivos:
                    self.heuristicas[estado][objetivo] = self.infinito

    def __str__(self):
        """Representación en modo texto del problema."""
        msg = "Estado Inicial: {0}; Objetivos: {1}"
        return msg.format(self.estado_inicial.nombre,
                          self.estados_objetivos)

    def es_objetivo(self, estado):
        """Indica si el estado indicado es uno de los estados objetivos."""
        return estado in self.estados_objetivos

    def resultado(self, estado, accion):
        """Nuevo estado de aplicar acción indicada en estado actual."""
        if estado.nombre not in self.acciones.keys():
            return None
        acciones_estado = self.acciones[estado.nombre]
        if accion.nombre not in acciones_estado.keys():
            return None
        return acciones_estado[accion.nombre]

    def coste_accion(self, estado, accion):
        """Devuelve el coste de aplicar una acción en un estado."""
        if estado.nombre not in self.costes.keys():
            return self.infinito
        costes_estado = self.costes[estado.nombre]
        if accion.nombre not in costes_estado.keys():
            return self.infinito
        return costes_estado[accion.nombre]

    def coste_camino(self, nodo):
        """Devuelve el coste total de recorrer el camino hasta un estado."""
        total = 0
        while nodo.padre:
            total += self.coste_accion(nodo.padre.estado, nodo.accion)
            nodo = nodo.padre
        return total


# %%
class Nodo:
    """Nodo del árbol usado para alcanzar una solución al problema."""

    def __init__(self, estado, accion=None, acciones=None, padre=None,
                 hijos=None):
        if hijos is None:
            hijos = []
        self.estado = estado
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos = []
        self.hijos.extend(hijos)
        self.coste = 0
        self.heuristicas = {}
        self.valores = {}
        self.alfa = 0
        self.beta = 0

    def __str__(self):
        """Representación en modo texto del nodo."""
        return self.estado.nombre

    def expandir(self, problema):
        """Crea todos los nodos hijos aplicando todas las acciones posibles."""
        self.hijos = []
        if not self.acciones:
            if self.estado.nombre not in problema.acciones.keys():
                return self.hijos
            self.acciones = problema.acciones[self.estado.nombre]
        for accion in self.acciones.keys():
            accion_hijo = Accion(accion)
            nuevo_estado = problema.resultado(self.estado, accion_hijo)
            acciones_nuevo = {}
            if nuevo_estado.nombre in problema.acciones.keys():
                acciones_nuevo = problema.acciones[nuevo_estado.nombre]
            hijo = Nodo(nuevo_estado, accion_hijo, acciones_nuevo, self)
            coste = self.padre.coste if self.padre else 0
            coste += problema.coste_accion(self.estado, accion_hijo)
            hijo.coste = coste
            hijo.heuristicas = problema.heuristicas[hijo.estado.nombre]
            hijo.valores = {estado: heuristica + hijo.coste
                            for estado, heuristica
                            in hijo.heuristicas.items()}
            self.hijos.append(hijo)
        return self.hijos

    def hijo_mejor(self, problema, metrica='valor', criterio='menor'):
        """Devuelve hijo con menor cantidad según un criterio."""
        if not self.hijos:
            return None
        mejor = self.hijos[0]
        for hijo in self.hijos:
            for objetivo in problema.estados_objetivos:
                if metrica == 'valor':
                    valor_hijo = hijo.valores[objetivo.nombre]
                    valor_mejor = mejor.valores[objetivo.nombre]
                    if(criterio == 'menor' and
                       valor_hijo < valor_mejor):
                        mejor = hijo
                    elif(criterio == 'mayor' and
                         valor_hijo > valor_mejor):
                        mejor = hijo
                elif metrica == 'heuristica':
                    heuristica_hijo = hijo.heuristicas[objetivo.nombre]
                    heuristica_mejor = mejor.heuristicas[objetivo.nombre]
                    if(criterio == 'menor' and
                       heuristica_hijo < heuristica_mejor):
                        mejor = hijo
                    elif(criterio == 'mayor' and
                         heuristica_hijo > heuristica_mejor):
                        mejor = hijo
                elif metrica == 'coste':
                    coste_camino_hijo = problema.coste_camino(hijo)
                    coste_camino_mejor = problema.coste_camino(mejor)
                    if(criterio == 'menor' and
                       coste_camino_hijo < coste_camino_mejor):
                        mejor = hijo
                    elif(criterio == 'mayor' and
                         coste_camino_hijo > coste_camino_mejor):
                        mejor = hijo
                elif metrica == 'alfa':
                    if(criterio == 'menor' and
                       hijo.alfa < mejor.alfa):
                        mejor = hijo
                    elif(criterio == 'mayor' and
                         hijo.alfa > mejor.alfa):
                        mejor = hijo
                elif metrica == 'beta':
                    if(criterio == 'menor' and
                       hijo.beta < mejor.beta):
                        mejor = hijo
                    elif(criterio == 'mayor' and
                         hijo.beta > mejor.beta):
                        mejor = hijo
        return mejor


# %%

if __name__ == '__main__':
    accN = Accion('norte')
    accS = Accion('sur')
    accE = Accion('este')
    accO = Accion('oeste')

    coruna = Estado('A Coruña', [accS, accE])
    bilbao = Estado('Bilbao', [accS, accE, accO])
    barcelona = Estado('Barcelona', [accS, accO])
    lisboa = Estado('Lisboa', [accN, accS, accE])
    madrid = Estado('Madrid', [accN, accS, accE, accO])
    valencia = Estado('Valencia', [accN, accS, accO])
    faro = Estado('Faro', [accN, accE])
    sevilla = Estado('Sevilla', [accN, accE, accO])
    granada = Estado('Granada', [accN, accO])

    viajes = {'A Coruña': {'sur': lisboa,
                           'este': bilbao},
              'Bilbao': {'sur': madrid,
                         'este': barcelona,
                         'oeste': coruna},
              'Barcelona': {'sur': valencia,
                            'oeste': bilbao},
              'Lisboa': {'norte': coruna,
                         'sur': faro,
                         'este': madrid},
              'Madrid': {'norte': bilbao,
                         'sur': sevilla,
                         'este': valencia,
                         'oeste': lisboa},
              'Valencia': {'norte': barcelona,
                           'sur': granada,
                           'oeste': madrid},
              'Faro': {'norte': lisboa,
                       'este': sevilla},
              'Sevilla': {'norte': madrid,
                          'este': granada,
                          'oeste': faro},
              'Granada': {'norte': valencia,
                          'oeste': sevilla}}

    kms = {'A Coruña': {'sur': 608,
                        'este': 545},
           'Bilbao': {'sur': 408,
                      'este': 613,
                      'oeste': 545},
           'Barcelona': {'sur': 350,
                         'oeste': 613},
           'Lisboa': {'norte': 608,
                      'sur': 278,
                      'este': 624},
           'Madrid': {'norte': 408,
                      'sur': 534,
                      'este': 357,
                      'oeste': 624},
           'Valencia': {'norte': 350,
                        'sur': 487,
                        'oeste': 357},
           'Faro': {'norte': 278,
                    'este': 200},
           'Sevilla': {'norte': 534,
                       'este': 252,
                       'oeste': 200},
           'Granada': {'norte': 487,
                       'oeste': 252}}

    distancias = {'A Coruña': {'A Coruña': 0,
                               'Bilbao': 443,
                               'Barcelona': 895,
                               'Lisboa': 522,
                               'Madrid': 509,
                               'Valencia': 797,
                               'Faro': 687,
                               'Sevilla': 696,
                               'Granada': 799},
                  'Bilbao': {'A Coruña': 443,
                             'Bilbao': 0,
                             'Barcelona': 468,
                             'Lisboa': 725,
                             'Madrid': 323,
                             'Valencia': 473,
                             'Faro': 807,
                             'Sevilla': 703,
                             'Granada': 678},
                  'Barcelona': {'A Coruña': 895,
                                'Bilbao': 468,
                                'Barcelona': 0,
                                'Lisboa': 1005,
                                'Madrid': 504,
                                'Valencia': 303,
                                'Faro': 1003,
                                'Sevilla': 828,
                                'Granada': 681},
                  'Lisboa': {'A Coruña': 522,
                             'Bilbao': 725,
                             'Barcelona': 1005,
                             'Lisboa': 0,
                             'Madrid': 502,
                             'Valencia': 760,
                             'Faro': 189,
                             'Sevilla': 314,
                             'Granada': 513},
                  'Madrid': {'A Coruña': 509,
                             'Bilbao': 323,
                             'Barcelona': 504,
                             'Lisboa': 502,
                             'Madrid': 0,
                             'Valencia': 303,
                             'Faro': 527,
                             'Sevilla': 390,
                             'Granada': 359},
                  'Valencia': {'A Coruña': 797,
                               'Bilbao': 473,
                               'Barcelona': 303,
                               'Lisboa': 760,
                               'Madrid': 303,
                               'Valencia': 0,
                               'Faro': 725,
                               'Sevilla': 540,
                               'Granada': 379},
                  'Faro': {'A Coruña': 708,
                           'Bilbao': 807,
                           'Barcelona': 1003,
                           'Lisboa': 189,
                           'Madrid': 527,
                           'Valencia': 725,
                           'Faro': 0,
                           'Sevilla': 195,
                           'Granada': 404},
                  'Sevilla': {'A Coruña': 696,
                              'Bilbao': 703,
                              'Barcelona': 828,
                              'Lisboa': 314,
                              'Madrid': 390,
                              'Valencia': 540,
                              'Faro': 195,
                              'Sevilla': 0,
                              'Granada': 210},
                  'Granada': {'A Coruña': 799,
                              'Bilbao': 678,
                              'Barcelona': 681,
                              'Lisboa': 513,
                              'Madrid': 359,
                              'Valencia': 379,
                              'Faro': 404,
                              'Sevilla': 210,
                              'Granada': 0}}

    problema_faro_bcn = Problema(faro, [barcelona], viajes, kms, distancias)

    acciones_faro = problema_faro_bcn.acciones['Faro']
    nodo_faro = Nodo(faro, None, acciones_faro, None)
    hijos_faro = nodo_faro.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_faro.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_faro])
    menor = nodo_faro.hijo_mejor(problema_faro_bcn)
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores['Barcelona']))

    este_sevilla = problema_faro_bcn.resultado(faro, accE)
    print("{0}".format(este_sevilla.nombre))
    acciones_sevilla = problema_faro_bcn.acciones['Sevilla']
    nodo_sevilla = Nodo(este_sevilla, accE, acciones_sevilla, nodo_faro)
    nodo_faro.hijos.append(nodo_sevilla)
    kms = problema_faro_bcn.coste_camino(nodo_sevilla)
    print("Coste: {0}".format(kms))
    heuristica = problema_faro_bcn.heuristicas['Sevilla']['Barcelona']
    print("Heurística: {0}".format(heuristica))
    valor = heuristica + kms
    print("Valor: {0}".format(valor))
    hijos_sevilla = nodo_sevilla.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_sevilla.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_sevilla])
    menor = nodo_sevilla.hijo_mejor(problema_faro_bcn)
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores['Barcelona']))

    norte_madrid = problema_faro_bcn.resultado(nodo_sevilla.estado, accN)
    print("{0}".format(norte_madrid.nombre))
    acciones_madrid = problema_faro_bcn.acciones['Madrid']
    nodo_madrid = Nodo(norte_madrid, accN, acciones_madrid, nodo_sevilla)
    nodo_sevilla.hijos.append(nodo_madrid)
    kms = problema_faro_bcn.coste_camino(nodo_madrid)
    print("Coste: {0}".format(kms))
    heuristica = problema_faro_bcn.heuristicas['Madrid']['Barcelona']
    print("Heurística: {0}".format(heuristica))
    valor = heuristica + kms
    print("Valor: {0}".format(valor))
    no_fin = problema_faro_bcn.es_objetivo(nodo_madrid.estado)
    print("Destino: {0}".format(no_fin))
    hijos_madrid = nodo_madrid.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_madrid.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_madrid])
    menor = nodo_madrid.hijo_mejor(problema_faro_bcn)
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores['Barcelona']))

    este_valencia = problema_faro_bcn.resultado(nodo_madrid.estado, accE)
    print("{0}".format(este_valencia.nombre))
    acciones_valencia = problema_faro_bcn.acciones['Valencia']
    nodo_valencia = Nodo(este_valencia, accE, acciones_valencia, nodo_madrid)
    nodo_madrid.hijos.append(nodo_valencia)
    kms = problema_faro_bcn.coste_camino(nodo_valencia)
    print("Coste: {0}".format(kms))
    heuristica = problema_faro_bcn.heuristicas['Valencia']['Barcelona']
    print("Heurística: {0}".format(heuristica))
    valor = heuristica + kms
    print("Valor: {0}".format(valor))
    hijos_valencia = nodo_valencia.expandir(problema_faro_bcn)
    print("Hijos de {0}:".format(nodo_valencia.estado.nombre))
    print([hijo.estado.nombre for hijo in hijos_valencia])
    menor = nodo_valencia.hijo_mejor(problema_faro_bcn)
    print("Hijo Menor Valor: {0} - {1}".format(
            menor.estado.nombre,
            menor.valores['Barcelona']))

    norte_barcelona = problema_faro_bcn.resultado(nodo_valencia.estado, accN)
    print("{0}".format(norte_barcelona.nombre))
    acc_barcelona = problema_faro_bcn.acciones['Barcelona']
    nodo_barcelona = Nodo(norte_barcelona, accN, acc_barcelona, nodo_valencia)
    nodo_valencia.hijos.append(nodo_barcelona)
    kms = problema_faro_bcn.coste_camino(nodo_barcelona)
    print("Coste: {0}".format(kms))
    heuristica = problema_faro_bcn.heuristicas['Barcelona']['Barcelona']
    print("Heurística: {0}".format(heuristica))
    valor = heuristica + kms
    print("Valor: {0}".format(valor))
    fin = problema_faro_bcn.es_objetivo(nodo_barcelona.estado)
    print("Destino: {0}".format(fin))
