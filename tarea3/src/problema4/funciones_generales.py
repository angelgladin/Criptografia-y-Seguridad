# Función que calcula el inverso de un número en Zp
function inverso_unidad(a, mod)    
    u0, u1 = 1, 0
    v0, v1 = 0, 1
 
    while mod != 0
        q = floor(a/mod)
        r = a - mod * q
        u = u0 - q * u1
        v = v0 - q * v1
        #Update a,b
        a = mod
        mod = r
        #Update for next iteration
        u0 = u1
        u1 = u
        v0 = v1
        v1 = v
    end
 
    return  a, u0, v0
end

#Funcion que verifica que una congruencia tenga solucion
function cong_val(a,b,n)
    j = gcd(a,n)
    ans = false
    if b % j == 0
        ans = true
    end
    
    return ans
end

# solve_congruencia(a, b, n) soluciona la congruencia usando el algoritmo extendido de Euclides.
function congruencias(a,b,n)
    if cong_val(a,b,n)
        # Reduciendo la congruencia 
        m_c_d = gcd(a,n)
        a, n, b = a/m_c_d, n/m_c_d, b/m_c_d
        
        a_inverso = (inverso_unidad(a, n)[2] + n) % n
        
        x = (b * a_inverso) % n
        #x = x * m_c_d
    else
        x = "La congruencia no es válida"
    end
    
    return x
end

#Función que suma dos puntos diferentes P,Q en una curva elíptica
function pnt_add(P, Q, mod)

    lam = ((Q[2] - P[2]) % mod)//(Q[1] - P[1])
    if denominator(λ) != 1
        lam = congruencias(denominator(lam), numerator(lam), mod)
        else 
        lam = numerator(lam)
    end
    lam = (mod + lam) % mod 
    x = (lam^2 - P[1] - Q[1]) % mod
    y = (lam*(P[1]-x) - P[2]) % mod
    x = (mod + x) % mod
    y = (mod + y) % mod
    
    return [Int(x),Int(y)]
    
end

#Funcion que calcula  P+P= 2P en una curva eliptica
function pnt_double(P, a, mod)
    Q = P
    lam = ((3*P[1]^2 + a) % mod)//(2*P[2])
    if denominator(lam) != 1
        lam = congruencias(denominator(lam), numerator(lam), mod)
        else 
        lam = numerator(lam) % mod
    end
    lam = (mod + lam) % mod 
    x = (lam^2 - P[1] - Q[1]) % mod
    y = (lam*(P[1]-x) - P[2]) % mod
    x = (mod + x) % mod
    y = (mod + y) % mod
    
    return [Int(x),Int(y)]
    
end

#Funcion que regresa la representacion binaria de un número decimal
function binary_s(d)
    
    a = bitstring(d)
    if d != 0
        l = "1"*split(a,'1'; limit=2)[2]
        else 
        l = "0"
    end
    return l
end

# Funcion que multiplica a un numero por un escalar d, representado en la forma binaria $d = d_{0} + 2^{w}d_{1} + 2^{2w}d_{2} + ... + 2^{mw}d_{m}$
function pnt_k(P, d, a, mod)
    N = P
    Q = [0,0]
    l = binary_s(d)
    m = length(l)
        
    for i in m:-1:1
        if l[i] == '1'
            if Q[1] != 0 || Q[2] != 0
                Q = pnt_add(N, Q, mod) 
                else 
                Q = N
            end
        end 
        N = pnt_double(N, a, mod)
    end
    
    return Q
end
