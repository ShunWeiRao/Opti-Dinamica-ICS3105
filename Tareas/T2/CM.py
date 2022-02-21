import DIP

start_time = time.time()
#r(x,y)

def costo_inmediato(t): #recibe la semana y calcula el costo inmediato de esa semana, considerando la demanda del mes
  m = semana_mes[t]
  r = collections.defaultdict(dict)
  probD = meses[m]
  for y in range(0,Q+1):
      for x in range(0,Q-y+1):
          costoInmediato = c*x+f*(1 if x>0 else 0) ##condicion de si se pide o no

          #esperanza de costo de quiebre y holding
          for d in probD.keys():
              costoInmediato += q*max(d-y-x,0)*probD[d]
              costoInmediato += h*max(y+x-d,0)*probD[d]

          r[y][x]=costoInmediato
  return r, probD
#Back DP
C = collections.defaultdict(dict)
xOpt = collections.defaultdict(dict)
#Terminal:
for y in range(0,Q+1):
    C[T+1][y]= 0
#Recursion
for t in reversed(range(1,T+1)):
    r,probD = costo_inmediato(t)

    for y in range(0,Q+1):
        #escoge acción óptima.
        bestC = float('inf')
        bestx = -1
        for x in range(0, Q - y + 1):
            #costo inmediato
            CostoAccion = r[y][x]
            #valor esperado futuro
            for d in probD.keys():
                sfuturo = max(y+x-d,0)
                CostoAccion += C[t+1][sfuturo]* probD[d]

            #Actualiza
            if CostoAccion< bestC:
                bestC=CostoAccion
                bestx=x

        C[t][y]=bestC
        xOpt[t][y]=bestx

#Imprime Valor
print("Política óptima:")
for t in range(1, T+1):
    for y in range(0,Q+1):
        print("t={},y={}:x*={} C*={}".format(t,y, xOpt[t][y], C[t][y]))

print("Tiempo: {} segundos.".format(time.time() - start_time))
