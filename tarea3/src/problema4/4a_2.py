m = Int(ceil(q^(1/4)))
Js = [[0,0] for i in 0:2m+1]

for i in 0:2:2*m
    Js[i+1] = pnt_k(P, Int(i/2), E[1], q)
    Js[i+2] = [Js[i+1][1], -Js[i+1][2]]
end