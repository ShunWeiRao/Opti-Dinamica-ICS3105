import time
import collections
import numpy as np
from InventarioDinamicoInfinito import normaInfinito,PrintResult

l=0.99
estados = [i for i in range(1,101)]
x = {1:1/10,2:1/5,3:2/5,4:1}

P = collections.defaultdict(dict)

# P = np.zeros((5,100,100))
for accion,p in x.items():
    P[accion] = collections.defaultdict(dict)
    for s in estados:
        for s_prima in estados:
            if s_prima > s:
                P[accion][s][s_prima] = p*(1-p)**(s_prima-s-1)
            elif s_prima == 1:
                P[accion][s][s_prima] = 1 - sum(p*(1-p)**sigma for sigma in range(0,100-s))
            else: P[accion][s][s_prima] = 0

P[1][10]
r = collections.defaultdict(dict)
for accion in x:
    for s in estados:
        if s != 100:
            r[accion][s] = -1
        else: r[accion][s] = 100

V = collections.defaultdict(dict)
d = collections.defaultdict(dict)
for s in estados:
    V[s] = 0
iter = 0
while 1:
    iter += 1
    V_n = V.copy()
    for s in estados:
        V[s] = max(r[accion][s] + l*sum(P[accion][s][j]*V[s] for j in estados) for accion in x)
    if normaInfinito(V_n,V) <= 1e-10 or iter == 10000:
        break

for s in estados:
    d[s] = 1 + np.argmax([r[accion][s] + l*sum(P[accion][s][j]*V[s] for j in estados) for accion in x])

PrintResult(V, d, "VI")
print("Convergencia en {} iteraciones.".format(iter))
