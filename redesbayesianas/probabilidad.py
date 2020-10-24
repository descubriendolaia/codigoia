#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bases de la Propabilidad.

Ejemplos de las bases de la probabilidad que luego se usarán en las redes
bayesianas.
"""
import random


# %% --- AXIOMAS DE KOLGOMOROV ------------------------------------------------

# Existe varias formas de sentar la reglas básicas de la probabilidad. Una
# bastante común es la definición de aximas hechas por Kolgomorov:
# - La probabilidad P de un evento E debe estar siempre entre 0 y 1:
#    0 <= P(E) <= 1
# - La probabilidad de un evento cierto es 1 y de uno false es 0:
#    P(cierto) = 1 ; P(falso) = 0
# - Principio de Inclusión y Exclusión (ambas expresiones son equivalentes):
#    P(A o B) = P(A) + P(B) - P (A y B)
#    P(A y B) = P(A) + P(B) - P (A o B)
# Nota: la probabilidad conjunta P(A y B) también se escribe P(A,B)
print("***************")
print("*** AXIOMAS ***")
print("***************")
print()

# Una propiedad importante de los dos primeros axiomas es que la probabilidad
# de que un evento no se dé es 1 menos la probabilidad de que el evento se dé:
#    P(¬E) = 1 - P(E)

# Probabilida de que llueva mañana
PROB_A = 0.78612567
MSG = "Probablidad de que llueva mañana: {0}"
print(MSG.format(PROB_A))

# Probabilidad de que NO llueva mañana.
PROB_B = 1.0 - PROB_A
MSG = "Probablidad de que NO llueva mañana: {0}"
print(MSG.format(PROB_B))

# Otra propiedad importante del tercer axioma es que si dos evento son
# excluyentes entre sí (no pueden darse a la vez), entonces P(A y B) = 0, ya
# que P(A o B) = P(A) + P(B)
print()

# Probabilidad de que salga un 1 en un dado.
PROB_1 = 1 / 6
MSG = "Probabilidad de que salga un 1 en un dado: {0}"
print(MSG.format(PROB_1))

# Probabilidad de que salga un 5 en un dado.
PROB_5 = 1 / 6
MSG = "Probabilidad de que salga un 5 en un dado: {0}"
print(MSG.format(PROB_5))

# No puede salir un 1 y un 5 a la vez en un dado: P(A=1,A=5) = 0
MSG = "Probabilidad de que salga un 1 o un 5 en un dado: {0}"
PROB_1_OR_5 = PROB_1 + PROB_5
print(MSG.format(PROB_1_OR_5))

# Probabilidad de que salga un 3 en un dado.
PROB_3 = 1 / 6
MSG = "Probabilidad de que salga un 3 en un dado: {0}"
print(MSG.format(PROB_3))

# No puede salir un 1, un 3 o un 5 a la vez en un dado: P(A=1,A=5,A=3) = 0
MSG = "Probabilidad de que salga un 1, un 3 o un 5 en un dado: {0}"
PROB_1_OR_3_OR_5 = PROB_1 + PROB_3 + PROB_5
print(MSG.format(PROB_1_OR_3_OR_5))


# %% --- DEFINICIONES ---------------------------------------------------------

# Un experimento puede ser sacar un número entero aleatorio entre 1 y 10.
# El espacio muestral son todos los números enteros que hay entre 1 y 10.
# Un evento simple es sacar una vez un número aleatorio:
evento = random.randint(1, 10)
print("***************")
print("*** EVENTOS ***")
print("***************")
print()
print("--- Evento Simple ---")
MSG = "1 nº aleatorio entre 1 y 10: {0}"
print(MSG.format(evento))

# En este caso, la probabilidad de que salga cualquier número es la misma,
# por lo que se dice que son "equiprobables".
print("Probabilidad: 1/10 para todos (equiprobable)")
print()

# Un evento múltiple es sacar varios números aleatorios:
EVENTO_1 = random.randint(1, 10)
EVENTO_2 = random.randint(1, 10)
EVENTO_3 = random.randint(1, 10)
print("--- Evento Múltiple ---")
MSG = "3 nº aleatorios entre 0 y 10: ({0}, {1}, {2})"
print(MSG.format(EVENTO_1, EVENTO_2, EVENTO_3))
print("Probabilidad de 3 unos: (1/10)·(1/10)·(1/10) = 1/1000")
print()

# %% --- FRECUENCIA RELATIVA --------------------------------------------------
# Número de veces que ocurre un evento frente al número de veces que se repite
# un experimento. Si se repite un número muy elevado de veces, cada vez nos
# aproximaremos más y más a la probabilidad real.
print("***************************")
print("*** FRECUENCIA RELATIVA ***")
print("***************************")
print()

# El experimento será lanzar una moneda al aire.
# El espacio muestral será: cara o cruz.
# Cada lanzamiento de moneda será un evento.
print("--- Lanzar una Moneda ---")
print("Cara: 1")
print("Cruz: 0")

# Iremos aumentando cada vez más los resultados.
LIMITES = [10, 100, 1000, 10000, 100000, 1000000]

for veces in LIMITES:
    # Guardará la lista de resultados de lanzar una moneda varias veces.
    resultados = []

    # Contabilizará el número de veces que sale cada resultado.
    CARAS = 0
    CRUCES = 0

    # Lanzamos la moneda varias veces.
    print("Lanzamos la moneda {0} veces:".format(veces))
    for i in range(0, veces):
        # Lanzamos la moneda.
        resultado = random.randint(0, 1)

        # Aumentamos las caras o las cruces según el resultado.
        if resultado == 1:
            CARAS += 1
        elif resultado == 0:
            CRUCES += 1

        # Agregamos el resultado a la lista de resultados.
        resultados.append(resultado)

    # Moramos los resultado obtenidos.
    MSG = "Resultados: [{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, ...]"
    ejemplos = resultados[:8]
    print(MSG.format(ejemplos[0],
                     ejemplos[1],
                     ejemplos[2],
                     ejemplos[3],
                     ejemplos[4],
                     ejemplos[5],
                     ejemplos[6],
                     ejemplos[7]))

    # Mostramos las frecuencias relativas
    MSG = "  - Caras: {0} -> Frecuencia Relativa: {1}"
    print(MSG.format(CARAS, CARAS / veces))
    MSG = "  - Cruces: {0} -> Frecuencia Relativa: {1}"
    print(MSG.format(CRUCES, CRUCES / veces))
    print()


# %% --- PROBABILIDAD A POSTERIORI --------------------------------------------

# La probabilidad a priori es la probabilidad en ausencia de más información.
# La probabilidad a posteriori es la probabilidad cuando aparece nueva
# información a tener en cuenta. Thomas Bayes postuló que:
# P(A|B) = P(A,B) / P(A).
# Donde P(A,B) es la probabilidad conjunta, es decir, la probabilidad de que
# se den al mismo tiempo los resultados A y B.

# El primer evento A será elegir un número entero entre 1 y 10.
# La probabilidad a priori P(A=5) será de 1/10.
# La probabilidad de que salga un 5 cuando antes ya ha salido un 3 es una
# probabilidad a posteriori:
# P(A=5|B=3) = P(A=5,B=3) / P(A=5)

# Como son evento equiprobables e independientes, la probabilidad de que salga
# en un evento el 5 y en otro el 3 es P(A=5,B=3) = 1/10 · 1/10 = 1/100.
# P(A=5|B=3) = P(A=5,B=3) / P(A=5) = (1/100) / (1/10) = 1/10
# Lo que es lógico, porque son evento independientes, como ya se ha dicho.
print("*********************************")
print("*** PROBABILIDAD A POSTERIORI ***")
print("*********************************")
print()


def frecuencia_relativa(espacio_muestral,
                        valor,
                        limite=10000):
    """
    Permite calcular la probabilidad según una frecuencia relativa.

    Argumentos:
    - espacio_muestral: lista con valores posibles del experimento.
    - valor: valor del que obtener la frecuencia relativa.
    - limite: número de veces que se repetirá el experimiento.

    Devuelve: frecuencia relativa del valor una vez se repite el experimiento
              un número de veces (indicado por límite).
    """
    # Comprobaciones.
    if not espacio_muestral:
        raise ValueError("No ha indicado un espacio muestral")
    if limite <= 0:
        limite = 10000

    # Guardaremos las veces que se repite cada resultado.
    veces_valor = {valor: 0 for valor in espacio_muestral}

    # Asociamos un número con cada resultado.
    longitud = len(espacio_muestral)
    indice = dict(zip(range(0, longitud), espacio_muestral))

    # Repetimos varias veces el experimento.
    for _ in range(0, limite):
        # Ejecutamos el experimiento.
        aleatorio = random.randint(0, longitud-1)

        # Aumentamos el contador del resultado.
        valor = indice[aleatorio]
        veces_valor[valor] += 1

    # Devolvemos la frecuencia relativa del solicituda.
    return veces_valor[valor] / limite


# Definimos el espacio muestral: números enteros entre 1 y 10.
print("---- P(A) ----")
NUMEROS = list(range(1, 11))
print("Espacio Muestral: {0}".format(NUMEROS))

# Probabilidad a priori de que salga un 5: P(A=5)
PRIORI_5 = frecuencia_relativa(espacio_muestral=NUMEROS,
                               valor=5)
print("Priori 5: P(A=5) = {0}".format(PRIORI_5))
print()

# Probabilidad a priori de que salga un 5 y un 3: P(A=5,B=3)
print("--- P(A,B) ---")
PARES = [(a, b)
         for b in range(1, 11)
         for a in range(1, 11)]
print("Espacio Muestral: {0}".format(PARES))

# Probabilidad a priori de que salga un 5: P(A=5)
PRIORI_5_3 = frecuencia_relativa(espacio_muestral=PARES,
                                 valor=(5, 3))
print("Priori 5 y 3: P(A=5,B=3) = {0}".format(PRIORI_5_3))

# Vamos a simularlo para ver si da similar.
ACIERTOS = 0
LIMITE = 10000
for n in range(0, LIMITE):
    resultado = random.randint(1, 10)
    if resultado == 3:
        resultado = random.randint(1, 10)
        if resultado == 5:
            ACIERTOS += 1
print("Simulación de P(A=5,B=3) = {0}".format(ACIERTOS / LIMITE))
print()

# Probabilidad a posteriori: P(A=5|B=3)
print("--- P(A|B) = P(A,B) / P(A) ---")
print("Posteriori 5 si 3: P(A=5|B=3) = {0}".format(PRIORI_5_3 / PRIORI_5))
print()


# %% --- REGLA DEL PRODUCTO / MULTIPLICACIÓN ----------------------------------

# A partir de la definición de probabilidad a posteriori, reordenando términos
# se puede definir la regla del producto (o de la multiplicación):
# P(A,B) = P(A|B)·P(B) = P(B|A)·P(A)
# Esto nos da la probabilidad conjunto a partir de la probabilidad a priori y
# la probabilidad condicional (a posteriori).
print("**************************")
print("*** REGLA DEL PRODUCTO ***")
print("**************************")
print()

# Probabilidad de que haya atascos.
PROB_A = 0.46781
MSG = "Probabilidad de que haya atascos: {0}"
print(MSG.format(PROB_A))

# Probabilidad de que mañana llueva: P(A)
PROB_B = 0.81264
MSG = "Probabilidad de que mañana llueva: {0}"
print(MSG.format(PROB_B))

# Probabilidad de que haya atascos después de comenzar a llover: p(B|A)
PROB_A_TRAS_B = 0.98154
MSG = "Probabilidad de que haya atascos después de comenzar a llover: {0}"
print(MSG.format(PROB_A_TRAS_B))

# Probabilidad de que, a la vez, haya atascos y llueva mañana: P(A,B)
PROB_A_Y_B = PROB_A_TRAS_B * PROB_B
MSG = "Probabilidad de que, a la vez, haya atascos y llueva mañana: {0}"
print(MSG.format(PROB_A_Y_B))
MSG = "Luego, si llueve aumentan las probabilidades de atascos: {0} > {1}"
print(MSG.format(PROB_A_Y_B, PROB_A))
print()

# Donde hay que tener en cuenta que, si dos sucesos A y B son independientes
# entre sí: P(A|B) = P(A), es decir, B no afecta para nada a A.
# Datos: P(A=5,B=3) = P(A=5|B=3)·P(B=3) = P(A=5)·P(B=3) = 1/6 · 1/6 = 1/36

# Probabilida de sacar un 5 en un dado.
PROB_5 = 1 / 6
MSG = "Probabilida de sacar un 5 en un dado: {0}"
print(MSG.format(PROB_5))

# Probabilida de sacar un 3 en un dado
PROB_3 = 1 / 6
MSG = "Probabilida de sacar un 3 en un dado: {0}"
print(MSG.format(PROB_3))

# Probabilidad de sacar un 3 y un 5 a la vez en dos dados.
PROB_3_Y_5 = PROB_3 * PROB_5
MSG = "Probabilidad de sacar un 3 y un 5 a la vez en dos dados: {0}"
print(MSG.format(PROB_3_Y_5))

# Debe ser muy similiar si lo hacemos por el enfoque frecuentista.
ESPACIO = [(a, b) for a in range(1, 7) for b in range(1, 7)]
PROB_3_Y_5 = frecuencia_relativa(espacio_muestral=ESPACIO,
                                 valor=(3, 5),
                                 limite=100000)
MSG = "Muy similar al enfoque frecuentista: {0}"
print(MSG.format(PROB_3_Y_5))
print()

# Esta regla se puede ampliar a múltiples sucesos:
# P(A,B,C) = P(A|B,C)·P(B|C)·P(C)
# P(A,B,C,D) = P(A|B,C,D)·P(B|C,D)·P(C|D)·P(D)
# P(A,B,C,D,E) = P(A|B,C,D,E)·P(B|C,D,E)·P(C|D,E)·P(D|E)·P(E)
# ...
# Cuanto más variables, más cálculos hay que hacer (explosión combinacional).

# Esta última fórmula se puede simplificar cuando todas la variables son
# independientes entre sí: P(A|B,C,D,...) = P(A)
# P(A,B,C,D,E,...) = P(A)·P(B)·P(C)·P(D)·P(E)·...
# Esto reduce muchos los cálculos, y será de mucha utilidad más adelante en
# las redes bayesianas.


# %% --- PROBABILIDAD TOTAL / MARGINAL ----------------------------------------

# Se puede calcular la probabilidad de un evento a partir de las probabilidades
# conjuntas con el resto de variables, siempre y cuando el resto de variables
# sean todas independientes entre sí y exhaustivas es:
# P(B) = sum(P(Ai,B)) = sum(P(B|Ai)·P(Ai))
# Donde Ai son todos los posibles valores de A. Para el caso de 1 variable
# boolena, con sólo 2 valores:
# P(B) = P(B|A)·P(A) + P(B|¬A)·P(¬A)
print("***********************************")
print("*** PROBABILIDAD TOTAL/MARGINAL ***")
print("***********************************")
print()

# Probabilida de tener gripe: P(G)
PROB_G = 0.30000
MSG = "Probabilida de tener gripe: {0}"
print(MSG.format(PROB_G))

# Probabilidad de NO tener gripe: P(¬G)
PROB_NO_G = 1 - PROB_G
MSG = "Probabilidad de NO tener gripe:  {0}"
print(MSG.format(PROB_NO_G))

# Probabilidad de tener fiebre si se tiene gripe: P(F|G)
PROB_F_TRAS_G = 0.60000
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_G))

# Probabilidad de tener fiebre cuanto NO se tiene gripe: P(F|¬G)
PROB_F_TRAS_NO_G = 0.07000
MSG = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_NO_G))

# Probabilidad de tener fibre: P(F) = P(F|G)·P(G) + P(F|¬G)·P(¬G)
PROB_F = (PROB_F_TRAS_G * PROB_G) + (PROB_F_TRAS_NO_G * PROB_NO_G)
MSG = "Probabilidad de tener fibre: {0}"
print(MSG.format(PROB_F))


# %% --- REGLA DE BAYES -------------------------------------------------------

# A partir de la regla del producto, reordenando términos en la expresión
# P(A|B)·P(B) = P(B|A)·P(A), se puede definir la Regla de Bayes:
# P(A|B) = [P(B|A)·P(A)] / P(B) = [P(B|A)·P(A)] / sum(P(B|A)·P(A))

# Esta regla es la base del enfoque bayesiano de la probabilidad, en oposición
# al enfoque frecuentista basado en la frecuencia relativa.
print("**********************")
print("*** REGLA DE BAYES ***")
print("**********************")
print()

# Probabilida de tener gripe: P(G)
PROB_G = 0.30000
MSG = "Probabilida de tener gripe: {0}"
print(MSG.format(PROB_G))

# Probabilidad de NO tener gripe: P(¬G)
PROB_NO_G = 1 - PROB_G
MSG = "Probabilidad de NO tener gripe:  {0}"
print(MSG.format(PROB_NO_G))
print()

# Probabilidad de tener fiebre si se tiene gripe: P(F|G)
PROB_F_TRAS_G = 0.60000
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_G))

# Probabilidad de tener fiebre cuanto NO se tiene gripe: P(F|¬G)
PROB_F_TRAS_NO_G = 0.07000
MSG = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_NO_G))

# Probabilidad de NO tener fiebre si se tiene gripe: P(¬F|G)
PROB_NO_F_TRAS_G = 1 - PROB_F_TRAS_G
MSG = "Probabilidad de NO tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_NO_F_TRAS_G))

# Probabilidad de NO tener fiebre cuanto NO se tiene gripe: P(¬F|¬G)
PROB_NO_F_TRAS_NO_G = 1 - PROB_F_TRAS_NO_G
MSG = "Probabilidad de NO tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_NO_F_TRAS_NO_G))
print()

# Probabilidad de tener fibre: P(F) = P(F|G)·P(G) + P(F|¬G)·P(¬G)
PROB_F = (PROB_F_TRAS_G * PROB_G) + (PROB_F_TRAS_NO_G * PROB_NO_G)
MSG = "Probabilidad de tener fibre: {0}"
print(MSG.format(PROB_F))

# Probabilidad de NO tener fibre: P(¬F) = P(¬F|G)·P(G) + P(¬F|¬G)·P(¬G)
PROB_NO_F = (PROB_NO_F_TRAS_G * PROB_G) + (PROB_NO_F_TRAS_NO_G * PROB_NO_G)
MSG = "Probabilidad de NO tener fibre: {0}"
print(MSG.format(PROB_NO_F))
print()

# Probabilidad de tener gripe si se tiene fiebre:
# P(G|F) = P(F|G)·P(G) / P(F)
PROB_G_TRAS_F = (PROB_F_TRAS_G * PROB_G) / PROB_F
MSG = "Probabilidad de tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_F))

# Probabilidad de NO tener gripe si se tiene fiebre:
# P(¬G|F) = P(F|¬G)·P(¬G) / P(F)
PROB_NO_G_TRAS_F = (PROB_F_TRAS_NO_G * PROB_NO_G) / PROB_F
MSG = "Probabilidad de NO tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_F))

# Probabilidad de tener gripe si NO se tiene fiebre:
# P(G|¬F) = P(¬F|G)·P(G) / P(¬F)
PROB_G_TRAS_NO_F = (PROB_NO_F_TRAS_G * PROB_G) / PROB_NO_F
MSG = "Probabilidad de tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_NO_F))

# Probabilidad de NO tener gripe si NO se tiene fiebre:
# P(¬G|¬F) = P(¬F|¬G)·P(¬G) / P(¬F)
PROB_NO_G_TRAS_NO_F = (PROB_NO_F_TRAS_NO_G * PROB_NO_G) / PROB_NO_F
MSG = "Probabilidad de NO tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_NO_F))
print()


# %% --- NORMALIZACION --------------------------------------------------------

# Para no repetir tantos cálculos, se puede usar la normalización 'alfa':
# alfa = 1 / P(B) = 1 / sum(P(B|Ai)·P(Ai)) => P(A|B) = alfa·P(B|A)·P(B)
print("****************************")
print("*** NORMALIZACIÓN (ALFA) ***")
print("****************************")
print()

# Normalización de tener fiebre:
# 1 / P(F) = 1 / [P(F|G)·P(G) + P(F|¬G)·P(¬G)]
ALFA_F = 1 / PROB_F
MSG = "Normalización de tener fiebre: {0}"
print(MSG.format(ALFA_F))

# Normalización de NO tener fiebre:
# 1 / P(¬F) = 1 / [P(¬F|G)·P(G) + P(¬F|¬G)·P(¬G)]
ALFA_NO_F = 1 / PROB_NO_F
MSG = "Normalización de NO tener fiebre: {0}"
print(MSG.format(ALFA_NO_F))
print()

# Probabilidad de tener gripe si se tiene fiebre:
# P(G|F) = alfaF·P(F|G)·P(G)
PROB_G_TRAS_F = ALFA_F * PROB_F_TRAS_G * PROB_G
MSG = "Probabilidad de tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_F))

# Probabilidad de NO tener gripe si se tiene fiebre:
# P(¬G|F) = alfaF·P(F|¬G)·P(¬G)
PROB_NO_G_TRAS_F = ALFA_F * PROB_F_TRAS_NO_G * PROB_NO_G
MSG = "Probabilidad de NO tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_F))

# Probabilidad de tener gripe si NO se tiene fiebre:
# P(G|¬F) = alfa¬F·P(¬F|G)·P(G)
PROB_G_TRAS_NO_F = ALFA_NO_F * PROB_NO_F_TRAS_G * PROB_G
MSG = "Probabilidad de tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_NO_F))

# Probabilidad de NO tener gripe si NO se tiene fiebre:
# P(¬G|¬F) = alfa¬F·P(¬F|¬G)·P(¬G)
PROB_NO_G_TRAS_NO_F = ALFA_NO_F * PROB_NO_F_TRAS_NO_G * PROB_NO_G
MSG = "Probabilidad de NO tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_NO_F))
print()


# %% --- PROPIEDADES ÚTILES ---------------------------------------------------

# La probabilida de que se haya dado un evento si ya se ha dado, es 1:
# P(A|A) = 1
# Por lo tanto, da igual el resto de evento que se den, seguirá siendo 1:
# P(A|A,B,C,D,E,...) = 1

# La Regla del Producto y la Regla de Bayes se puede ampliar con más variables,
# e incluso se pueden combinar entre sí. Las más útiles son:
# P(A,B|C) = P(A|B,C)·P(B|C) = P(B|A,C)·P(A|C)
# P(A|B,C) = [P(B|A,C)·P(A|C)] / P(B|C) = [P(C|A,B)·P(A|B)] / P(C|B)

# En ambos casos lo que se ha hecho es aplicar la Regla del Producto (primera)
# y la Regla de Bayes (segunda) cuand ya ha ocurrido otro evento C.
