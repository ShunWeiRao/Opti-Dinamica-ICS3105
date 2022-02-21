from T2 import DIP


####heuristica 1####
start_time = time.time()
#Heurística conservadora
xOpt =collections.defaultdict(dict)
def costo(xOpt):
  C = 0
  for i in xOpt:
    C+= c*xOpt[i] + f*(1 if xOpt[i]>0 else 0)
    if i != 52:
      #xOpt[i+1] es la demanda en i
      C+= (200-xOpt[i+1])*h
    else:
      C+= (200-40)*h
  return C


#Iteración
for t in range(1,T+1):
    if t == 1:
      x = Q-30
      xOpt[t] = x
    else:
      mes = semana_mes[t-1]
      u = demanda[mes][0]
      x = 200 - (200-u)
      xOpt[t] = x
print(xOpt)
print(costo(xOpt))

print("Tiempo: {} segundos.".format(time.time() - start_time))



####heuristica 2####
start_time = time.time()
G_miope = collections.defaultdict(dict)
C_miope = collections.defaultdict(dict)
S_miope = {}
s_miope = {}
pi_miope = {}

for t in range(1,T+1):
  m = semana_mes[t]
  probD = meses[m]
  for y in range(Q+1):
      loss = c * y
      for d in probD.keys():
          loss += q*max(d-y,0)*probD[d]
          loss += h*max(y-d,0)*probD[d]
      G_miope[t][y] = loss
  S_miope[t] = (min(G_miope[t], key=G_miope[t].get) if min(G_miope[t], key=G_miope[t].get) > 30 else 30)
  s_miope[t] = max(s for s in range(S_miope[t]) if G_miope[t][s] <= G_miope[t][S_miope[t]] + K)
  C_miope[t] = min(G_miope[t][s] + (K if s > 30 else 0) for s in range(30,Q+1))

# plt.plot(*zip(*G[1].items()),"-o")
# plt.plot(*zip(*G_miope[1].items()),"-o")
"""Para actualizar s pasa algo que no se encuentra valor al lado izq de S tal que sea su G sea mayor a G(S) + K
Por ejemplo min(G[1]) = 810 y no existe el valor en la funcion que supere 1500+810
"""
for t in range(1,T+1):
  pi_miope[t] = (s_miope[t],S_miope[t])
pi_miope

sum(C_miope[t] for t in range(1,T+1))
print("Tiempo: {} segundos.".format(time.time() - start_time))







####heuristica 3####
start_time = time.time()
#Back DP
C =collections.defaultdict(dict)
xOpt =collections.defaultdict(dict)
def costo_inmediato(t): #recibe la semana y calcula el costo inmediato de esa semana, considerando la demanda del mes
  m = semana_mes[t]
  u = demanda[m][0]
  r = collections.defaultdict(dict)
  for s in range(0,Q+1):
      for x in range(0,Q-s+1):
          costoInmediato = c*x+f*(1 if x>0 else 0) ##condicion de si se pide o no
          #esperanza de costo de quiebre y holding
          costoInmediato += q*max(u-s-x,0)
          costoInmediato += h*max(s+x-u,0)

          r[s][x]=costoInmediato
  return r, u
#Terminal:
for s in range(0,Q+1):
    C[T+1][s]= 0
#Recursion
for t in reversed(range(1,T+1)):
    r, u = costo_inmediato(t)
    for s in range(0,Q+1):
        #escoge acción óptima.
        bestC = float('inf')
        bestx = -1
        for x in range(0, Q - s + 1):
            #costo inmediato
            CostoAccion = r[s][x]
            #valor esperado futuro
            sfuturo = max(s+x-u,0)
            CostoAccion += C[t+1][sfuturo]

            #Actualiza
            if CostoAccion< bestC:
                bestC=CostoAccion
                bestx=x

        C[t][s]=bestC
        xOpt[t][s]=bestx
#Imprime Valor
print("Política óptima:")
for t in range(1, 2):
    for s in range(0,Q+1):
        print("t={},s={}:x*={} C*={}".format(t,s, xOpt[t][s], C[t][s]))
print("Tiempo: {} segundos.".format(time.time() - start_time))
