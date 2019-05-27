def encontrar_puntos(A, B, p):
    '''Función que encuentra los puntos de la curva tal que
    satisface la ecuación.

    Ecuación de la curva elíptica de Weierstrass
        y^2 = x^3 + Ax + B

    Arguments:
        A {[int]} -- [Constamte de la ecuación]
        B {[int]} -- [Constamte de la ecuación]
        p {[int]} -- [Primo del campo Z_p]
    '''

    # Lista que tendrá los puntos
    puntos = []

    # Iterar sobre los valores que tomará la x
    for i in range(p):
        # Calcular x^3 + Ax + B módulo p
        l = (pow(i, 3, p) + (A * i) + B) % p
        # Iterar sobre los valores que tomará la y
        for j in range(p):
            y_2 = pow(j, 2, p)
            # Verificar si satisface la congruencia
            if (y_2 - l) % p == 0:
                # Agregar el punto
                puntos.append((i, j,))

    return puntos

print(encontrar_puntos(A=1, B=9, p=17))
