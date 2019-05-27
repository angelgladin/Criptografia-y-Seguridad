m = Int(ceil(sqrt(358)))
mP = pnt_k(P, m, E[1], q)

iP_s = [pnt_k(P, i, E[1], q) for i in 0:m-1]

j = 0
jmP = pnt_k(mP, j, E[1], q)
m_jmP = [Int(jmP[1]), -Int(jmP[2])]
res = pnt_add(Q,m_jmP,q)
res in iP_s
# Observamos que j = 0 se encuentra en iP_s, en el índice i = 7
i = 7
k = (i + j*m)%q

# Corroboramos que kP = C1
pnt_k(P, k, E[1], q) == Q

#Calculamos M + kB y corroboramos que sea igual al C2 proporcionado
kB = pnt_k(B, k, E[1], q)
test_M2 = pnt_add(M, kB, q)

