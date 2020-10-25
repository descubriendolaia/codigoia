#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bases de la Propabilidad.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""
import random


# %%
PROB_A = 0.78612567
MSG = "Probablidad de que llueva mañana: {0}"
print(MSG.format(PROB_A))
PROB_B = 1.0 - PROB_A
MSG = "Probablidad de que NO llueva mañana: {0}"
print(MSG.format(PROB_B))

# %%
PROB_1 = 1 / 6
MSG = "Probabilidad de que salga un 1 en un dado: {0}"
print(MSG.format(PROB_1))
PROB_5 = 1 / 6
MSG = "Probabilidad de que salga un 5 en un dado: {0}"
print(MSG.format(PROB_5))
MSG = "Probabilidad de que salga un 1 o un 5 en un dado: {0}"
PROB_1_OR_5 = PROB_1 + PROB_5
print(MSG.format(PROB_1_OR_5))
PROB_3 = 1 / 6
MSG = "Probabilidad de que salga un 3 en un dado: {0}"
print(MSG.format(PROB_3))
MSG = "Probabilidad de que salga un 1, un 3 o un 5 en un dado: {0}"
PROB_1_OR_3_OR_5 = PROB_1 + PROB_3 + PROB_5
print(MSG.format(PROB_1_OR_3_OR_5))


# %%
EVENTO = random.randint(1, 10)
MSG = "1 nº aleatorio entre 1 y 10: {0}"
print(MSG.format(EVENTO))


# %%
print("--- Lanzar una Moneda ---")
print("Cara: 1")
print("Cruz: 0")
LIMITES = [10, 100, 1000, 10000, 100000, 1000000]
for veces in LIMITES:
    resultados = []
    CARAS = 0
    CRUCES = 0
    print("Lanzamos la moneda {0} veces:".format(veces))
    for i in range(0, veces):
        resultado = random.randint(0, 1)
        if resultado == 1:
            CARAS += 1
        elif resultado == 0:
            CRUCES += 1
        resultados.append(resultado)
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
    MSG = "  - Caras: {0} -> Frecuencia Relativa: {1}"
    print(MSG.format(CARAS, CARAS / veces))
    MSG = "  - Cruces: {0} -> Frecuencia Relativa: {1}"
    print(MSG.format(CRUCES, CRUCES / veces))


# %%
def frecuencia_relativa(espacio_muestral, valor, limite=10000):
    """Calcula la probabilidad según una frecuencia relativa."""
    veces_valor = {valor: 0 for valor in espacio_muestral}
    longitud = len(espacio_muestral)
    indice = dict(zip(range(0, longitud), espacio_muestral))
    for _ in range(0, limite):
        aleatorio = random.randint(0, longitud-1)
        valor = indice[aleatorio]
        veces_valor[valor] += 1
    return veces_valor[valor] / limite


NUMEROS = list(range(1, 11))
print("Espacio Muestral: {0}".format(NUMEROS))
PRIORI_5 = frecuencia_relativa(NUMEROS, 5)
print("Priori 5: P(A=5) = {0}".format(PRIORI_5))

PARES = [(a, b) for b in range(1, 11) for a in range(1, 11)]
print("Espacio Muestral: {0}".format(PARES))
PRIORI_5_3 = frecuencia_relativa(PARES, (5, 3))
print("Priori 5 y 3: P(A=5,B=3) = {0}".format(PRIORI_5_3))

ACIERTOS = 0
LIMITE = 10000
for n in range(0, LIMITE):
    resultado = random.randint(1, 10)
    if resultado == 3:
        resultado = random.randint(1, 10)
        if resultado == 5:
            ACIERTOS += 1
print("Simulación de P(A=5,B=3) = {0}".format(ACIERTOS / LIMITE))

print("Posteriori 5 si 3: P(A=5|B=3) = {0}".format(PRIORI_5_3 / PRIORI_5))


# %%
PROB_A = 0.46781
MSG = "Probabilidad de que haya atascos: {0}"
print(MSG.format(PROB_A))

PROB_B = 0.81264
MSG = "Probabilidad de que mañana llueva: {0}"
print(MSG.format(PROB_B))

PROB_A_TRAS_B = 0.98154
MSG = "Probabilidad de que haya atascos después de comenzar a llover: {0}"
print(MSG.format(PROB_A_TRAS_B))

PROB_A_Y_B = PROB_A_TRAS_B * PROB_B
MSG = "Probabilidad de que, a la vez, haya atascos y llueva mañana: {0}"
print(MSG.format(PROB_A_Y_B))
MSG = "Luego, si llueve aumentan las probabilidades de atascos: {0} > {1}"
print(MSG.format(PROB_A_Y_B, PROB_A))

# %%
PROB_5 = 1 / 6
MSG = "Probabilida de sacar un 5 en un dado: {0}"
print(MSG.format(PROB_5))

PROB_3 = 1 / 6
MSG = "Probabilida de sacar un 3 en un dado: {0}"
print(MSG.format(PROB_3))

PROB_3_Y_5 = PROB_3 * PROB_5
MSG = "Probabilidad de sacar un 3 y un 5 a la vez en dos dados: {0}"
print(MSG.format(PROB_3_Y_5))

ESPACIO = [(a, b) for a in range(1, 7) for b in range(1, 7)]
PROB_3_Y_5 = frecuencia_relativa(ESPACIO, (3, 5), 100000)
MSG = "Muy similar al enfoque frecuentista: {0}"
print(MSG.format(PROB_3_Y_5))


# %%
PROB_G = 0.30000
MSG = "Probabilida de tener gripe: {0}"
print(MSG.format(PROB_G))

PROB_NO_G = 1 - PROB_G
MSG = "Probabilidad de NO tener gripe:  {0}"
print(MSG.format(PROB_NO_G))

PROB_F_TRAS_G = 0.60000
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_G))

PROB_F_TRAS_NO_G = 0.07000
MSG = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_NO_G))

PROB_F = (PROB_F_TRAS_G * PROB_G) + (PROB_F_TRAS_NO_G * PROB_NO_G)
MSG = "Probabilidad de tener fibre: {0}"
print(MSG.format(PROB_F))


# %%
PROB_G = 0.30000
MSG = "Probabilida de tener gripe: {0}"
print(MSG.format(PROB_G))

PROB_NO_G = 1 - PROB_G
MSG = "Probabilidad de NO tener gripe:  {0}"
print(MSG.format(PROB_NO_G))

PROB_F_TRAS_G = 0.60000
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_G))

PROB_F_TRAS_NO_G = 0.07000
MSG = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_NO_G))

PROB_NO_F_TRAS_G = 1 - PROB_F_TRAS_G
MSG = "Probabilidad de NO tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_NO_F_TRAS_G))

PROB_NO_F_TRAS_NO_G = 1 - PROB_F_TRAS_NO_G
MSG = "Probabilidad de NO tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_NO_F_TRAS_NO_G))

PROB_F = (PROB_F_TRAS_G * PROB_G) + (PROB_F_TRAS_NO_G * PROB_NO_G)
MSG = "Probabilidad de tener fibre: {0}"
print(MSG.format(PROB_F))

PROB_NO_F = (PROB_NO_F_TRAS_G * PROB_G) + (PROB_NO_F_TRAS_NO_G * PROB_NO_G)
MSG = "Probabilidad de NO tener fibre: {0}"
print(MSG.format(PROB_NO_F))

PROB_G_TRAS_F = (PROB_F_TRAS_G * PROB_G) / PROB_F
MSG = "Probabilidad de tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_F))

PROB_NO_G_TRAS_F = (PROB_F_TRAS_NO_G * PROB_NO_G) / PROB_F
MSG = "Probabilidad de NO tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_F))

PROB_G_TRAS_NO_F = (PROB_NO_F_TRAS_G * PROB_G) / PROB_NO_F
MSG = "Probabilidad de tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_NO_F))

PROB_NO_G_TRAS_NO_F = (PROB_NO_F_TRAS_NO_G * PROB_NO_G) / PROB_NO_F
MSG = "Probabilidad de NO tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_NO_F))


# %%
ALFA_F = 1 / PROB_F
MSG = "Normalización de tener fiebre: {0}"
print(MSG.format(ALFA_F))

ALFA_NO_F = 1 / PROB_NO_F
MSG = "Normalización de NO tener fiebre: {0}"
print(MSG.format(ALFA_NO_F))

PROB_G_TRAS_F = ALFA_F * PROB_F_TRAS_G * PROB_G
MSG = "Probabilidad de tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_F))

PROB_NO_G_TRAS_F = ALFA_F * PROB_F_TRAS_NO_G * PROB_NO_G
MSG = "Probabilidad de NO tener gripe si se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_F))

PROB_G_TRAS_NO_F = ALFA_NO_F * PROB_NO_F_TRAS_G * PROB_G
MSG = "Probabilidad de tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_G_TRAS_NO_F))

PROB_NO_G_TRAS_NO_F = ALFA_NO_F * PROB_NO_F_TRAS_NO_G * PROB_NO_G
MSG = "Probabilidad de NO tener gripe si NO se tiene fiebre: {0}"
print(MSG.format(PROB_NO_G_TRAS_NO_F))
