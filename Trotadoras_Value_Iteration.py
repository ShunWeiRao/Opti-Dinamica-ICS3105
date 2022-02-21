import collections
import numpy as np

Estados = [0,1,2,3,4]
Acciones =[0,1]
l = 0.97

#P[accion][s][s_prima]
P = collections.defaultdict(dict)
for i in Acciones:
    P[i] = np.zeros((5,5))

P[0][0][0] = 0.23
P[0][0][1] = 0.5
P[0][0][2] = 0.15
P[0][0][3] = 0.1
P[0][0][4] = 0.02

P[0][1][1] = 0.25
P[0][1][2] = 0.50
P[0][1][3] = 0.20
P[0][1][4] = 0.05

P[0][2][2] = 0.30
P[0][2][3] = 0.50
P[0][2][4] = 0.20

P[0][3][3] = 0.70
P[0][3][4] = 0.30

P[0][4][4] = 1

P[1][0][0] = 1
P[1][1][0] = 1
P[1][2][0] = 1
P[1][3][0] = 1
P[1][4][0] = 1

K = [200, 200, 150, 100, 0]
G = [150, 150, 200, 400, 2500]
V = collections.defaultdict(dict)
d = collections.defaultdict(dict)
for s in Estados:
    V[s] = 0
iter = 0
while 1:
    iter += 1
    V_n = V.copy()
    for s in Estados:
        V[s] = max(K[s] - x*G[s] + l*sum(P[x][s][j]*V[s] for j in Estados) for x in Acciones)
    if sum((V[s] - V_n[s])**2 for s in Estados) < 1e-5 or iter >1000:
        break

for s in Estados:
        d[s] = np.argmax(K[s] - x*G[s] + l*sum(P[x][s][j]*V[s] for j in Estados) for x in Acciones)

print(d, V)