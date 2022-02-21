import time
import collections
import gurobipy as gp
from gurobipy import GRB



def CostoInmediato(Q:dict,c,f,h,q:dict,demanda:dict):
    r = collections.defaultdict(dict)
    for s in range(0, Q + 1):
        for x in range(0, Q - s + 1):
            #costo de ordenar
            temp = c * x + f * (1 if x > 0 else 0)
            # esperanza de costo de quiebre y holding
            for d in demanda.keys():
                temp += q * max(d - s - x, 0) * demanda[d] + h * max(s + x - d, 0) * demanda[d]

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
def getPoliticaDesdeCosto(C:dict, prob_demanda:dict):
    X = collections.defaultdict(dict)
    Q = max(C.keys())
    for s in C.keys():
        best = float('inf')
        for x in range(0, Q - s + 1):
            CostoAccion = r[s][x]
            for d in prob_demanda.keys():
                CostoAccion += lam * C[max(s + x - d, 0)] * prob_demanda[d]
            # Actualiza
            if CostoAccion < best:
                best = CostoAccion
                X[s] = x
    return X
def getCostoDesdePolitica(X:dict,demanda:dict):
    precisionEvaluacion=1e-6
    C_x = collections.defaultdict(dict)
    for s in X.keys(): C_x[s] = 0
    while 1:
        C_xOld=C_x.copy()
        for s in X.keys():
            CostoAccion = r[s][X[s]]
            for d in demanda.keys():
                CostoAccion += lam * C_xOld[max(s +X[s] - d, 0)] * demanda[d]
            C_x[s] = CostoAccion

        if normaInfinito(C_x,C_xOld)< precisionEvaluacion:
            return C_x
def IteracionDeValor(r:dict, prob_demanda:dict, lam, precisionIdeV):

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
            C[s] = float('inf')
            for x in range(0, Q - s + 1):
                #costo inmediato + valor esperado futuro
                CostoAccion = r[s][x]
                for d in prob_demanda.keys():
                    CostoAccion += lam * C_old[max(s+x-d,0)] * prob_demanda[d]
                #Actualiza
                if CostoAccion< C[s]:
                    C[s]=CostoAccion

        if normaInfinito(C,C_old)<precisionIdeV*(1-lam)/2/lam: break

    #Obteción de política epsilon óptima
    X = getPoliticaDesdeCosto(C, prob_demanda)

    #Imprime Valor
    PrintResult(C, X, "Value Iteration")

    print("Tiempo: {} segundos.".format(time.time() - start_time))
    print("Convergencia en {} iteraciones.".format(iter))
    print()
def IteracionDePolitica(r:dict, prob_demanda:dict, lam):
    Q=max(r.keys())
    start_time = time.time()
    # Iteracion de Política
    X = collections.defaultdict(dict)
    for s in r.keys(): X[s] = 0  # opolítica inicial (puede ser cualquiera)
    iter = 0
    while 1:
        iter += 1
        C = getCostoDesdePolitica(X, prob_demanda)
        X_old = X.copy()

        # Obteción de nueva política
        for s in r.keys():
            bestC = C[s]
            bestX = X_old[s]

            for x in range(0, Q - s + 1):
                CostoAccion = r[s][x]
                for d in prob_demanda.keys():
                    CostoAccion += lam * C[max(s + x - d, 0)] * prob_demanda[d]
                # Actualiza
                if CostoAccion < bestC:
                    bestC = CostoAccion
                    bestX = x

            X[s] = bestX

        if normaInfinito(X, X_old) == 0: break

    PrintResult(C, X,"Policy Iteration")
    print("Tiempo: {} segundos.".format(time.time() - start_time))
    print("Convergencia en {} iteraciones.".format(iter))
def MetodoLP(r:dict,prob_demanda:dict,lam):
    start_time = time.time()

    # Modelo LP
    m = gp.Model('LP')
    m.Params.LogToConsole = 0
    Cvar = m.addVars(r.keys(), lb=0, ub=10000000, name="C")
    m.setObjective(gp.quicksum(Cvar), GRB.MAXIMIZE)
    m.update()
    for s in r.keys():
        for x in r[s].keys():
            temp = gp.LinExpr()
            for d in prob_demanda.keys():
                temp.add(Cvar[max(s + x - d, 0)], -1 * lam * prob_demanda[d])
            m.addConstr(Cvar[s] + temp <= r[s][x])

    m.optimize()
    if m.status == GRB.OPTIMAL:

        C = m.getAttr('x', Cvar)
        X = getPoliticaDesdeCosto(C, prob_demanda)

        PrintResult(C, X,"LP Method")
        print("Tiempo: {} segundos.".format(time.time() - start_time))
    else:
        print('Error resolviendo gurobi')


#Datos
Q=5
c=2
f=4
h=1
q=15
lam = 0.9
prob_demanda={0:0.05, 1:0.2, 2:0.4, 3:0.2, 4:0.15}

r=CostoInmediato(Q,c,f,h,q,prob_demanda)

#Iteracion de Valor
IteracionDeValor(r, prob_demanda, lam, 1e-8)

#Iteracion de Política
IteracionDePolitica(r, prob_demanda, lam)

#Método LP
MetodoLP(r,prob_demanda,lam)

