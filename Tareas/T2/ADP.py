from T2.MDP import pi
import random

#M escenarios
M = 1000

random.seed(10)
escenario = collections.defaultdict(dict)
for m in range(1,M+1):
  for t in range(1,T+1):
    mes = semana_mes[t]
    u = demanda[mes][0]
    d = demanda[mes][1]
    dem = random.randint(u-d,u+d)
    escenario[m][t] = dem
# print(escenario[1])
y = {}
y[1] = 30

""""oli aqui intento hacer el problema deterministico conociendo la demanda"""
# G = collections.defaultdict(dict)
# costo = collections.defaultdict(dict)
# inventario = {}
# inventario[0] = 30
# for t in range(1,T+1):
#   for s in range(Q+1):
#     G[t][s] = q*(max(escenario[1][t] - s + inventario[t-1], 0)) + h*(max(s + inventario[t-1] - escenario[1][t], 0))
#   inventario[t] = inventario[t-1] - escenario[1][t] + min(G[t], key=G[t].get)
#   costo[1][t] = min(c*y + G[t][y] for y in range(Q+1))
#
#

# r = collections.defaultdict(dict)
# for t in range(1,2):
#   for s in range(Q+1):
#     r[t][s] = K*(1 if s > y[t] else 0) + c*(s - y[t] if s >= y[t] else 0)
#     r[t][s] += q*(max(escenario[1][t] - s, 0)) + h*(max(s - escenario[1][t], 0))
#
# plt.plot(*zip(*r[1].items()),"-o")
#
#
#
# m = Model("")
#
# y_prima = m.addVars(T,lb=0, vtype=GRB.INTEGER)
# y = m.addVars(T, lb=0, vtype=GRB.INTEGER)
#
# m.setObjective(quicksum(c*(y_prima[t] - y[t])\
#  +  q*max_(escenario[1][t+1] - y_prima[t+1], 0) + h*max_(y_prima[t] - escenario[1][t+1], 0) for t in range(T)), GRB.MINIMIZE)
#
#
#  # K*(1 if y_prima[t] > y[t] else 0) +
# m.addConstrs(y_prima[t] >= y[t] for t in range(T))
# m.addConstrs(y[t+1] == y_prima[t] - escenario[1][t+1] for t in range(T-1))
#
# m.optimize()


y = collections.defaultdict(dict)
y_prima = collections.defaultdict(dict)
C = collections.defaultdict(dict)

for sc in range(1,M+1):
  y[sc][1] = 30
  for t in range(1,T+1):
    if y[sc][t] < pi[t][0]:
      y_prima[sc][t] = pi[t][1] - y[sc][t]
    else:
      y_prima[sc][t] = y[sc][t]
    y[sc][t+1] = max(y_prima[sc][t] - escenario[sc][t],0)
    C[sc][t] = K*(1 if y_prima[sc][t] > y[sc][t] else 0) + c*(y_prima[sc][t] - y[sc][t])
    C[sc][t] += q*max(escenario[sc][t] - y_prima[sc][t], 0) + h*max(y_prima[sc][t] - escenario[sc][t], 0)

# plt.plot(*zip(*C[1].items()))

C_total = {}
for sc in range(1,M+1):
  C_total[sc] = sum(C[sc][t] for t in range(1,T+1))

C_prom = sum(C_total.values())/M

plt.hist(C_total.values(), bins=20, alpha=0.3, color="yellow", edgecolor="green")
plt.text(C_prom, M/10, r"$\bar{x}$")
plt.xlabel('Costo Total [USD]')
plt.ylabel('Frecuencia')
plt.title('Simulación')
# plt.savefig("fig.png", dpi=1200)
plt.show()
