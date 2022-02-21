import collections
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

demanda = {}
demanda[1] = (20,4)
demanda[2] = (18,8)
demanda[3] = (30,5)
demanda[4] = (32,7)
demanda[5] = (17,5)
demanda[6] = (18,8)
demanda[7] = (25,7)
demanda[8] = (19,10)
demanda[9] = (18,6)
demanda[10] = (15,2)
demanda[11] = (20,1)
demanda[12] = (40,15)

meses = {}
for mes in range(1,13):
  probD = {}
  for d in range(0,200 +1):
    a = demanda[mes][0] - demanda[mes][1]
    b = demanda[mes][0] + demanda[mes][1]

    if a - 1 < d < b + 1 :
      probD[d] = 1/(2*demanda[mes][1] +1)
    else:
      probD[d] = 0

    meses[mes] = probD


semana_mes = {}
for t in range(1,53):
  if 1<=t<5 : semana_mes[t] = 1
  if 5<=t<9 : semana_mes[t] = 2
  if 9<=t<14 : semana_mes[t] = 3
  if 14<=t<18 : semana_mes[t] = 4
  if 18<=t<23 : semana_mes[t] = 5
  if 23<=t<27 : semana_mes[t] = 6
  if 27<=t<31 : semana_mes[t] = 7
  if 31<=t<36 : semana_mes[t] = 8
  if 36<=t<40 : semana_mes[t] = 9
  if 40<=t<45 : semana_mes[t] = 10
  if 45<=t<49 : semana_mes[t] = 11
  if 49<=t<53 : semana_mes[t] = 12

T = 52
Q = 200
c = 25
f = 1500
h = 6
q = 90
K = 1500
