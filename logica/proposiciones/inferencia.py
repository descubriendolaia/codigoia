#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Métodos de inferencia en lógica de proposiciones.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""
from motor import Proposicion
from motor import Constante
from motor import Variable


# %% --- FUNCIONES AUXILIARES -------------------------------------------------

def _crea_proposicion(valor):
    """
    Se encarga de devolver un tipo de proposición acorde al valor pasado.

    Argumentos:
    - valor: valor a comprobar de qué tipo de proposición es.

    Devuelve: instancia de Proposicion, Variable o Constante, según valor.
    """
    # Si ya es una proposición, la devolvemos tal cual.
    if isinstance(valor, Proposicion):
        return valor

    # Si es una cadena de texto, creamos una variable.
    if isinstance(valor, str):
        return Variable(valor)

    # Si es un booleano, creamos una constante.
    if isinstance(valor, bool):
        return Constante(valor)

    # En caso constrario, es un error.
    err = "No se pudo crear una proposición a partir de {0}"
    raise ValueError(err.format(valor))


# %% --- TABLA DE VERDAD ------------------------------------------------------

def tabla_verdad(*premisas,
                 conclusion,
                 variables=None,
                 simbolos=None,
                 modelo=None):
    """
    Realiza inferencia en lógica de proposiones.

    Mediante la construcción y análisis de todas la combinaciones posibles de
    valores de símbolos en una tabla de verdad.

    Argumentos:
    - premisas: todos los argumentos, salvo el último, serán las premisas.
    - conclusion: el último argumento es la conclusión a ver si es válida.
    - variables: variables que se han usado en las premisas y la conclusión.
    - simbolos: lista de variables que un quedan por probar sus valores.
    - modelo: conjunto de combinaciones de valores de variables ya probadas.

    Devuelve: nada.
    """
    # Comprobaciones.
    if not conclusion:
        raise ValueError("Debe indicar una conclusión")

    # Si no nos pasan variables, las cogemos de las premisas y conclusión.
    if not variables:
        variables = list(frozenset.union(conclusion.variables(),
                                         *[premisa.variables()
                                           for premisa in premisas]))

    # Creamos la base de conocimiento con las premisas.
    base_conocimiento = [_crea_proposicion(premisa)
                         for premisa in premisas]

    # Creamos una proposición con la conclusión.
    demuestra = _crea_proposicion(conclusion)

    # Si no han pasado los símbolos, la iniciamos con las variables.
    if simbolos is None:
        simbolos = []
        simbolos.extend(variables.copy())

    # Si no han pasdo un modelo, lo iniciamos.
    if modelo is None:
        modelo = list()

    # Si no quedan más símbolos.
    if not simbolos:
        # Miramos si el modelo valida la base de conocimiento.
        asignaciones = dict(modelo)
        valores_premisas = [premisa.evaluar(**asignaciones)
                            for premisa
                            in base_conocimiento]
        todas_premisas = all(valor
                             for valor
                             in valores_premisas)

        # Si valida la base de conocimiento (premisas)
        if todas_premisas:
            # Devolvemos la evaluación de la conclusión con ese modelo.
            return demuestra.evaluar(**asignaciones)

        # Si no las valida, devolvemo verdadero.
        return True

    # Obtenemos el siguiente símbolo.
    simbolo = simbolos.pop()

    # Agregamos al modelo sus posibles valores.
    modelo_t = list(modelo)
    modelo_f = list(modelo)
    modelo_t.append((simbolo, True))
    modelo_f.append((simbolo, False))

    # Creamos tablas de verdad con cada valor.
    tabla_t = tabla_verdad(*premisas,
                           conclusion=conclusion,
                           variables=variables,
                           simbolos=simbolos.copy(),
                           modelo=modelo_t)
    tabla_f = tabla_verdad(*premisas,
                           conclusion=conclusion,
                           variables=variables,
                           simbolos=simbolos.copy(),
                           modelo=modelo_f)

    # Indicamos si ambos son ciertos.
    return tabla_t and tabla_f


# %% --- DEDUCCIÓN CON REGLAS DE INFERENCIA -----------------------------------

def deduccion(*premisas,
              conclusion,
              variables=None):
    """
    Realiza inferencia en lógica de proposiones.

    Mediante la aplicación de equivalencias y reglas de deducción.
    Se va a implementar como una búsqueda en grafo.

    Argumentos:
    - premisas: todos los argumentos, salvo el último, serán las premisas.
    - conclusion: el último argumento es la conclusión a ver si es válida.
    - variables: variables que se han usado en las premisas y la conclusión.

    Devuelve: nada.
    """
    # TODO Implementar el algoritmo de deducción de Lógica de Proposiciones.


# %% --- MAIN -----------------------------------------------------------------

if __name__ == '__main__':
    # Ejemplos de inferencia en lógica de proposiciones.

    # Poder medir los tiempos.
    from time import time

    print()
    print("-----------------")
    print("--- VARIABLES ---")
    print("-----------------")
    print()
    # Definimos las proposiciones
    P = Variable('P')
    Q = Variable('Q')
    R = Variable('R')
    S = Variable('S')
    VARIABLES = [variable.nombre for variable in [P, Q, R]]
    print("Variables: {0}".format(VARIABLES))
    print()

    # Definimos la base de conocimiento.
    PREMISAS = []
    PREMISAS.append(P >> Q)
    PREMISAS.append(Q >> R)
    PREMISAS.append(R >> S)

    # Definimos la conclusión a comprobar.
    PROBAR = P >> S

    # Indicamos qué inferencias vamos a lanzar.
    LANZA_TABLA_VERDAD = True

    # Realizamos la inferencia mediante tabla de verdad.
    if LANZA_TABLA_VERDAD:
        print()
        print("***********************")
        print("*** TABLA DE VERDAD ***")
        print("***********************")
        inicio = time()
        solucion = tabla_verdad(*PREMISAS,
                                conclusion=PROBAR)
        print("Conclusión: {0}".format(solucion))
        tiempo = time() - inicio
        MSG = "Tiempo: {0} milisegundos"
        print(MSG.format(tiempo*1000))
        print("--------------------")
