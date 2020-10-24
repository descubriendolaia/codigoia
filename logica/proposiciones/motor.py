#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Lógica de Proposiciones.

Clases que representan objetos de la lógica de proposiciones, la más simple
que existe. Esto nos permitirá automatizar la creación de tablas de verdad.

SINTAXIS:
    - Letras Proposicionales (Variables): P, Q, R, S, T, ...
    - Constantes Lógicas: True, False
    - Símbolos Lógicos:
        - Negación (NOT): ~
        - Conjunción (AND): &
        - Disyunción (OR): |
        - Implicación (si-entonces): >>, <<
        - Equivalencia (si-y-solo-si): ==
    - Símbolos auxiliares (precedencia):
        - Paréntesis: (, )
        - Corchetes: [, ]

DEFINICIONES:
    - Proposición: una constante lógica o una letra proposicional. También se
                   le llama 'literal' o 'fórmula atómica'.
    - Sentencia (Fórmula Compuesta):
        - Una proposición.
        - La negación de una sentencia.
        - La conjunción, disyunción, condicional o bicondicional de dos o más
          sentencias.
    - Implicación: sentencia condicial de tipo "si-entonces" (>>, <<).

NOTACIÓN BNF:
    sentencia → sentencia-atómica | sentencia-compleja
    sentencia-atómica → True | False | P | Q | R | S | ...
    sentencia-compleja → ( sentencia ) | [ sentencia ]
        | ~ sentencia
        | sentencia & sentencia
        | sentencia | sentencia
        | sentencia >> sentencia
        | sentencia << sentencia
        | sentencia iif sentencia
    PRECEDENCIA:  not, and, or, >>, <<, ==
"""


# %% --- FUNCIONES AUXILIARES -------------------------------------------------

def _crea_proposicion(valor):
    """
    Devuelve un tipo de proposición acorde al valor pasado.

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


def _crea_filas_tabla_verdad(variables):
    """
    Devuelve una lista de diccionarios.

    Cada diccionario tiene como claves cada una de las variables y como valor
    un booleano. La lista abarcará todas las combinaciones posibles de valores
    boolenas de cada variable.

    Argumentos:
    - variables: lista de variables con las que crear las filas.

    Devuelve: lista con todas las combinaciones boolenas de las variables.
    """
    # Comprobaciones.
    if len(variables) == 0:
        return [dict()]

    # Creamos una lista con las variables pasadas.
    variables = list(variables)

    # Cogemos la primera variable por un lado y el resto por otro.
    vars_p = variables[0]
    vars_r = _crea_filas_tabla_verdad(variables[1:])

    # Función auxiliar para combinar los valores.
    def _combina(vars_p, valor, vars_r):
        # Lista de valores a devolver.
        valores = []

        # Del resto de variables.
        for var_r in vars_r:
            # Metemos el valor de la primera variable en una lista.
            valores_p = [(vars_p, valor)]

            # Obtenemos cada uno de sus valores restantes.
            valores_r = list(var_r.items())

            # Los combinamos con el de la primera variable.
            valores_p.extend(valores_r)

            # Lo agregamos a la lista.
            valores.append(dict(valores_p))

        # Devolvemos un diccionario con los valores obtenidos.
        return valores

    # Obtenemos los valores, los combinamos y los devolvemos.
    valor_t = _combina(vars_p, True, vars_r)
    valor_f = _combina(vars_p, False, vars_r)
    return valor_t + valor_f


# %% --- PROPOSICIÓN ----------------------------------------------------------

class Proposicion:
    """Proposición en lógica de proposiciones."""

    def __init__(self, *hijas):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - hijas: lista de variables a crear como proposiciones hijas.

        Devuelve: nada.
        """
        # Símbolo que representa la proposición.
        self.simbolo = ""

        # Representa el valor de verdad de una proposición vacía.
        self.vacia = ""

        # Proposiciones hijas de la actual.
        self.hijas = [_crea_proposicion(hija)
                      for hija in hijas]

    def __str__(self):
        """
        Representación en modo texto de la proposición.

        Devuelve: información sobre proposiciones hijas.
        """
        # Si no hay proposiciones hijas, terminamos.
        if len(self.hijas) == 0:
            return self.vacia

        # Mostramos todas las proposiciones hijas.
        return self.simbolo.join(hija.str_hijas()
                                 for hija in self.hijas)

    def str_hijas(self):
        """
        Representación en modo texto de las proposiciones hijas.

        Devuelve: información sobre proposiciones hijas.
        """
        # Mostramos la información más relevante.
        msg = "{0}"
        if isinstance(self, (Constante, Variable, Not)):
            msg = "({0})"
        return msg.format(self)

    def __repr__(self):
        """
        Representación de la proposición para depuración.

        Devuelve: texto para depuración.
        """
        # Mostramos la información más relevante.
        return "Proposicion({0})".format(self)

    def variables(self):
        """
        Obtiene la lista de variables de la proposición y las devuelve.

        Devuelve: lista de variables.
        """
        # Si no hay proposiciones hijas, terminamos.
        if len(self.hijas) == 0:
            return frozenset()

        # Devolvemos un conjunto con todas las variables que haya en las
        # proposiciones hijas (se usa un conjunto para no repetirlas).
        return frozenset.union(*[hija.variables()
                                 for hija in self.hijas])

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Se implementará en cada una de las clases que heredan de esta.
        raise NotImplementedError("Hay que implementar este método")

    def ver_tabla_verdad(self,
                         maximo=5):
        """
        Muestra la tabla de verdad de la proposición.

        Muestra todas la combinaciones posibles de los valores de sus
        variables.

        Argumentos:
        - maximo: nº máximo de variables a mostrar.

        Devuelve: nada.
        """
        # Ordenamos las variables.
        variables = sorted(self.variables())

        # Creamos la tabla de verdad con las variables.
        filas = _crea_filas_tabla_verdad(variables)

        # Definimos una cabecera (como máximo 5 variables).
        literales = str(self)
        num_literales = max(maximo, len(literales))
        columnas = "  ".join("{0: ^5}".format(variable)
                             for variable in variables)
        cabecera = "{0}  |  {1: ^{2}}".format(columnas,
                                              literales,
                                              num_literales)

        # Mostramos la cabecera y un separador.
        print(cabecera)
        print("=" * len(cabecera))

        # Por cada una de las filas.
        for fila in filas:
            # Formateamos los valores de las variables.
            valores = "  ".join("{0: ^{1}}".format(str(fila[variable]),
                                                   max(maximo,
                                                       len(variable)))
                                for variable in variables)

            # Calculamos el valor de verdad.
            resultado = "{0: ^{1}}".format(str(self.evaluar(**fila)),
                                           num_literales)

            # Lo mostramos.
            print("{0}  |  {1}".format(valores, resultado))

        # Forzamos un salto de línea al final.
        print()

    def __and__(self, otra):
        """
        Sobrecarga de operador lógico conjunción (por la izquierda).

        Argumentos:
        - otra: la otra proposición (parte derecha) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Cogemos las conjunciones hijas de la actual.
        unas = self.hijas if isinstance(self, And) else [self]

        # Cogemos las conjunciones hijas de la otra.
        otras = otra.hijas if isinstance(otra, And) else [otra]

        # Creamos una proposición de tipo conjunción con ellas.
        return And(*(unas + otras))

    def __rand__(self, otra):
        """
        Sobrecarga de operador lógico conjunción (por la derecha).

        Argumentos:
        - otra: la otra proposición (parte izquierda) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Le damos la vuelta a la operación.
        return _crea_proposicion(otra) & self

    def __or__(self, otra):
        """
        Sobrecarga de operador lógico diyunción (por la izquierda).

        Argumentos:
        - otra: la otra proposición (parte derecha) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Cogemos las disyunciones hijas de la actual.
        unas = self.hijas if isinstance(self, Or) else [self]

        # Cogemos las disyunciones hijas de la otra.
        otras = otra.hijas if isinstance(otra, Or) else [otra]

        # Creamos una proposición de tipo disyunción con ellas.
        return Or(*(unas + otras))

    def __ror__(self, otra):
        """
        Sobrecarga de operador lógico disyunción (por la derecha).

        Argumentos:
        - otra: la otra proposición (parte derecha) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Le damos la vuelta a la operación.
        return _crea_proposicion(otra) | self

    def __invert__(self):
        """
        Sobrecarga del operador lógico de negación.

        Devuelve: una proposición que represente la operación.
        """
        # Creamos una proposición de tipo negación.
        return Not(self)

    def __rshift__(self, otra):
        """
        Sobrecarga del operador lógico de deplazamiento hacia la derecha.

        Va a equivaler a una implicación hacia la izquierda (parte izquierda).

        Argumentos:
        - otra: la otra proposición (parte derecha) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Creamos una proposición de tipo implicación.
        return Implica(self, otra)

    def __rrshift__(self, otra):
        """
        Sobrecarga del operador lógico de deplazamiento hacia la derecha.

        Va a equivaler a una implicación hacia la izquierda (parte derecha).

        Argumentos:
        - otra: la otra proposición (parte izquierda) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Creamos una proposición de tipo implicación.
        return Implica(otra, self)

    def __lshift__(self, otra):
        """
        Sobrecarga del operador lógico de deplazamiento hacia la izquierda.

        Va a equivaler a una implicación hacia la derecha (parte izquierda).

        Argumentos:
        - otra: la otra proposición (parte derecha) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Creamos una proposición de tipo implicación.
        return ImplicadoPor(self, otra)

    def __rlshift__(self, otra):
        """
        Sobrecarga del operador lógico de deplazamiento hacia la izquierda.

        Va a equivaler a una implicación hacia la derecha (parte derecha).

        Argumentos:
        - otra: la otra proposición (parte izquierda) con la que operar.

        Devuelve: una proposición que represente la operación.
        """
        # Creamos una proposición de tipo implicación.
        return ImplicadoPor(otra, self)

    def __eq__(self, otra):
        """
        Sobrecarga del operador igualdad.

        Va a simbolizar una equivalencia lógica
        (doble implicación, 'sí y sólo sí').

        Argumentos:
        - otra: la otra proposición con la que operar.
        Devuelve: una proposición que represente la operación.
        """
        # Indicamos si ambas proposiciones son equivalentes.
        return self.es_equivalente(otra)

    def conjuncion(self, otra):
        """
        Realiza una conjunción entre la proposición actual y otra.

        Argumentos:
        - otra: la otra proposición con la que operar.

        Devuelve: resultado de hacer la operación.
        """
        # Realizamos la operación.
        return self & otra

    def disyuncion(self, otra):
        """
        Realiza una disyunción entre la proposición actual y otra.

        Argumentos:
        - otra: la otra proposición con la que operar.

        Devuelve: resultado de hacer la operación.
        """
        # Realizamos la operación.
        return self | otra

    def negacion(self):
        """
        Realiza una negación de la proposición actual.

        Devuelve: resultado de hacer la operación.
        """
        # Realizamos la operación.
        return ~self

    def implica(self, otra):
        """
        Realiza una implicación entre la proposición actual y otra.

        Argumentos:
        - otra: la otra proposición con la que operar.

        Devuelve: resultado de hacer la operación.
        """
        # Realizamos la operación.
        return self >> otra

    def implicado_por(self, otra):
        """
        Realiza una implicación inversa entre la proposición actual y otra.

        Argumentos:
        - otra: la otra proposición con la que operar.

        Devuelve: resultado de hacer la operación.
        """
        # Realizamos la operación.
        return self << otra

    def equivale(self, otra):
        """
        Realiza una equivalencia entre la proposición actual y otra.

        Argumentos:
        - otra: la otra proposición con la que operar.

        Devuelve: resultado de hacer la operación.
        """
        # Creamos una proposición de tipo negación.
        return Equivale(self, otra)

    def es_tautologia(self):
        """
        Indica si la proposición es una tautología.

        Devuelve: True si es tautología, False si no lo es.
        """
        # Obtenemos la tabla de verdad.
        tabla = _crea_filas_tabla_verdad(self.variables())

        # Indicamos si todos los resultados son True.
        return all(self.evaluar(**fila)
                   for fila in tabla)

    def es_contradiccion(self):
        """
        Indica si la proposición es una contradicción.

        Devuelve: True si es contradicción, False si no lo es.
        """
        # Obtenemos la tabla de verdad.
        tabla = _crea_filas_tabla_verdad(self.variables())

        # Indicamos si todos los resultados son False.
        return all(not self.evaluar(**fila)
                   for fila in tabla)

    def es_contingente(self):
        """
        Indica si no es tautología ni contradicción.

        Es dedir, si algunas combinaciones de valores dan True
        y otras dan False.

        Devuelve: True si es contingente, False si no lo es.
        """
        # No debe ser ni tautología ni contradicción.
        return (not self.es_tautologia() and
                not self.es_contradiccion())

    def es_equivalente(self, otra):
        """
        Indica si la proposición dada es equivalente a otra.

        Argumentos:
        - otra: la otra proposición con la que operar.

        Devuelve: True si es equivalente, False si no lo es.
        """
        # Creamos la proposición de la otra.
        otra = _crea_proposicion(otra)

        # Obtenemos la tabla de verdad de todas las variables.
        todas = self.variables() | otra.variables()
        tabla = _crea_filas_tabla_verdad(todas)

        # Indicamos si el resultado de ambas es igual.
        return all(self.evaluar(**fila) == otra.evaluar(**fila)
                   for fila in tabla)

    def es_identica(self, otra):
        """
        Indica si la proposición es identica (misma expresión) a otra.

        Argumentos:
        - otra: proposción a ver si es idéntica a la actual.

        Devuelve: si la proposición indicada es exactemente la misma a esta.
        """
        # Deben ser de la misma clase y con todo igual definido.
        return (self.__class__ == otra.__class__ and
                len(self.hijas) == len(otra.hijas) and
                all(una.es_identica(otra)
                    for (una, otra) in zip(self.hijas, otra.hijas)))

    def sustituye(self, una, otra):
        """
        Realiza una sustitución dentro de la proposición.

        Argumentos:
        - una: parte a sustituir.
        - otra: parte con la que sustituir a la una.

        Devuelve: proposición con la sustitución hecha.
        """
        # Si la proposición actual es igual a la una, devolvemos la otra.
        if self.es_identica(una):
            return otra

        # Realizamos la sustitución en las proposiciones hijas.
        return self.__class__(*[hija.sustituye(una, otra)
                                for hija in self.hijas])


# %% --- CONSTANTE ------------------------------------------------------------

class Constante(Proposicion):
    """
    Clase que representa a una constante lógica (valor de la tabla de verdad).

    Hereda de Proposición, ya que las constantes lógicas son proposiciones.
    """

    def __init__(self, valor):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - valor: valor de la constante lógica (True o False).

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__()

        # No tendrá proposiciones hijas.
        self.hijas = []

        # Guardamos el valor pasado.
        self.valor = bool(valor)

    def __str__(self):
        """
        Representación en modo texto de la constante.

        Devuelve: valor de la constante.
        """
        # Pasamos el booleano a cadena de texto.
        return str(self.valor)

    def variables(self):
        """
        Obtiene la lista de variables de la proposición y las devuelve.

        Devuelve: lista de variables.
        """
        # No hay variables.
        return frozenset()

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # No hay nada que evaluar, tan sólo devolver el valor.
        return self.valor

    def es_identica(self, otra):
        """
        Indica si la proposición es identica (misma expresión) a otra.

        Argumentos:
        - otra: proposción a ver si es idéntica a la actual.

        Devuelve: si la proposición indicada es exactemente la misma a esta.
        """
        # Debe ser una constante y tener el mismo valor.
        return (isinstance(otra, Constante) and
                self.valor == otra.valor)

    def sustituye(self, una, otra):
        """
        Realiza una sustitución dentre de la proposición.

        Argumentos:
        - una: parte a sustituir.
        - otra: parte con la que sustituir a la una.

        Devuelve: proposición con la sustitución hecha.
        """
        # No se puede realizar sustituciones en constantes.
        return Constante(self.valor)


# %% --- VARIABLE -------------------------------------------------------------

class Variable(Proposicion):
    """
    Clase que representa a una variable lógica.

    Hereda de Proposición, ya que las variables lógicas son proposiciones.
    """

    def __init__(self, nombre):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - valor: letra proposicional que identifica a la variable.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__()

        # No tendrá proposiciones hijas.
        self.hijas = []

        # Guardamos el nombre pasado (letra proposicional).
        self.nombre = str(nombre)

    def __str__(self):
        """
        Representación en modo texto de la variable.

        Devuelve: nombre de la variable.
        """
        # Devolvemos el nombre de la variable.
        return str(self.nombre)

    def variables(self):
        """
        Obtiene la lista de variables de la proposición y las devuelve.

        Devuelve: lista de variables.
        """
        # Sólo habrá una variable, ella misma.
        return frozenset({self.nombre})

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Devolvemos el valor de esa variable.
        return asignaciones[self.nombre]

    def es_identica(self, otra):
        """
        Indica si la proposición es identica (misma expresión) a otra.

        Argumentos:
        - otra: proposción a ver si es idéntica a la actual.

        Devuelve: si la proposición indicada es exactemente la misma a esta.
        """
        # Debe ser una variable y tener el mismo nombre.
        return (isinstance(otra, Variable) and
                self.nombre == otra.nombre)

    def sustituye(self, una, otra):
        """
        Realiza una sustitución dentre de la proposición.

        Argumentos:
        - una: parte a sustituir.
        - otra: parte con la que sustituir a la una.

        Devuelve: proposición con la sustitución hecha.
        """
        # Si la variable actual es igual a la una, devolvemos la otra.
        if self.es_identica(una):
            return otra

        # Devolvemos la variable ya que no se podrá sustituir.
        return Variable(self.nombre)


# %% --- OPERADORES LÓGICOS ---------------------------------------------------

class Not(Proposicion):
    """Representa a una proposición de tipo negación lógica."""

    def __init__(self, hija):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - hija: proposición a negar.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__(hija)

    def __str__(self):
        """
        Representación en modo texto de la negación.

        Devuelve: negación de la proposición hija.
        """
        # Le ponemos el símbolo de negación delante.
        return "¬{0}".format(self.hijas[0].str_hijas())

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Devolveremos la negación de la evaluación de su proposición interna.
        return not self.hijas[0].evaluar(**asignaciones)


class And(Proposicion):
    """Representa a una proposición de tipo conjunción lógica."""

    def __init__(self, *hijas):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - hijas: lista de proposiciones que componen la conjunción.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__(*hijas)

        # Definimos el símbolo de la conjunción lógica.
        self.simbolo = " ^ "

        # La proposición vacía tendrá un valor de verdad de True.
        self.vacia = "True"

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Será verdad si todos las proposiciones hijas son verdad.
        return all(hija.evaluar(**asignaciones)
                   for hija in self.hijas)


class Or(Proposicion):
    """Representa a una proposición de tipo disyunción lógica."""

    def __init__(self, *hijas):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - hijas: lista de proposiciones que componen la disyunción.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__(*hijas)

        # Definimos el símbolo de la disyunción lógica.
        self.simbolo = " v "

        # La proposición vacía tendrá un valor de verdad de False.
        self.vacia = "False"

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Será verdad si todos las proposiciones hijas son verdad.
        return any(hija.evaluar(**asignaciones)
                   for hija in self.hijas)


class Implica(Proposicion):
    """Representa a una proposición de tipo implicación lógica."""

    def __init__(self, premisa, conclusion):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - premisa: parte izquierda de la implicación.
        - conclusión: parte derecha de la implicación.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__(premisa, conclusion)

        # Definimos el símbolo de la implicación lógica.
        self.simbolo = " => "

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Si la premisa es cierta.
        if self.hijas[0].evaluar(**asignaciones):
            # Devolvemos la evaluaciión de la conclusión.
            return self.hijas[1].evaluar(**asignaciones)

        # Si la premisa no es cierta, siempre será True.
        return True


class ImplicadoPor(Proposicion):
    """Representa a una proposición de tipo implicación lógica."""

    def __init__(self, conclusion, premisa):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - conclusión: parte derecha de la implicación.
        - premisa: parte izquierda de la implicación.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__(conclusion, premisa)

        # Definimos el símbolo de la implicación lógica.
        self.simbolo = " <= "

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Si la premisa es cierta.
        if self.hijas[1].evaluar(**asignaciones):
            # Devolvemos la evaluaciión de la conclusión.
            return self.hijas[0].evaluar(**asignaciones)

        # Si la premisa no es cierta, siempre será True.
        return True


class Equivale(Proposicion):
    """Representa a una proposición de tipo equivalencia lógica."""

    def __init__(self, izquierda, derecha):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - izquierda: parte izquierda de la equivalencia.
        - derecha: parte derecha de la equivalencia.

        Devuelve: nada.
        """
        # Invocamos al constructor de la clase base.
        super().__init__(izquierda, derecha)

        # Definimos el símbolo de la implicación lógica.
        self.simbolo = " <=> "

    def evaluar(self, **asignaciones):
        """
        Devolverá el valor de verdad de la proposición.

        Argumentos:
        - asignaciones: diccionario con los valores asignados a cada literal.

        Devuelve: valor de verdad (booleano) de la proposición.
        """
        # Las evaluaciones de ambas partes deben ser iguales.
        return (self.hijas[0].evaluar(**asignaciones) ==
                self.hijas[1].evaluar(**asignaciones))


# %% --- RAZONAMIENTO ---------------------------------------------------------

class Razonamiento:
    """
    Razonamiento en lógica de proposiciones.

    Permite saber si dicho razonamiento es válido o no.
    """

    def __init__(self, *premisas, conclusion):
        """
        Crea una nueva instancia de la clase.

        Argumentos:
        - premisas: todos los argumentos, salvo el último, serán las premisas.
        - conclusion: el último argumento es la conclusión a ver si es válida.

        Devuelve: nada.
        """
        # Guardamos las premisas y la conclusión como proposiciones.
        self.premisas = [_crea_proposicion(premisa)
                         for premisa in premisas]
        self.conclusion = _crea_proposicion(conclusion)

    def __str__(self):
        """
        Representación en modo texto de la proposición.

        Devuelve: texto con premisas y conclusión.
        """
        # Mostramos las premisas y la conclusión.
        valores = [str(premisa) for premisa in self.premisas]
        inicio = ", ".join(valores) if self.premisas else ""
        fin = ", Conclusion = {0}".format(str(self.conclusion))
        return inicio + fin

    def __repr__(self):
        """
        Representación de la proposición para depuración.

        Devuelve: texto para depuración.
        """
        # Mostramos la información más relevante.
        return "Razonamiento({0})".format(self)

    def variables(self):
        """
        Obtiene la lista de variables del razonamiento y las devuelve.

        Devuelve: lista de variables del razonamiento.
        """
        # Devolvemos el conjunto de las variables tanto de las premisas como
        # de la conclusión (se usa conjunto para evitar repetidos).
        return frozenset.union(self.conclusion.variables(),
                               *[premisa.variables()
                                 for premisa in self.premisas])

    def ver_tabla_verdad(self):
        """
        Muestra la tabla de verdad del razonamiento.

        Muestra por un lado la tabla de verdad de las premisas
        y por otro el de la conclusión.
        """
        # Ordenamos las varibles.
        variables = sorted(self.variables())

        # Creamos la tabla de verdad.
        filas = _crea_filas_tabla_verdad(variables)

        # Mostramos las variables.
        literales = ["{0: ^5}".format(variable)
                     for variable in variables]

        # Mostramos las premisas.
        premisas = ["{0: ^6}".format(str(premisa))
                    for premisa in self.premisas]

        # Mostramos la conclusión.
        conclusion = "{0: ^10}".format(str(self.conclusion))

        # Componemos la cabecera.
        cabecera_literales = "  ".join(literales)
        cabecera_premisas = "{0: ^8}".format("   ".join(premisas))
        formato = "{0}  |  {1: ^{2}}  |  {3: ^{4}}"
        print(formato.format(" " * len(cabecera_literales),
                             "premisas",
                             len(cabecera_premisas),
                             "conclusion",
                             len(conclusion)))
        formato = "{0}  |  {1: ^8}  |  {2}"
        header = formato.format(cabecera_literales,
                                cabecera_premisas,
                                conclusion)

        # Mostramos la cabecera y un separador.
        print(header)
        print("="*len(header))

        # Recorremos las filas de la tabla de verdad.
        for fila in filas:
            # Evalumos las premisas.
            valores_premisas = [premisa.evaluar(**fila)
                                for premisa in self.premisas]

            # Evaluamos la conclusión.
            valor_conclusion = self.conclusion.evaluar(**fila)

            # Marca para indicar que las premisas son correctas.
            todas = all(valor
                        for valor in valores_premisas)
            estrella = "*" if todas else ""

            # Formateamos cada variable.
            formateo = ("{0: ^{1}}".format(str(fila[variable]),
                                           len(literal))
                        for (literal, variable)
                        in zip(literales, variables))
            columnas_variables = "  ".join(formateo)

            # Formateamos las premisas.
            formateo = ("{0: ^{1}}".format(str(valor) + estrella,
                                           len(premisa))
                        for (premisa, valor)
                        in zip(premisas, valores_premisas))
            columnas_premisas = "   ".join(formateo)

            # Formateamos la conclusión.
            columna_conclusion = "{0: ^{1}}".format(str(valor_conclusion) +
                                                    estrella,
                                                    len(conclusion))

            # Juntamos todo.
            formato = "{0}  |  {1: ^8}  |  {2}"
            print(formato.format(columnas_variables,
                                 columnas_premisas,
                                 columna_conclusion))

        # Forzamos un salto de línea.
        print()

    def sustituye(self, una, otra):
        """
        Realiza una sustitución dentre de la proposición.

        Argumentos:
        - una: parte a sustituir.
        - otra: parte con la que sustituir a la una.

        Devuelve: proposición con la sustitución hecha.
        """
        # Devolvemos un nuevo razonamiento con las sustituciones hechas, tanto
        # en las premisas como en la conclusión.
        return Razonamiento(*[premisa.sustituye(una, otra)
                              for premisa
                              in self.premisas],
                            conclusion=self.conclusion.sustituye(una, otra))

    def es_valido(self):
        """
        Indica si el razonamiento es válido.

        Es decir, si se puede inferir la conclusión a partir de las premisas.

        Devuelve: True si es válido, False en caso contrario.
        """
        # Obtenemos las variables de las premisas.
        variables_premisas = [premisa.variables()
                              for premisa in self.premisas]
        variables_premisas = (frozenset.union(*variables_premisas)
                              if self.premisas else frozenset())

        # Les agregamos las variables de la conclusión.
        variables = (variables_premisas |
                     self.conclusion.variables())

        # Creamos la tabla de verdad.
        tabla = _crea_filas_tabla_verdad(variables)

        # Las evaluamos y miramos si la conclusión es cierta en todas las
        # filas donde las premisas se evalúan como ciertas.
        return all(self.conclusion.evaluar(**fila)
                   for fila in tabla
                   if all(premisa.evaluar(**fila)
                          for premisa in self.premisas))


# %% --- MAIN -----------------------------------------------------------------

if __name__ == "__main__":
    # Ejemplos de lógica de proposiciones.

    print()
    print("-----------------")
    print("--- VARIABLES ---")
    print("-----------------")
    print()
    # Definimos las proposiciones
    P = Variable("P")
    Q = Variable("Q")
    R = Variable("R")
    VARIABLES = [variable.nombre for variable in [P, Q, R]]
    print("Variables: {0}".format(VARIABLES))
    print()

    # Definimos unas cuantas proposiciones simples.
    negacion = ~P
    conjuncion = P & Q
    disyuncion = P | Q
    implicacion1 = P >> Q
    implicacion2 = P << Q
    equivalencia = Equivale(P, Q)

    print("-----------------------------------")
    print("--- OPERACIONES LÓGICAS BÁSICAS ---")
    print("-----------------------------------")
    print()
    # Mostramos las tablas de verdad.
    negacion.ver_tabla_verdad()
    conjuncion.ver_tabla_verdad()
    disyuncion.ver_tabla_verdad()
    implicacion1.ver_tabla_verdad()
    implicacion2.ver_tabla_verdad()
    equivalencia.ver_tabla_verdad()

    print("------------------------------")
    print("--- VARIABLES Y CONSTANTES ---")
    print("------------------------------")
    print()
    # Se puede operar sólo con constantes.
    V = Constante(True)
    F = Constante(False)
    print("Valor de V: {0}".format(V.valor))
    print("Valor de F: {0}".format(F.valor))
    print()
    constantes = V & F
    constantes.ver_tabla_verdad()

    # Mezcla de variables y constantes.
    mezcla = P & V
    mezcla.ver_tabla_verdad()

    print("----------------------------")
    print("--- SENTENCIAS COMPLEJAS ---")
    print("----------------------------")
    print()
    # Proposiciones más complejas.
    compleja1 = (P & Q) >> R & Q << R
    compleja1.ver_tabla_verdad()
    print("Es Tautología: {0}".format(compleja1.es_tautologia()))
    print("Es Contradicción: {0}".format(compleja1.es_contradiccion()))
    print("Es Contingente: {0}".format(compleja1.es_contingente()))
    print()

    # Proposición aun más compleja.
    compleja2 = (P & Q) >> ((R & ~Q) | (R >> ~Q))
    compleja2.ver_tabla_verdad()
    print()

    print("-------------------")
    print("--- SIMILITUDES ---")
    print("-------------------")
    print()
    # Comprobamos propiedades de similitud.
    primera = P >> Q
    segunda = ~P | Q
    primera.ver_tabla_verdad()
    segunda.ver_tabla_verdad()
    equivalentes = primera.es_equivalente(segunda)
    identicas = primera.es_identica(segunda)
    print("Son Equivalentes: {0}".format(equivalentes))
    print("Son Idénticas: {0}".format(identicas))
    print()

    print("-----------------------------")
    print("--- EQUIVALENCIAS TÍPICAS ---")
    print("-----------------------------")
    print()
    # Comprobamos la lista de equivalencias más típicas.
    print("--- Constantes ---")
    no_V = ~V
    no_F = ~F
    print("¬V <=> F: {0}".format(no_V.es_equivalente(F)))
    print("V <=> ¬F: {0}".format(V.es_equivalente(no_F)))
    print()

    p_y_V = P & True
    p_y_F = P & False
    p_o_V = P | True
    p_o_F = P | False
    print("P ^ V <=> P: {0}".format(p_y_V.es_equivalente(P)))
    print("P ^ F <=> F: {0}".format(p_y_F.es_equivalente(False)))
    print("P v V <=> V: {0}".format(p_o_V.es_equivalente(True)))
    print("P v F <=> P: {0}".format(p_o_F.es_equivalente(P)))
    print()

    p_y_no_p = P & ~P
    p_o_no_p = P | ~P
    print("P ^ ¬P <=> F: {0}".format(p_y_no_p.es_equivalente(False)))
    print("P v ¬P <=> V: {0}".format(p_o_no_p.es_equivalente(True)))
    print()

    print("--- Doble Negación ---")
    no_no_p = ~~P
    print("¬¬P ^ P <=> P: {0}".format(no_no_p.es_equivalente(P)))
    print()

    print("--- Idempotente ---")
    p_y_p = P & P
    p_o_p = P | P
    print("P ^ P <=> P: {0}".format(p_y_p.es_equivalente(P)))
    print("P v P <=> P: {0}".format(p_o_p.es_equivalente(P)))
    print()

    print("--- Conmutativa ---")
    izq = P & Q
    der = Q & P
    MSG = "P ^ Q <=> Q ^ P: {0}"
    print(MSG.format(izq.es_equivalente(der)))
    izq = P | Q
    der = Q | P
    MSG = "P v Q <=> Q v P: {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Asociativa ---")
    izq = (P & Q) & R
    der = P & (Q & R)
    MSG = "(P ^ Q) ^ R <=> P ^ (Q ^ R): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    izq = (P | Q) | R
    der = P | (Q | R)
    MSG = "(P v Q) v R <=> P v (Q v R): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Absorción ---")
    izq = P & (P | Q)
    der = P
    MSG = "P ^ (P v Q) <=> P: {0}"
    print(MSG.format(izq.es_equivalente(der)))
    izq = P | (P & Q)
    der = P
    MSG = "P v (P ^ Q) <=> P: {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Distributiva ---")
    izq = P & (Q | R)
    der = (P & Q) | (P & R)
    MSG = "P ^ (Q v R) <=> (P ^ Q) v (P ^ R): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    izq = P | (Q & R)
    der = (P | Q) & (P | R)
    MSG = "P v (Q ^ R) <=> (P v Q) ^ (P v R): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Leyes de De Morgan ---")
    izq = ~(P & Q)
    der = ~P | ~Q
    MSG = "¬(P ^ Q) <=> ¬P v ¬Q: {0}"
    print(MSG.format(izq.es_equivalente(der)))
    izq = ~(P | Q)
    der = ~P & ~Q
    MSG = "¬(P v Q) <=> ¬P ^ ¬Q: {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Contraposición ---")
    izq = P >> Q
    der = ~Q >> ~P
    MSG = " (P => Q) <=> (¬Q => ¬P): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Eliminar Condicional ---")
    izq = P >> Q
    der = ~P | Q
    MSG = " (P => Q) <=> (¬P v Q): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("--- Eliminar Bicondicional ---")
    izq = Equivale(P, Q)
    der = (P & Q) | (~P & ~Q)
    MSG = " (P <=> Q) <=> (P ^ Q) v (¬P ^ ¬Q): {0}"
    print(MSG.format(izq.es_equivalente(der)))
    print()

    print("---------------------")
    print("--- SUSTITUCIONES ---")
    print("---------------------")
    print()
    # Cambiamos la P por una T
    T = Variable("T")
    sustituida = compleja1.sustituye(P, T)
    sustituida.ver_tabla_verdad()

    # Cambiamos la R por un True
    sustituida = sustituida.sustituye(R, True)
    sustituida.ver_tabla_verdad()

    print("--------------------")
    print("--- RAZONAMIENTO ---")
    print("--------------------")
    print()
    # Miramos si el razonamiento es válido.
    premisa1 = P >> Q
    premisa2 = Q >> R
    demostrar = P >> R
    razonamiento = Razonamiento(premisa1,
                                premisa2,
                                conclusion=demostrar)
    razonamiento.ver_tabla_verdad()
    print("Es Valido: {0}".format(razonamiento.es_valido()))
