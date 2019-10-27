#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente racional de tipo tabla.
Devuelve una acción según la secuencia de percepciones que ha recibido hasta
el momento. Necesita de una tabla donde se defina todas las secuencias de
percepciones posibles y su acción correspondiente.
"""


# %% --- AGENTE TABLA ---

class AgenteTabla:
    """
    Clase que representa a un agente racional de tipo tabla.
    """

    def __init__(self,
                 acciones):
        """
        Crea una nueva instancia de la clase.
        Argumentos:
        - acciones: diccionario cuya clave será una secuencia de percepciones
                    separadas por comas y cuyo valor es la acción a realizar.
        """
        # Comprobaciones.
        if not acciones:
            raise "No se ha indicado la tabla de acciones"

        # Guardamos la tabla de secuencia de percepciones y acciones.
        self.acciones = acciones

        # Al inicio, no se habrá percibido aun nada.
        self.percepciones = ""

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
            self.percepciones += ","
        self.percepciones += percepcion

        # Buscamos la acción a realizar en la tabla según las percepciones
        # recibidas hasta el momento.
        if self.percepciones in self.acciones.keys():
            return self.acciones[self.percepciones]
        else:
            self.percepciones = ""
            return accion_basica


# %% --- MAIN ---

if __name__ == "__main__":
    """
    Ejemplos de agente tabla.
    """
    # Máquina expendedora simple.
    # Percepciones: moneda, a1, a2, a3.
    # Cualquier otra percepción reinicia la máquina.
    # La primera percepción debe ser: moneda
    # Hay que alternar la moneda con los códigos.
    # Puede servir hasta un máximo de 2 bebidas.
    acciones = {"moneda": "pedir-codigo",
                "moneda,a1": "servir-bebida1",
                "moneda,a2": "servir-bebida2",
                "moneda,a3": "servir-bebida3",
                "moneda,a1,moneda": "pedir-codigo",
                "moneda,a2,moneda": "pedir-codigo",
                "moneda,a3,moneda": "pedir-codigo",
                "moneda,a1,moneda,a1": "servir-bebida1",
                "moneda,a1,moneda,a2": "servir-bebida2",
                "moneda,a1,moneda,a3": "servir-bebida3",
                "moneda,a2,moneda,a1": "servir-bebida1",
                "moneda,a2,moneda,a2": "servir-bebida2",
                "moneda,a2,moneda,a3": "servir-bebida3",
                "moneda,a3,moneda,a1": "servir-bebida1",
                "moneda,a3,moneda,a2": "servir-bebida2",
                "moneda,a3,moneda,a3": "servir-bebida3"}

    # Máquina expendedora como agente tabla
    print("-- Agente Tabla: Máquina Expendedora -- ")
    expendedora = AgenteTabla(acciones=acciones)

    # Pedimos percepciones hasta que indique cadena vacía.
    percepcion = input("Indicar Percepcion:")
    while percepcion:
        # Obtenemos la acción a realizar.
        accion = expendedora.actuar(percepcion=percepcion
                                    accion_basica="esperar")

        # La mostramos
        print(accion)

        # Pedimos la siguiente percepción.
        percepcion = input("Indicar Percepcion:")
