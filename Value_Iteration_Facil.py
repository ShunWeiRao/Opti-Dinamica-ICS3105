import numpy as np

def politica_call(l):
    V = [0, 0]
    d = [0, 0]
    P0 = 105
    P1 = 110
    C0 = 100
    for i in range(1000):
        V[0] = max(P0 - C0, l*0.5*(V[0] + V[1]))
        V[1] = max(P1 - C0, l*(0.75*V[0] + 0.25*V[1]))

    d0 = [P0 - C0, l*0.5*(V[0] + V[1])]
    d1 = [P1 - C0, l*(0.75*V[0] + 0.25*V[1])]
    return V[0], V[1], d0, d1