l=0.8
V = Vn = {0:0,1:0}
iter = 0
while 1:
    iter += 1
    Vn = {}
    Vn[0] = max(1 + l*V[0], 2 + l/2*(V[0] + V[1]))
    Vn[1] = max(1 + l/2*(V[0] + V[1]), 2 + l*V[0]/2)
    print(iter,Vn)
    if normaInfinito(Vn,V) < 1e-8:
        print((1 + l*Vn[0], 2 + l/2*(Vn[0] + Vn[1])), (1 + l/2*(Vn[0] + Vn[1]), 2 + l*Vn[0]/2))
        print("Si está en 0 estudiar mucho, si está en 1 estudiar poco")
        break
    else: V = Vn
