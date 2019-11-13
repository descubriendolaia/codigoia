#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de inferencias realizadas mediante probabilidad y que luego serán la
base de las redes bayesianas.
"""


# %% --- INDEPENDENCIA MARGINAL O ABSOLUTA ---

# Si dos sucesos A y B son independientes entre sí:
# P(A|B) = P(A)
# Es decir, B no afecta para nada a B.
print("******************************")
print("*** INDEPENDENCIA ABSOLUTA ***")
print("******************************")
print()

# Datos: P(A=5,B=3) = P(A=5|B=3)·P(B=3) = P(A=5)·P(B=3) = 1/6 · 1/6 = 1/36
# Probabilida de sacar un 5 en un dado.
prob_5 = 1 / 6
msg = "Probabilida de sacar un 5 en un dado: {0}"
print(msg.format(prob_5))

# Probabilida de sacar un 3 en un dado
prob_3 = 1 / 6
msg = "Probabilida de sacar un 3 en un dado: {0}"
print(msg.format(prob_3))

# Probabilidad de sacar un 3 y un 5 a la vez en dos dados.
prob_3_y_5 = prob_3 * prob_5
msg = "Probabilidad de sacar un 3 y un 5 a la vez en dos dados: {0}"
print(msg.format(prob_3_y_5))

# Esta última fórmula se puede ampliar cuando todas la variables son
# independientes entre sí: P(A|B,C,D,...) = P(A)
# P(A,B,C,D,E,...) = P(A)·P(B)·P(C)·P(D)·P(E)·...


# %% --- INDEPENDENCIA CONDICIONAL ---

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
p_fiebre_tras_gripe = 0.89231
msg = "Probabilidad de tener fiebre si se tienen gripe: {0}"
print(msg.format(p_fiebre_tras_gripe))

# Probabilidad de tener dolor de garganta si se tiene gripe: P(D|G)
p_garganta_tras_gripe = 0.94213
msg = "Probabilidad de tener dolor de garganta si se tienen gripe: {0}"
print(msg.format(p_garganta_tras_gripe))

# Probabilida de tener ambas cosas si se tiene gripe: P(F|G)·P(D|G)
p_fiebre_garganta_tras_gripe = p_fiebre_tras_gripe * p_garganta_tras_gripe
msg = "Probabilidad de tener ambos si se tienen gripe: {0}"
print(msg.format(p_fiebre_garganta_tras_gripe))


# %% --- REGLA DE BAYES ---

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
prob_g = 0.30000
prob_no_g = 1 - 0.30000
msg = "Probabilida de tener gripe: {0}"
print(msg.format(prob_g))
msg = "Probabilida de NO tener gripe: {0}"
print(msg.format(prob_no_g))

# Probabilidades de tener fiebre si se tiene gripe: P(F|G)
prob_f_tras_g = 0.60000
msg = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(msg.format(prob_f_tras_g))

# Probabilidad de tener fiebre cuanto NO se tiene gripe: P(F|¬G)
prob_f_tras_no_g = 0.07000
msg = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(msg.format(prob_f_tras_no_g))

# Probabilidades de tener dolor de garganta si se tiene gripe: P(D|G)
prob_d_tras_g = 0.80000
msg = "Probabilidad de tener dolor de garganta si se tiene gripe: {0}"
print(msg.format(prob_d_tras_g))

# Probabilidad de tener dolor de garganta cuanto NO se tiene gripe: P(D|¬G)
prob_d_tras_no_g = 0.10000
msg = "Probabilidad de tener dolor de garganta cuanto NO se tiene gripe: {0}"
print(msg.format(prob_d_tras_no_g))

# Calculamos el factor de normalización.
# P(F) = P(F|G)·P(G) + P(F|¬G)·P(¬G)
# P(D) = P(D|G)·P(G) + P(D|¬G)·P(¬G)
# P(F)·P(G) = [P(F|G)·P(G) + P(F|¬G)·P(¬G)]·[P(D|G)·P(G) + P(D|¬G)·P(¬G)]
# P(F)·P(G) = P(F|G)·P(G)·P(D|G)·P(G) +
#             P(F|G)·P(G)·P(D|¬G)·P(¬G) +
#             P(F|¬G)·P(¬G)·P(D|G)·P(G)
#             P(F|¬G)·P(¬G)·P(D|¬G)·P(¬G)
# alfa = 1 / P(F)·P(G)
f_g = prob_f_tras_g * prob_g
f_no_g = prob_f_tras_no_g * prob_no_g
d_g = prob_d_tras_g * prob_g
d_no_g = prob_d_tras_no_g * prob_no_g
alfa = 1 / ((f_g * d_g) +
            (f_g * d_no_g) +
            (f_no_g + d_g) +
            (f_no_g * d_no_g))
msg = "Factor alfa de normalización: {0}"
print(msg.format(alfa))

# Probabilidad de tener gripe si se tiene fiebre y dolor de garganta:
# P(G|F,D) = [P(F|G)·P(D|G)·P(G)] / [P(F)·P(D)] = alfa·P(F|G)·P(D|G)·P(G)
prob_g_tras_f_y_d = alfa * prob_f_tras_g * prob_d_tras_g * prob_g
msg = "Probabilidad de tener gripe si se tiene fiebre y dolor de garganta: {0}"
print(msg.format(prob_g_tras_f_y_d))
