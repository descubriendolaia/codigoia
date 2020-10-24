#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de Inferencia en Probabilidad.

Ejemplos de inferencias realizadas mediante probabilidad y que luego serán la
base de las redes bayesianas.
"""


# %% --- INDEPENDENCIA MARGINAL O ABSOLUTA ------------------------------------

# Si dos sucesos A y B son independientes entre sí:
# P(A|B) = P(A)
# Es decir, B no afecta para nada a B.
print("******************************")
print("*** INDEPENDENCIA ABSOLUTA ***")
print("******************************")
print()

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

# Esta última fórmula se puede ampliar cuando todas la variables son
# independientes entre sí: P(A|B,C,D,...) = P(A)
# P(A,B,C,D,E,...) = P(A)·P(B)·P(C)·P(D)·P(E)·...


# %% --- INDEPENDENCIA CONDICIONAL --------------------------------------------

# Si A y B son independientes:
# P(A|B,C) = P(A|C)
# P(A,B|C) = P(A|B,C)·P(B|C) = P(A|C)·P(B|C)
# Esto se puede ampliar a múltiples variables independientes entre sí:
# P(A1,A2,A3,...,An|B) = P(A1|B)·P(A2|B)·P(A3|B)·...·P(An|B)
print("*********************************")
print("*** INDEPENDENCIA CONDICIONAL ***")
print("*********************************")
print()

# Ejemplo: F = tener fiebre, D = tener dolor de garganta, G = tener gripe.
# Tener fiebre y tener dolor de garganta son independientes entre sí.
# La probabilidad de tener fiebre y dolor de garganta si se tiene gripe:
# P(F,D|G) = P(F|G)·P(D|G)
# Es decir, sería la multiplicación de la probabilida de tener fiebre cuando
# se tiene gripe por la multiplicación de tener dolor de garganta cuando se
# tiene gripe:

# Probabilidad de tener fiebre si se tiene gripe: P(F|G)
P_FIEBRE_TRAS_GRIPE = 0.89231
MSG = "Probabilidad de tener fiebre si se tienen gripe: {0}"
print(MSG.format(P_FIEBRE_TRAS_GRIPE))

# Probabilidad de tener dolor de garganta si se tiene gripe: P(D|G)
P_GARGANTA_TRAS_GRIPE = 0.94213
MSG = "Probabilidad de tener dolor de garganta si se tienen gripe: {0}"
print(MSG.format(P_GARGANTA_TRAS_GRIPE))

# Probabilida de tener ambas cosas si se tiene gripe: P(F|G)·P(D|G)
P_FIEBRE_GARGANTA_TRAS_GRIPE = P_FIEBRE_TRAS_GRIPE * P_GARGANTA_TRAS_GRIPE
MSG = "Probabilidad de tener ambos si se tienen gripe: {0}"
print(MSG.format(P_FIEBRE_GARGANTA_TRAS_GRIPE))


# %% --- REGLA DE BAYES -------------------------------------------------------

# La independencia condicional se puede aplicar a la Regla de Bayes para
# simplificar (y mucho, en algunos casos) los cálculos:
print("**********************")
print("*** REGLA DE BAYES ***")
print("**********************")
print()

# Para el caso de 2 variables (A y B) cuando se ha dado otra (C):
# P(A,B|C) = P(A|B,C)·P(B|C)
# P(A,B|C) = P(B|A,C)·P(A|C)
# Igualando los 2 resultados:
# P(A|B,C)·P(B|C) = P(B|A,C)·P(A|C)
# Despejando uno de los factores:
# P(A|B,C) = [P(B|A,C)·P(A|C)] / P(B|C)
# Aplicando la Regla de Bayes a P(A|C) = [P(C|A)·P(A)] / P(C), queda:
# P(A|B,C) = [P(B|A,C)·P(C|A)·P(A)] / [P(B|C)·P(C)]
# Pero, si B y C son independientes, se pueden simplificar algunos términos:
# P(B|A,C) = P(B|A)
# P(B|C) = P(B)
# Con lo que quedaría:
# P(A|B,C) = [P(B|A)·P(A|C)·P(A)] / [P(B)·P(C)]
# Y esto puede ahorrar muchos cálculos, lo que supuso un gran avance.

# Ejemplo: G = tener gripe, F = fiebre, D = dolor de garganta.
# La probabilidad de tener gripe si se tiene fiebre y dolor de garganta:
# P(G|F,D) = [P(F|G,D)·P(D|G)·P(G)] / [P(F|D)·P(D)]
# Lo que seríe difícil de obtener y calcular (sobre todo P(F|G,D) y P(F|D)).
# Pero como tener fiebre y dolor de garganta son independientes:
# P(G|F,D) = [P(F|G)·P(D|G)·P(G)] / [P(F)·P(D)]
# Donde:
# P(F|G) es la probabilidad de tener fiebre cuando se tiene gripe.
# P(D|G) es la probabilidad de dolor de garganta cuando se tiene gripe.
# P(G) es la probabilidad de tener gripe.
# P(F) es la probabilidad marginal de tener fiebre.
# P(D) es la probabilidad marginal de tener dolor de garganta.
# Todas estas probabilidades son relativamente fáciles de obtener y calcular.

# ProbabilidaS de tener gripe: P(G) y P(¬G)
PROB_G = 0.30000
PROB_NO_G = 1 - 0.30000
MSG = "Probabilida de tener gripe: {0}"
print(MSG.format(PROB_G))
MSG = "Probabilida de NO tener gripe: {0}"
print(MSG.format(PROB_NO_G))

# Probabilidades de tener fiebre si se tiene gripe: P(F|G)
PROB_F_TRAS_G = 0.60000
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_G))

# Probabilidad de tener fiebre cuanto NO se tiene gripe: P(F|¬G)
PROB_F_TRAS_NO_G = 0.07000
MSG = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_NO_G))

# Probabilidades de tener dolor de garganta si se tiene gripe: P(D|G)
PROB_D_TRAS_G = 0.80000
MSG = "Probabilidad de tener dolor de garganta si se tiene gripe: {0}"
print(MSG.format(PROB_D_TRAS_G))

# Probabilidad de tener dolor de garganta cuanto NO se tiene gripe: P(D|¬G)
PROB_D_TRAS_NO_G = 0.10000
MSG = "Probabilidad de tener dolor de garganta cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_D_TRAS_NO_G))

# Calculamos el factor de normalización.
# P(F) = P(F|G)·P(G) + P(F|¬G)·P(¬G)
# P(D) = P(D|G)·P(G) + P(D|¬G)·P(¬G)
# P(F)·P(G) = [P(F|G)·P(G) + P(F|¬G)·P(¬G)]·[P(D|G)·P(G) + P(D|¬G)·P(¬G)]
# P(F)·P(G) = P(F|G)·P(G)·P(D|G)·P(G) +
#             P(F|G)·P(G)·P(D|¬G)·P(¬G) +
#             P(F|¬G)·P(¬G)·P(D|G)·P(G)
#             P(F|¬G)·P(¬G)·P(D|¬G)·P(¬G)
# alfa = 1 / P(F)·P(G)
F_G = PROB_F_TRAS_G * PROB_G
F_NO_G = PROB_F_TRAS_NO_G * PROB_NO_G
D_G = PROB_D_TRAS_G * PROB_G
D_NO_G = PROB_D_TRAS_NO_G * PROB_NO_G
ALFA = 1 / ((F_G * D_G) +
            (F_G * D_NO_G) +
            (F_NO_G + D_G) +
            (F_NO_G * D_NO_G))
MSG = "Factor alfa de normalización: {0}"
print(MSG.format(ALFA))

# Probabilidad de tener gripe si se tiene fiebre y dolor de garganta:
# P(G|F,D) = [P(F|G)·P(D|G)·P(G)] / [P(F)·P(D)] = alfa·P(F|G)·P(D|G)·P(G)
PROB_G_TRAS_F_Y_D = ALFA * PROB_F_TRAS_G * PROB_D_TRAS_G * PROB_G
MSG = "Probabilidad de tener gripe si se tiene fiebre y dolor de garganta: {0}"
print(MSG.format(PROB_G_TRAS_F_Y_D))
