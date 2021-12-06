#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agentes Racionales en la Inteligencia Artificial.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""


# %%
class AgenteTabla:
    """Agente racional de tipo tabla."""

    def __init__(self, acciones):
        self.acciones = acciones
        self.percepciones = ""

    def actuar(self, percepcion, accion_basica=""):
        """Actua según la percepción, devolviendo una acción."""
        if not percepcion:
            return accion_basica
        if len(self.percepciones) != 0:
            self.percepciones += ','
        self.percepciones += percepcion
        if self.percepciones in self.acciones.keys():
            return self.acciones[self.percepciones]
        self.percepciones = ""
        return accion_basica


# %%
class AgenteReactivoSimple:
    """Agente racional de tipo reactivo simple."""

    def __init__(self, reglas):
        self.reglas = reglas

    def actuar(self, percepcion, accion_basica=""):
        """Actua según la percepción, devolviendo una acción."""
        if not percepcion:
            return accion_basica
        if percepcion in self.reglas.keys():
            return self.reglas[percepcion]
        return accion_basica


# %%
class AgenteBasadoModelos:
    """Agente racional de tipo basado en modelos."""

    def __init__(self, modelo, reglas, estado_inicial="", accion_inicial=""):
        """Crea una nueva instancia de la clase."""
        self.modelo = modelo
        self.reglas = reglas
        self.estado_inicial = estado_inicial
        self.accion_inicial = accion_inicial
        self.accion = None
        self.estado = self.estado_inicial
        self.ult_accion = self.accion_inicial

    def actuar(self, percepcion):
        """Actua según la percepción, devolviendo una acción."""
        if not percepcion:
            return self.accion_inicial
        clave = (self.estado, self.ult_accion, percepcion)
        if clave not in self.modelo.keys():
            self.estado = self.estado_inicial
            self.accion = self.accion_inicial
            self.ult_accion = self.accion_inicial
            return self.accion_inicial
        self.estado = self.modelo[clave]
        if self.estado not in self.reglas.keys():
            self.estado = self.estado_inicial
            self.accion = self.accion_inicial
            self.ult_accion = self.accion_inicial
            return self.accion_inicial
        accion = self.reglas[self.estado]
        self.ult_accion = accion
        return accion


# %%
if __name__ == '__main__':
    LANZA_TABLA = True
    LANZA_SIMPLE = True
    LANZA_MODELOS = True

    if LANZA_TABLA:
        # Máquina expendedora simple.
        # Percepciones: moneda, a1, a2, a3.
        # Cualquier otra percepción reinicia la máquina.
        # La primera percepción debe ser: moneda
        # Hay que alternar la moneda con los códigos.
        # Puede servir hasta un máximo de 2 bebidas.
        ACCIONES = {'moneda': 'pedir-codigo',
                    'moneda,a1': 'servir-bebida1',
                    'moneda,a2': 'servir-bebida2',
                    'moneda,a3': 'servir-bebida3',
                    'moneda,a1,moneda': 'pedir-codigo',
                    'moneda,a2,moneda': 'pedir-codigo',
                    'moneda,a3,moneda': 'pedir-codigo',
                    'moneda,a1,moneda,a1': 'servir-bebida1',
                    'moneda,a1,moneda,a2': 'servir-bebida2',
                    'moneda,a1,moneda,a3': 'servir-bebida3',
                    'moneda,a2,moneda,a1': 'servir-bebida1',
                    'moneda,a2,moneda,a2': 'servir-bebida2',
                    'moneda,a2,moneda,a3': 'servir-bebida3',
                    'moneda,a3,moneda,a1': 'servir-bebida1',
                    'moneda,a3,moneda,a2': 'servir-bebida2',
                    'moneda,a3,moneda,a3': 'servir-bebida3'}
        print("-- Agente Tabla: Máquina Expendedora -- ")
        expendedora = AgenteTabla(ACCIONES)
        PERCEPCION = input("Indicar Percepcion:")
        while PERCEPCION:
            ACCION = expendedora.actuar(PERCEPCION, 'esperar')
            print(ACCION)
            PERCEPCION = input("Indicar Percepcion:")

    if LANZA_SIMPLE:
        # Conjunto de reglas de tipo 'si-entonces' para una máquina expendedora
        # excesivamente simple (no funcionará nada bien, ¡bebida gratis!)
        REGLAS = {'moneda': 'pedir-codigo',
                  'a1': 'servir-bebida1',
                  'a2': 'servir-bebida2',
                  'a3': 'servir-bebida3'}
        print("-- Agente Reactivo Simple: Máquina Expendedora -- ")
        expendedora = AgenteReactivoSimple(REGLAS)
        PERCEPCION = input("Indicar Percepcion:")
        while PERCEPCION:
            ACCION = expendedora.actuar(PERCEPCION, 'esperar')
            print(ACCION)
            PERCEPCION = input("Indicar Percepcion:")

    if LANZA_MODELOS:
        # Máquna expendedora simple (máquina de estados).
        # Los estados posibles son: sin-moneda, con-moneda, a1-servida,
        # a2-servida, a3-servida.
        # En cada estado, al ejecutar una acción, se llega a un nuevo estado.
        # Las aciones posibles son: pedir-moneda, pedir-codigo, reiniciar.
        # Las percepciones posibles son: moneda, a1, a2, a3, servida.
        MODELO = {('sin-moneda', 'pedir-moneda', 'moneda'): 'con-moneda',
                  ('con-moneda', 'pedir-codigo', 'a1'): 'a1-servida',
                  ('con-moneda', 'pedir-codigo', 'a2'): 'a2-servida',
                  ('con-moneda', 'pedir-codigo', 'a3'): 'a3-servida',
                  ('a1-servida', 'esperar', 'servida'): 'sin-moneda',
                  ('a2-servida', 'esperar', 'servida'): 'sin-moneda',
                  ('a3-servida', 'esperar', 'servida'): 'sin-moneda'}
        REGLAS = {'sin-moneda': 'pedir-moneda',
                  'con-moneda': 'pedir-codigo',
                  'a1-servida': 'esperar',
                  'a2-servida': 'esperar',
                  'a3-servida': 'esperar'}
        print("-- Agente Reactivo Basado en Modelos: Máquina Expendedora -- ")
        expendedora = AgenteBasadoModelos(MODELO, REGLAS, 'sin-moneda',
                                          'pedir-moneda')
        PERCEPCION = input("Indicar Percepcion:")
        while PERCEPCION:
            ACCION = expendedora.actuar(PERCEPCION)
            print(ACCION)
            PERCEPCION = input("Indicar Percepcion:")
