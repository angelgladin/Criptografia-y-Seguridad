p1 = pnt_k(P, 2*m, E[1], q)
k = 0
r = [0,0]

prueba = false
while prueba == false && k < m
    p2 = pnt_k(p1, k, E[1], q)
    r = pnt_add(Q, p2, q)
    prueba = (r in Js)
    k = k + 1
    
end
if k!=m  #Puede que haya un caso en el que k sí deba ser m, pero son raros
    k = k-1
end

j = 0
alph = Int((q +1 +2*m*k - j))
P2 = pnt_k(P, alph, E[1], q)