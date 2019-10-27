#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente racional de tipo reactivo basado en modelos.
Lo agente reactivos no tienen tienen objetivos y sólo actuan según es el
entorno en cada momento. El basado en modelos posee una memoria, por lo que
evitará fallos que tiene el reactivo simple. Se corresponde a una máquina de
estados al mantener un estado interno y modelo del mundo basado en la
secuencia de percepciones.
"""


# %% -- AGENTE BASADO EN MODELOS --

class AgenteBasadoModelos:
    """
    Clase que representa a un agente racional de tipo basado en modelos.
    """

    def __init__(self,
                 modelo,
                 reglas,
                 estado_inicial="",
                 accion_inicial=""):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - modelo: diccionario donde la clave es una tupla con un estado,
                  una acción y una percepción, y el valor es un nuevo estado.
        - reglas: relación entre cada estado y la acción a ejecutar en él.
        - estado_inicial: nombre del estado inicial.
        - accion_inicial: nombre de la accion inicial.
        """
        # Comprobaciones.
        if not modelo:
            raise "No se ha indicado un modelo"
        if not reglas:
            raise "No se ha indicado las reglas"

        # Guardamos los argumentos pasados.
        self.modelo = modelo
        self.reglas = reglas
        self.estado_inicial = estado_inicial or ""
        self.accion_inicial = accion_inicial or ""

        # Nos situamos en el estado inicial.
        self.estado = self.estado_inicial

        # Establememos la última acción como la inicial.
        self.ult_accion = self.accion_inicial

    def actuar(self,
               percepcion):
        """
        Recibe una percepción y devuelve la acción a realizar según la
        secuencia de percepciones que ha recibido.
        Si la secuencia de percepciones no se encuentra en la tabla de
        acciones, reinicia la secuencia para empezar de nuevo.
        Argumentos:
        - percepcion: nombre de la percepción recibida.
        Devuelve: nombre de la acción a realizar.
        """
        # Si no hay percepción, terminamos.
        if not percepcion:
            return self.accion_inicial
        percepcion = percepcion.strip()
        if len(percepcion) == 0:
            return self.accion_inicial

        # Obtenemos el nuevo estado según el modelo.
        clave = (self.estado,
                 self.ult_accion,
                 percepcion)
        if clave not in self.modelo.keys():
            self.estado = self.estado_inicial
            self.accion = self.accion_inicial
            return self.accion_inicial
        self.estado = self.modelo[clave]

        # Obtenemos la acción a realizar según el nuevo estado y las reglas.
        if self.estado not in self.reglas.keys():
            self.estado = self.estado_inicial
            self.accion = self.accion_inicial
            return self.accion_inicial
        accion = self.reglas[self.estado]

        # La guardamos como última acción.
        self.ult_accion = accion

        # Devolvemos la acción.
        return accion


# %% --- MAIN ---

if __name__ == "__main__":
    """
    Ejemplo de agente reflexivo basado en modelos.
    """
    # Máquna expendedora simple (máquina de estados).
    # Los estados posibles son: sin-moneda, con-moneda, a1-servida,
    # a2-servida, a3-servida.
    # En cada estado, al ejecutar una acción, se llega a un nuevo estado.
    # Las aciones posibles son: pedir-moneda, pedir-codigo, reiniciar.
    # Las percepciones posibles son: moneda, a1, a2, a3, servida.
    modelo = {("sin-moneda", "pedir-moneda", "moneda"): "con-moneda",
              ("con-moneda", "pedir-codigo", "a1"): "a1-servida",
              ("con-moneda", "pedir-codigo", "a2"): "a2-servida",
              ("con-moneda", "pedir-codigo", "a3"): "a3-servida",
              ("a1-servida", "esperar", "servida"): "sin-moneda",
              ("a2-servida", "esperar", "servida"): "sin-moneda",
              ("a3-servida", "esperar", "servida"): "sin-moneda"}

    # En cada estado hay una nueva acción a ejecutar.
    reglas = {"sin-moneda": "pedir-moneda",
              "con-moneda": "pedir-codigo",
              "a1-servida": "esperar",
              "a2-servida": "esperar",
              "a3-servida": "esperar"}

    # Máquina expendedora como agente reactivo basado en modelos.
    print("-- Agente Reactivo Basado en Modelos: Máquina Expendedora -- ")
    expendedora = AgenteBasadoModelos(modelo=modelo,
                                      reglas=reglas,
                                      estado_inicial="sin-moneda",
                                      accion_inicial="pedir-moneda")

    # Pedimos percepciones hasta que indique cadena vacía.
    percepcion = input("Indicar Percepcion:")
    while percepcion:
        # Obtenemos la acción a realizar.
        accion = expendedora.actuar(percepcion=percepcion)

        # La mostramos
        print(accion)

        # Pedimos la siguiente percepción.
        percepcion = input("Indicar Percepcion:")
