#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de las bases de la probabilidad que luego se usarán en las redes
bayesianas.
"""
import random


# %% --- AXIOMAS DE KOLGOMOROV ---

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
prob_A = 0.78612567
msg = "Probablidad de que llueva mañana: {0}"
print(msg.format(prob_A))

# Probabilidad de que NO llueva mañana.
prob_B = 1.0 - prob_A
msg = "Probablidad de que NO llueva mañana: {0}"
print(msg.format(prob_B))

# Otra propiedad importante del tercer axioma es que si dos evento son
# excluyentes entre sí (no pueden darse a la vez), entonces P(A y B) = 0, ya
# que P(A o B) = P(A) + P(B)
print()

# Probabilidad de que salga un 1 en un dado.
prob_1 = 1 / 6
msg = "Probabilidad de que salga un 1 en un dado: {0}"
print(msg.format(prob_1))

# Probabilidad de que salga un 5 en un dado.
prob_5 = 1 / 6
msg = "Probabilidad de que salga un 5 en un dado: {0}"
print(msg.format(prob_5))

# No puede salir un 1 y un 5 a la vez en un dado: P(A=1,A=5) = 0
msg = "Probabilidad de que salga un 1 o un 5 en un dado: {0}"
prob_1_o_5 = prob_1 + prob_5
print(msg.format(prob_1_o_5))

# Probabilidad de que salga un 3 en un dado.
prob_3 = 1 / 6
msg = "Probabilidad de que salga un 3 en un dado: {0}"
print(msg.format(prob_3))

# No puede salir un 1, un 3 o un 5 a la vez en un dado: P(A=1,A=5,A=3) = 0
msg = "Probabilidad de que salga un 1, un 3 o un 5 en un dado: {0}"
prob_1_o_3_o_5 = prob_1 + prob_3 + prob_5
print(msg.format(prob_1_o_3_o_5))


# %% --- DEFINICIONES ---

# Un experimento puede ser sacar un número entero aleatorio entre 1 y 10.
# El espacio muestral son todos los números enteros que hay entre 1 y 10.
# Un evento simple es sacar una vez un número aleatorio:
evento = random.randint(1, 10)
print("***************")
print("*** EVENTOS ***")
print("***************")
print()
print("--- Evento Simple ---")
msg = "1 nº aleatorio entre 1 y 10: {0}"
print(msg.format(evento))

# En este caso, la probabilidad de que salga cualquier número es la misma,
# por lo que se dice que son "equiprobables".
print("Probabilidad: 1/10 para todos (equiprobable)")
print()

# Un evento múltiple es sacar varios números aleatorios:
evento_1 = random.randint(1, 10)
evento_2 = random.randint(1, 10)
evento_3 = random.randint(1, 10)
print("--- Evento Múltiple ---")
msg = "3 nº aleatorios entre 0 y 10: ({0}, {1}, {2})"
print(msg.format(evento_1, evento_2, evento_3))
print("Probabilidad de 3 unos: (1/10)·(1/10)·(1/10) = 1/1000")
print()

# %% --- FRECUENCIA RELATIVA ---
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
limites = [10, 100, 1000, 10000, 100000, 1000000]

for veces in limites:
    # Guardará la lista de resultados de lanzar una moneda varias veces.
    resultados = []

    # Contabilizará el número de veces que sale cada resultado.
    caras = 0
    cruces = 0

    # Lanzamos la moneda varias veces.
    print("Lanzamos la moneda {0} veces:".format(veces))
    for i in range(0, veces):
        # Lanzamos la moneda.
        resultado = random.randint(0, 1)

        # Aumentamos las caras o las cruces según el resultado.
        if resultado == 1:
            caras += 1
        elif resultado == 0:
            cruces += 1

        # Agregamos el resultado a la lista de resultados.
        resultados.append(resultado)

    # Moramos los resultado obtenidos.
    msg = "Resultados: [{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, ...]"
    ejemplos = resultados[:8]
    print(msg.format(ejemplos[0],
                     ejemplos[1],
                     ejemplos[2],
                     ejemplos[3],
                     ejemplos[4],
                     ejemplos[5],
                     ejemplos[6],
                     ejemplos[7]))

    # Mostramos las frecuencias relativas
    msg = "  - Caras: {0} -> Frecuencia Relativa: {1}"
    print(msg.format(caras, caras / veces))
    msg = "  - Cruces: {0} -> Frecuencia Relativa: {1}"
    print(msg.format(cruces, cruces / veces))
    print()


# %% --- PROBABILIDAD A POSTERIORI ---

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
    resultados = {valor: 0 for valor in espacio_muestral}

    # Asociamos un número con cada resultado.
    longitud = len(espacio_muestral)
    indice = dict(zip(range(0, longitud), espacio_muestral))

    # Repetimos varias veces el experimento.
    for i in range(0, limite):
        # Ejecutamos el experimiento.
        resultado = random.randint(0, longitud-1)

        # Aumentamos el contador el resultado.
        valor = indice[resultado]
        resultados[valor] += 1

    # Devolvemos la frecuencia relativa del solicituda.
    return resultados[valor] / limite


# Definimos el espacio muestral: números enteros entre 1 y 10.
print("---- P(A) ----")
numeros = list(range(1, 11))
print("Espacio Muestral: {0}".format(numeros))

# Probabilidad a priori de que salga un 5: P(A=5)
priori_5 = frecuencia_relativa(espacio_muestral=numeros,
                               valor=5)
print("Priori 5: P(A=5) = {0}".format(priori_5))
print()

# Probabilidad a priori de que salga un 5 y un 3: P(A=5,B=3)
print("--- P(A,B) ---")
pares = [(a, b)
         for b in range(1, 11)
         for a in range(1, 11)]
print("Espacio Muestral: {0}".format(pares))

# Probabilidad a priori de que salga un 5: P(A=5)
priori_5_3 = frecuencia_relativa(espacio_muestral=pares,
                                 valor=(5, 3))
print("Priori 5 y 3: P(A=5,B=3) = {0}".format(priori_5_3))

# Vamos a simularlo para ver si da similar.
aciertos = 0
limite = 10000
for n in range(0, limite):
    resultado = random.randint(1, 10)
    if resultado == 3:
        resultado = random.randint(1, 10)
        if resultado == 5:
            aciertos += 1
print("Simulación de P(A=5,B=3) = {0}".format(aciertos / limite))
print()

# Probabilidad a posteriori: P(A=5|B=3)
print("--- P(A|B) = P(A,B) / P(A) ---")
print("Posteriori 5 si 3: P(A=5|B=3) = {0}".format(priori_5_3 / priori_5))
print()


# %% --- REGLA DEL PRODUCTO / MULTIPLICACIÓN ---

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
prob_a = 0.46781
msg = "Probabilidad de que haya atascos: {0}"
print(msg.format(prob_a))

# Probabilidad de que mañana llueva: P(A)
prob_b = 0.81264
msg = "Probabilidad de que mañana llueva: {0}"
print(msg.format(prob_b))

# Probabilidad de que haya atascos después de comenzar a llover: p(B|A)
prob_a_tras_b = 0.98154
msg = "Probabilidad de que haya atascos después de comenzar a llover: {0}"
print(msg.format(prob_a_tras_b))

# Probabilidad de que, a la vez, haya atascos y llueva mañana: P(A,B)
prob_a_y_b = prob_a_tras_b * prob_b
msg = "Probabilidad de que, a la vez, haya atascos y llueva mañana: {0}"
print(msg.format(prob_a_y_b))
msg = "Luego, si llueve aumentan las probabilidades de atascos: {0} > {1}"
print(msg.format(prob_a_y_b, prob_a))
print()

# Donde hay que tener en cuenta que, si dos sucesos A y B son independientes
# entre sí: P(A|B) = P(A), es decir, B no afecta para nada a B.
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

# Debe ser muy similiar si lo hacemos por el enfoque frecuentista.
espacio = [(a, b) for a in range(1, 7) for b in range(1, 7)]
prob_3_y_5 = frecuencia_relativa(espacio_muestral=espacio,
                                 valor=(3, 5),
                                 limite=100000)
msg = "Muy similar al enfoque frecuentista: {0}"
print(msg.format(prob_3_y_5))
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


# %% --- PROBABILIDAD TOTAL / MARGINAL ---

# Se puede calcular la probabilidad de un evento a partir de las probabilidades
# conjuntas con el resto de variables, siempre y cuando el resto de variables
# sean todas independientes entre sí y exhaustivas es:
# P(B) = sum(P(Ai,B)) = sum(P(B|Ai)·P(Ai))
# Donde Ai son el resto de variables. Para el caso de 2 variables boolenas:
# P(B) = P(B|A)·P(A) + P(B|¬A)·P(¬A)
print("***********************************")
print("*** PROBABILIDAD TOTAL/MARGINAL ***")
print("***********************************")
print()

# Probabilida de tener gripe: P(G)
prob_g = 0.30000
msg = "Probabilida de tener gripe: {0}"
print(msg.format(prob_g))

# Probabilidad de NO tener gripe: P(¬G)
prob_no_g = 1 - prob_g
msg = "Probabilidad de NO tener gripe:  {0}"
print(msg.format(prob_no_g))

# Probabilidad de tener fiebre si se tiene gripe: P(F|G)
prob_f_tras_g = 0.60000
msg = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(msg.format(prob_f_tras_g))

# Probabilidad de tener fiebre cuanto NO se tiene gripe: P(F|¬G)
prob_f_tras_no_g = 0.07000
msg = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(msg.format(prob_f_tras_no_g))

# Probabilidad de tener fibre: P(F) = P(F|G)·P(G) + P(F|¬G)·P(¬G)
proba_f = (prob_f_tras_g * prob_g) + (prob_f_tras_no_g * prob_no_g)
msg = "Probabilidad de tener fibre: {0}"
print(msg.format(proba_f))


# %% --- REGLA DE BAYES ---

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
prob_g = 0.30000
msg = "Probabilida de tener gripe: {0}"
print(msg.format(prob_g))

# Probabilidad de NO tener gripe: P(¬G)
prob_no_g = 1 - prob_g
msg = "Probabilidad de NO tener gripe:  {0}"
print(msg.format(prob_no_g))
print()

# Probabilidad de tener fiebre si se tiene gripe: P(F|G)
prob_f_tras_g = 0.60000
msg = "Probabilidad de tener fiebre si se tiene gripe: {0}"
print(msg.format(prob_f_tras_g))

# Probabilidad de tener fiebre cuanto NO se tiene gripe: P(F|¬G)
prob_f_tras_no_g = 0.07000
msg = "Probabilidad de tener fiebre cuanto NO se tiene gripe: {0}"
print(msg.format(prob_f_tras_no_g))

# Probabilidad de NO tener fiebre si se tiene gripe: P(¬F|G)
prob_no_f_tras_g = 1 - prob_f_tras_g
msg = "Probabilidad de NO tener fiebre si se tiene gripe: {0}"
print(msg.format(prob_no_f_tras_g))

# Probabilidad de NO tener fiebre cuanto NO se tiene gripe: P(¬F|¬G)
prob_no_f_tras_no_g = 1 - prob_f_tras_no_g
msg = "Probabilidad de NO tener fiebre cuanto NO se tiene gripe: {0}"
print(msg.format(prob_no_f_tras_no_g))
print()

# Probabilidad de tener fibre: P(F) = P(F|G)·P(G) + P(F|¬G)·P(¬G)
prob_f = (prob_f_tras_g * prob_g) + (prob_f_tras_no_g * prob_no_g)
msg = "Probabilidad de tener fibre: {0}"
print(msg.format(prob_f))

# Probabilidad de NO tener fibre: P(¬F) = P(¬F|G)·P(G) + P(¬F|¬G)·P(¬G)
prob_no_f = (prob_no_f_tras_g * prob_g) + (prob_no_f_tras_no_g * prob_no_g)
msg = "Probabilidad de NO tener fibre: {0}"
print(msg.format(prob_no_f))
print()

# Probabilidad de tener gripe si se tiene fiebre:
# P(G|F) = P(F|G)·P(G) / P(F)
prob_g_tras_f = (prob_f_tras_g * prob_g) / prob_f
msg = "Probabilidad de tener gripe si se tiene fiebre: {0}"
print(msg.format(prob_g_tras_f))

# Probabilidad de NO tener gripe si se tiene fiebre:
# P(¬G|F) = P(F|¬G)·P(¬G) / P(F)
prob_no_g_tras_f = (prob_f_tras_no_g * prob_no_g) / prob_f
msg = "Probabilidad de NO tener gripe si se tiene fiebre: {0}"
print(msg.format(prob_no_g_tras_f))

# Probabilidad de tener gripe si NO se tiene fiebre:
# P(G|¬F) = P(¬F|G)·P(G) / P(¬F)
prob_g_tras_no_f = (prob_no_f_tras_g * prob_g) / prob_no_f
msg = "Probabilidad de tener gripe si NO se tiene fiebre: {0}"
print(msg.format(prob_g_tras_no_f))

# Probabilidad de NO tener gripe si NO se tiene fiebre:
# P(¬G|¬F) = P(¬F|¬G)·P(¬G) / P(¬F)
prob_no_g_tras_no_f = (prob_no_f_tras_no_g * prob_no_g) / prob_no_f
msg = "Probabilidad de NO tener gripe si NO se tiene fiebre: {0}"
print(msg.format(prob_no_g_tras_no_f))
print()


# %% --- NORMALIZACION ---

# Para no repetir tantos cálculos, se puede usar la normalización 'alfa':
# alfa = 1 / P(B) = 1 / sum(P(B|Ai)·P(Ai)) => P(A|B) = alfa·P(B|A)·P(B)
print("****************************")
print("*** NORMALIZACIÓN (ALFA) ***")
print("****************************")
print()

# Normalización de tener fiebre:
# 1 / P(F) = 1 / [P(F|G)·P(G) + P(F|¬G)·P(¬G)]
alfa_f = 1 / prob_f
msg = "Normalización de tener fiebre: {0}"
print(msg.format(alfa_f))

# Normalización de NO tener fiebre:
# 1 / P(¬F) = 1 / [P(¬F|G)·P(G) + P(¬F|¬G)·P(¬G)]
alfa_no_f = 1 / prob_no_f
msg = "Normalización de NO tener fiebre: {0}"
print(msg.format(alfa_no_f))
print()

# Probabilidad de tener gripe si se tiene fiebre:
# P(G|F) = alfaF·P(F|G)·P(G)
prob_g_tras_f = alfa_f * prob_f_tras_g * prob_g
msg = "Probabilidad de tener gripe si se tiene fiebre: {0}"
print(msg.format(prob_g_tras_f))

# Probabilidad de NO tener gripe si se tiene fiebre:
# P(¬G|F) = alfaF·P(F|¬G)·P(¬G)
prob_no_g_tras_f = alfa_f * prob_f_tras_no_g * prob_no_g
msg = "Probabilidad de NO tener gripe si se tiene fiebre: {0}"
print(msg.format(prob_no_g_tras_f))

# Probabilidad de tener gripe si NO se tiene fiebre:
# P(G|¬F) = alfa¬F·P(¬F|G)·P(G)
prob_g_tras_no_f = alfa_no_f * prob_no_f_tras_g * prob_g
msg = "Probabilidad de tener gripe si NO se tiene fiebre: {0}"
print(msg.format(prob_g_tras_no_f))

# Probabilidad de NO tener gripe si NO se tiene fiebre:
# P(¬G|¬F) = alfa¬F·P(¬F|¬G)·P(¬G)
prob_no_g_tras_no_f = alfa_no_f * prob_no_f_tras_no_g * prob_no_g
msg = "Probabilidad de NO tener gripe si NO se tiene fiebre: {0}"
print(msg.format(prob_no_g_tras_no_f))
print()


# %% --- PROPIEDADES ÚTILES ---

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
