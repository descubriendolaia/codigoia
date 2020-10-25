#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de Inferencia en Probabilidad.

Curso del canal de Youtube 'Descubriendo la Inteligencia Artificial'.
Autor: JL Iglesias Feria (jl.iglesias.feria@gmail.com)
"""


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


# %%
P_FIEBRE_TRAS_GRIPE = 0.89231
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(P_FIEBRE_TRAS_GRIPE))

P_GARGANTA_TRAS_GRIPE = 0.94213
MSG = "Probabilidad de tener dolor de garganta si se tiene gripe: {0}"
print(MSG.format(P_GARGANTA_TRAS_GRIPE))

P_FIEBRE_GARGANTA_TRAS_GRIPE = P_FIEBRE_TRAS_GRIPE * P_GARGANTA_TRAS_GRIPE
MSG = "Probabilidad de tener ambos si se tiene gripe: {0}"
print(MSG.format(P_FIEBRE_GARGANTA_TRAS_GRIPE))


# %%
PROB_G = 0.30000
PROB_NO_G = 1 - 0.30000
MSG = "Probabilida de tener gripe: {0}"
print(MSG.format(PROB_G))
MSG = "Probabilida de NO tener gripe: {0}"
print(MSG.format(PROB_NO_G))

PROB_F_TRAS_G = 0.60000
MSG = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_G))

PROB_F_TRAS_NO_G = 0.07000
MSG = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_F_TRAS_NO_G))

PROB_D_TRAS_G = 0.80000
MSG = "Probabilidad de tener dolor de garganta si se tiene gripe: {0}"
print(MSG.format(PROB_D_TRAS_G))

PROB_D_TRAS_NO_G = 0.10000
MSG = "Probabilidad de tener dolor de garganta cuanto NO se tiene gripe: {0}"
print(MSG.format(PROB_D_TRAS_NO_G))

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

PROB_G_TRAS_F_Y_D = ALFA * PROB_F_TRAS_G * PROB_D_TRAS_G * PROB_G
MSG = "Probabilidad de tener gripe si se tiene fiebre y dolor de garganta: {0}"
print(MSG.format(PROB_G_TRAS_F_Y_D))
