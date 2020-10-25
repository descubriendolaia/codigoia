#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agentes Racionales en la Inteligencia Artificial.

Existen varios tipos de agentes racionales:

- Agente Tabla: el ídeal, si se pudiera emplementar. Consta de una tabla con
una correspondencia completa entre todas las percepciones posibles y la acción
a realizar en cada caso.

- Agentes Reactivos: actúan sólo según sus percepciones, sin considerar las
consecuencias de sus actos. No tienen objetivos y sólo actúan según es el
entorno en cada momento.

    - Agente Reactivo Simple: sólo actúa según la percepción actual, sin tener
    en cuenta percepciones anteriores (no hay memoria). Su mayor utilidad es
    para codificar los actos reflejos, es decir, aquellas acciones que hay que
    ejecutar sin razonar ni pensar (ej. retirar la mano cuando te la quemas).

    - Agente Basado en Modelo: posee una memoria, por lo que evitará algunos
    fallos que tiene el reactivo simple. Se corresponde a una máquina de
    estados al mantener un estado interno y modelo del mundo basado en la
    secuencia de percepciones. Sigue siendo demasiado simple y tiene fallos.

- Agentes que Planifican: tienen en cuenta las consecuencias de sus actos, ya
que realizan simulaciones, teniendo en cuenta cómo podría ser el entorno
después de realizar sus acciones.

    - Agente Basado en Objetivos: actúa para alcanzar un objetivo. Posee un
    modelo del mundo y mantiene un estado interno de donde está dentro de
    ese mundo. También conoce cómo cambia el mundo cuando realiza una acción.

    - Agente Basado en Utilidad: si existen varias formas de alcanzar el
    objetivo, tiene en cuenta la que le podría aportar mayor utilidad. Ya no
    es sólo alcanzar el objetivo sea como sea, sino de la mejor forma posible.

- Agente que Aprende: ampliación de cualquiera de los agentes anteriores, en
el que se añaden mecanismos para que el agente pueda ampliar su base de
conocimiento con nueva información. Puede aprender tanto a partir de la
secuencia de percepciones como de las consecuencias de sus acciones.

En este módulo se han implementado el agente tabla y los agentes reactivos.
En cuanto a agentes que planifican y que aprenden, tenemos toda la serie de
algoritmos que se verán durante el resto de curso.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""


# %% --- AGENTE TABLA ---------------------------------------------------------

class AgenteTabla:
    """Agente racional de tipo tabla."""

    def __init__(self,
                 acciones):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - acciones: diccionario cuya clave será una secuencia de percepciones
                    separadas por comas y cuyo valor es la acción a realizar.

        Devuelve: nada.
        """
        # Comprobaciones.
        if not acciones:
            raise ValueError("No se ha indicado la tabla de acciones")

        # Guardamos la tabla de secuencia de percepciones y acciones.
        self.acciones = acciones

        # Al inicio, no se habrá percibido aun nada.
        self.percepciones = ""

    def actuar(self,
               percepcion,
               accion_basica=""):
        """
        Actua según la percepción, devolviendo una acción.

        Recibe una percepción y devuelve la acción a realizar según la
        secuencia de percepciones que ha recibido.

        Si la secuencia de percepciones no se encuentra en la tabla de
        acciones, reinicia la secuencia para empezar de nuevo.

        Argumentos:
        - percepcion: nombre de la percepción recibida.
        - accion_basica: la acción a realizar si no se encuentra la secuencia
                         de percepciones en la tabla de acciones.

        Devuelve: nombre de la acción a realizar.
        """
        # Si no hay percepción, terminamos.
        if not percepcion:
            return accion_basica
        percepcion = percepcion.strip()
        if len(percepcion) == 0:
            return accion_basica

        # Agregamos la percepción a la lista de percepciones.
        if len(self.percepciones) != 0:
            self.percepciones += ','
        self.percepciones += percepcion

        # Buscamos la acción a realizar en la tabla según las percepciones
        # recibidas hasta el momento.
        if self.percepciones in self.acciones.keys():
            return self.acciones[self.percepciones]
        self.percepciones = ""
        return accion_basica


# %% -- AGENTE REACTIVO SIMPLE ------------------------------------------------

class AgenteReactivoSimple:
    """Agente racional de tipo reactivo simple."""

    def __init__(self,
                 reglas):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - reglas: relaciones entre las percepciones y las acciones a realizar.

        Devuelve: nada.
        """
        # Comprobaciones.
        if not reglas:
            raise ValueError("No se han indicado las reglas")

        # Guardamos las reglas con los pares percepción-acción.
        self.reglas = reglas

    def actuar(self,
               percepcion,
               accion_basica=""):
        """
        Actua según la percepción, devolviendo una acción.

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
        return accion_basica


# %% -- AGENTE BASADO EN MODELOS ----------------------------------------------

class AgenteBasadoModelos:
    """Agente racional de tipo basado en modelos."""

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

        Devuelve: nada.
        """
        # Comprobaciones.
        if not modelo:
            raise ValueError("No se ha indicado un modelo")
        if not reglas:
            raise ValueError("No se ha indicado las reglas")

        # Guardamos los argumentos pasados.
        self.modelo = modelo
        self.reglas = reglas
        self.estado_inicial = estado_inicial or ""
        self.accion_inicial = accion_inicial or ""
        self.accion = None

        # Nos situamos en el estado inicial.
        self.estado = self.estado_inicial

        # Establememos la última acción como la inicial.
        self.ult_accion = self.accion_inicial

    def actuar(self,
               percepcion):
        """
        Actua según la percepción, devolviendo una acción.

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
            self.ult_accion = self.accion_inicial
            return self.accion_inicial
        self.estado = self.modelo[clave]

        # Obtenemos la acción a realizar según el nuevo estado y las reglas.
        if self.estado not in self.reglas.keys():
            self.estado = self.estado_inicial
            self.accion = self.accion_inicial
            self.ult_accion = self.accion_inicial
            return self.accion_inicial
        accion = self.reglas[self.estado]

        # La guardamos como última acción.
        self.ult_accion = accion

        # Devolvemos la acción.
        return accion


# %% --- MAIN -----------------------------------------------------------------

if __name__ == '__main__':
    # Ejemplos de agentes tabla y reactivos.

    # Indicamos los algoritmos que queremos lanzar.
    LANZA_TABLA = True
    LANZA_SIMPLE = True
    LANZA_MODELOS = True

    # ------------------------------------------------------------------------
    # AGENTE TABLA
    # ------------------------------------------------------------------------

    # Si se pide lanzar el agente tabla
    if LANZA_TABLA:
        print()
        print("************************")
        print("***** AGENTE TABLA *****")
        print("************************")

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

        # Máquina expendedora como agente tabla
        print("-- Agente Tabla: Máquina Expendedora -- ")
        expendedora = AgenteTabla(acciones=ACCIONES)

        # Pedimos percepciones hasta que indique cadena vacía.
        PERCEPCION = input("Indicar Percepcion:")
        while PERCEPCION:
            # Obtenemos la acción a realizar.
            ACCION = expendedora.actuar(percepcion=PERCEPCION,
                                        accion_basica='esperar')

            # La mostramos
            print(ACCION)

            # Pedimos la siguiente percepción.
            PERCEPCION = input("Indicar Percepcion:")

    # ------------------------------------------------------------------------
    # AGENTE REACTIVO SIMPLE
    # ------------------------------------------------------------------------

    # Si se pide lanzar el agente reactivo simple
    if LANZA_SIMPLE:
        print()
        print("**********************************")
        print("***** AGENTE REACTIVO SIMPLE *****")
        print("**********************************")

        # Conjunto de reglas de tipo 'si-entonces' para una máquina expendedora
        # excesivamente simple (no funcionará nada bien, ¡bebida gratis!)
        REGLAS = {'moneda': 'pedir-codigo',
                  'a1': 'servir-bebida1',
                  'a2': 'servir-bebida2',
                  'a3': 'servir-bebida3'}

        # Máquina expendedora como agente reactivo simple.
        print("-- Agente Reactivo Simple: Máquina Expendedora -- ")
        expendedora = AgenteReactivoSimple(reglas=REGLAS)

        # Pedimos percepciones hasta que indique cadena vacía.
        PERCEPCION = input("Indicar Percepcion:")
        while PERCEPCION:
            # Obtenemos la acción a realizar.
            ACCION = expendedora.actuar(percepcion=PERCEPCION,
                                        accion_basica='esperar')

            # La mostramos
            print(ACCION)

            # Pedimos la siguiente percepción.
            PERCEPCION = input("Indicar Percepcion:")

    # ------------------------------------------------------------------------
    # AGENTE REACTIVO BASADO EN MODELOS
    # ------------------------------------------------------------------------

    # Si se pide lanzar el agente reactivo basado en modelos
    if LANZA_MODELOS:
        print()
        print("*********************************************")
        print("***** AGENTE REACTIVO BASADO EN MODELOS *****")
        print("*********************************************")

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

        # En cada estado hay una nueva acción a ejecutar.
        REGLAS = {'sin-moneda': 'pedir-moneda',
                  'con-moneda': 'pedir-codigo',
                  'a1-servida': 'esperar',
                  'a2-servida': 'esperar',
                  'a3-servida': 'esperar'}

        # Máquina expendedora como agente reactivo basado en modelos.
        print("-- Agente Reactivo Basado en Modelos: Máquina Expendedora -- ")
        expendedora = AgenteBasadoModelos(modelo=MODELO,
                                          reglas=REGLAS,
                                          estado_inicial='sin-moneda',
                                          accion_inicial='pedir-moneda')

        # Pedimos percepciones hasta que indique cadena vacía.
        PERCEPCION = input("Indicar Percepcion:")
        while PERCEPCION:
            # Obtenemos la acción a realizar.
            ACCION = expendedora.actuar(percepcion=PERCEPCION)

            # La mostramos
            print(ACCION)

            # Pedimos la siguiente percepción.
            PERCEPCION = input("Indicar Percepcion:")
