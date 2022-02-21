import time
import collections
import sys

T= 3
Q =3
c=2
f=4
h=1
q=15

# Demanda: Probab
probD={0:0.25,1:0.5,2:0.25}

start_time = time.time()
#r(x,s)
r = collections.defaultdict(dict)
for s in range(0,Q+1):
    for x in range(0,Q-s+1):
        costoInmediato = c*x+f*(1 if x>0 else 0)

        #esperanza de costo de quiebre y holding
        for d in probD.keys():
            costoInmediato += q*max(d-s-x,0)*probD[d]
            costoInmediato += h*max(s+x-d,0) * probD[d]

        r[s][x]=costoInmediato

# print("Costos Inmediatos:")
# for s in range(0,Q+1):
#     for x in range(0,Q-s+1):
#         print("s={},x={}: r={}".format(s,x,r[s][x]))

#Back DP
C =collections.defaultdict(dict)
xOpt =collections.defaultdict(dict)
#Terminal:
for s in range(0,Q+1):
    C[T+1][s]= 0
#Recursion
for t in reversed(range(1,T+1)):
    for s in range(0,Q+1):
        #escoge acción óptima.
        bestC = float('inf')
        bestx = -1
        for x in range(0, Q - s + 1):
            #costo inmediato
            CostoAccion = r[s][x]
            #valor esperado futuro
            for d in probD.keys():
                sfuturo = max(s+x-d,0)
                CostoAccion += C[t+1][sfuturo]* probD[d]

            #Actualiza
            if CostoAccion< bestC:
                bestC=CostoAccion
                bestx=x

        C[t][s]=bestC
        xOpt[t][s]=bestx

#Imprime Valor
print("Política óptima:")
for t in range(1, T + 1):
    for s in range(0,Q+1):
        print("t={},s={}:x*={} C*={}".format(t,s, xOpt[t][s], C[t][s]))

print("Tiempo: {} segundos.".format(time.time() - start_time))