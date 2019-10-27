#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente racional de tipo reactivo simple.
Lo agente reactivos no tienen tienen objetivos y sólo actuan según es el
entorno en cada momento. El simple ni siquiera tiene en cuenta la secuencia
de percepciones, sólo la percepción actual. Su mayor utilidad es para
codificar los actos reflejos, es decir, aquellas acciones que hay que ejecutar
sin razonar ni pensar (ej. retirar la mano cuando te la quemas).
"""


# %% -- AGENTE REACTIVO SIMPLE --

class AgenteReactivoSimple:
    """
    Clase que representa a un agente racional de tipo reactivo simple.
    """

    def __init__(self,
                 reglas):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - reglas: relaciones entre las percepciones y las acciones a realizar.
        """
        # Comprobaciones.
        if not reglas:
            raise "No se han indicado las reglas"

        # Guardamos las reglas con los pares percepción-acción.
        self.reglas = reglas

    def actuar(self,
               percepcion,
               accion_basica=""):
        """
        Recibe una percepción y devuelve la acción a realizar según la
        secuencia de percepciones que ha recibido.
        Si la secuencia de percepciones no se encuentra en la tabla de
        acciones, reinicia la secuencia para empezar de nuevo.
        Argumentos:
        - percepcion: nombre de la percepción recibida.
        - accion_basica: acción a realizar si no se reconoce la percepción.
        Devuelve: nombre de la acción a realizar.
        """
        # Si no hay percepción, terminamos.
        if not percepcion:
            return accion_basica
        percepcion = percepcion.strip()
        if len(percepcion) == 0:
            return accion_basica

        # No se tiene en cuenta secuencia de percepciones,
        # sólo la percepción actual.
        if percepcion in self.reglas.keys():
            return self.reglas[percepcion]
        else:
            return accion_basica


# %% --- MAIN ---

if __name__ == "__main__":
    """
    Ejemplos de agente reactivo simple.
    """
    # Conjunto de reglas de tipo "si-entonces" para una máquina expendedora
    # excesivamente simple (no funcionará nada bien, ¡bebida gratis!)
    reglas = {"moneda": "pedir-codigo",
              "a1": "servir-bebida1",
              "a2": "servir-bebida2",
              "a3": "servir-bebida3"}

    # Máquina expendedora como agente reactivo simple.
    print("-- Agente Reactivo Simple: Máquina Expendedora -- ")
    expendedora = AgenteReactivoSimple(reglas=reglas)

    # Pedimos percepciones hasta que indique cadena vacía.
    percepcion = input("Indicar Percepcion:")
    while percepcion:
        # Obtenemos la acción a realizar.
        accion = expendedora.actuar(percepcion=percepcion,
                                    accion_basica="esperar")

        # La mostramos
        print(accion)

        # Pedimos la siguiente percepción.
        percepcion = input("Indicar Percepcion:")
