import InventarioDinamicoInfinito
#Datos
Q=200
c=20
f=1600
h=4
q=75
lam = 0.90
prob_demanda={}
for d in range(30,61):
    prob_demanda[d] = 1/31

r=CostoInmediato(Q,c,f,h,q,prob_demanda)

#Iteracion de Valor
IteracionDeValor(r, prob_demanda, lam, 1e-4)

#Iteracion de Política
IteracionDePolitica(r, prob_demanda, lam)


#Método LP
MetodoLP(r,prob_demanda,lam)
