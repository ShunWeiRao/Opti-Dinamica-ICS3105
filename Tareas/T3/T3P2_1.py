import time
import collections
import gurobipy as gp
from gurobipy import GRB

def ValorInmediato(Q:dict):
    r = collections.defaultdict(dict)
    dec = ['a', 'b']
    for s in range(0, Q + 1):
        for x in dec:
            temp = 0
            #ganancia 1 y 2
            if s!= 2:
                if x == 'a':
                    temp += 1

                else:
                    temp += 2
            #ganancia 0
            else:
                temp += 0

            r[s][x] = temp
    return r
def normaInfinito(X:dict,Y:dict):
    maxDiff=0.0;
    for key in X.keys():
        diff = abs(X[key]-Y[key])
        if diff>maxDiff:
            maxDiff=diff

    return maxDiff
def PrintResult(C:dict,X:dict,metodo:str):
    print("Resultado para: " + metodo)
    print("Política óptima:")
    for s in C.keys():
        print("s={}: X*={} C*={}".format(s, X[s], C[s]))
def getPoliticaDesdeCosto(C:dict):
    X = collections.defaultdict(dict)
    Q = max(C.keys())
    dec = ['a', 'b']
    for s in C.keys():
        best = 0
        for x in dec:
            #costo inmediato + valor esperado futuro
            CostoAccion = r[s][x]
            if s == 0 and x == 'a':
                CostoAccion += lam * C[0]
            elif s == 0 and x == 'b':
                CostoAccion += (5*lam*C[0]+5*lam*C[1])/10
            elif s == 1 and x == 'a':
                CostoAccion += (5*lam*C[0]+5*lam*C[1])/10
            elif s == 1 and x == 'b':
                CostoAccion += (5*lam*C[1]+5*lam*C[2])/10
            else:
                CostoAccion += lam*C[2]
            # Actualiza
            if CostoAccion > best:
                best = CostoAccion
                X[s] = x
    return X
def getCostoDesdePolitica(X:dict):
    precisionEvaluacion=1e-10
    C_x = collections.defaultdict(dict)
    for s in X.keys(): C_x[s] = 0
    while 1:
        C_xOld=C_x.copy()
        for s in X.keys():
            CostoAccion = r[s][X[s]]

            if s == 0 and X[s] == 'a':
                CostoAccion += lam * C_xOld[0]
            elif s == 0 and X[s] == 'b':
                CostoAccion += (5*lam*C_xOld[0]+5*lam*C_xOld[1])/10
            elif s == 1 and X[s] == 'a':
                CostoAccion += (5*lam*C_xOld[0]+5*lam*C_xOld[1])/10
            elif s == 1 and X[s] == 'b':
                CostoAccion += (5*lam*C_xOld[1]+5*lam*C_xOld[2])/10
            else:
                CostoAccion += lam*C_xOld[2]
            C_x[s] = CostoAccion

        if normaInfinito(C_x,C_xOld)< precisionEvaluacion:
            return C_x
def IteracionDeValor(r:dict, lam, precisionIdeV):
    dec = ['a', 'b']
    Q=max(r.keys())
    start_time = time.time()
    #Iteración de Valor
    C = collections.defaultdict(dict)
    for s in r.keys():C[s]= 0 #valor inicial (puede ser cualquiera)
    iter=0
    while 1:
        iter+=1
        C_old=C.copy()
        for s in r.keys():
            C[s] = 0
            for x in dec:
                #costo inmediato + valor esperado futuro
                CostoAccion = r[s][x]
                if s == 0 and x == 'a':
                    CostoAccion += lam * C_old[0]
                elif s == 0 and x == 'b':
                    CostoAccion += (5*lam*C_old[0]+5*lam*C_old[1])/10
                elif s == 1 and x == 'a':
                    CostoAccion += (5*lam*C_old[0]+5*lam*C_old[1])/10
                elif s == 1 and x == 'b':
                    CostoAccion += (5*lam*C_old[1]+5*lam*C_old[2])/10
                else:
                    CostoAccion += lam*C_old[2]
                #Actualiza
                if CostoAccion > C[s]:
                    C[s]=CostoAccion

        if normaInfinito(C,C_old)<precisionIdeV*(1-lam)/2/lam: break

    #Obteción de política epsilon óptima
    X = getPoliticaDesdeCosto(C)

    #Imprime Valor
    PrintResult(C, X, "Value Iteration")

    print("Tiempo: {} segundos.".format(time.time() - start_time))
    print("Convergencia en {} iteraciones.".format(iter))
    print()
def IteracionDePolitica(r:dict, lam):
    dec = ['a', 'b']
    Q=max(r.keys())
    start_time = time.time()
    # Iteracion de Política
    X = collections.defaultdict(dict)
    for s in r.keys(): X[s] = 'a'  # opolítica inicial (puede ser cualquiera)
    iter = 0
    while 1:
        iter += 1
        C = getCostoDesdePolitica(X)
        X_old = X.copy()

        # Obteción de nueva política
        for s in r.keys():
            bestC = C[s]
            bestX = X_old[s]
            for x in dec:
                #costo inmediato + valor esperado futuro
                CostoAccion = r[s][x]
                if s == 0 and x == 'a':
                    CostoAccion += lam * C[0]
                elif s == 0 and x == 'b':
                    CostoAccion += (5*lam*C[0]+5*lam*C[1])/10
                elif s == 1 and x == 'a':
                    CostoAccion += (5*lam*C[0]+5*lam*C[1])/10
                elif s == 1 and x == 'b':
                    CostoAccion += (5*lam*C[1]+5*lam*C[2])/10
                else:
                    CostoAccion += lam*C[2]
                    # Actualiza

                if CostoAccion > bestC:
                    bestC = CostoAccion
                    bestX = x
            X[s] = bestX
        if (X[0] == X_old[0]) and (X[1] == X_old[1]) and (X[2] == X_old[2]): break

    PrintResult(C, X,"Policy Iteration")
    print("Tiempo: {} segundos.".format(time.time() - start_time))
    print("Convergencia en {} iteraciones.".format(iter))


#Datos
Q=2
lam = 0.8

r=ValorInmediato(Q)


#Iteracion de Valor
IteracionDeValor(r, lam, 1e-8)

#Iteracion de Política
IteracionDePolitica(r, lam)
