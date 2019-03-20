# -*- coding: utf-8 -*-

__author__ = "Ángel Iván Gladín García"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "angelgladin@ciencias.unam.mx"
__status__ = "Finished"


from math import sqrt
from typing import List

import sympy
import numpy


SPANISH_ALPHABET: str = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
MOD: int = len(SPANISH_ALPHABET)

Matrix = List[List[int]]


class Hill_Algorithm(object):
    """Funciones para la maipulación de matrices y texto.
    """

    def __init__(self, msg: str):
        """Inicializa el mensaje y lo guarda como propiedad.

        Sirve para guardar el mensaje a cifrar o descifrar.

        Arguments:
            msg {str} -- Mensaje
        """
        self.msg = msg
        self.len_msg = len(msg)

    def _msg_to_matrix(self, len_key: int) -> Matrix:
        """Convierte el mensaje a una matriz.

        Se hace una transformación del mensaje origial a una matriz
        de la forma `sqrt(self.len_key)` x `self.len_msg // n_columns`.

        Returns:
            Matrix -- Matriz cuadrada del mensaje
        """
        n_columns: int = int(sqrt(len_key))
        n_rows: int = self.len_msg // n_columns
        msg_matrix: Matrix = [[-1] * n_columns for _ in range(n_rows)]

        c: int = 0
        for i in range(n_rows):
            for j in range(n_columns):
                msg_matrix[i][j] = SPANISH_ALPHABET.index(self.msg[c % MOD])
                c += 1

        return msg_matrix

    def _matrix_multiplication(self, m1: Matrix, m2: Matrix) -> Matrix:
        """Multiplicación de dos matrices.

        Función auxiliar para la multiplicación de dos matrices.

        Arguments:
            m1 {Matrix} -- Matriz 1
            m2 {Matrix} -- Matriz 2

        Returns:
            Matrix -- El producto de ambas matrices
        """
        r_matrix: Matrix = [[-1] * (len(m2[0])) for _ in range(len(m2))]

        for h in range(len(r_matrix)):
            for i in range(len(m1)):
                a: int = 0
                for j in range(len(m2[0])):
                    a += m1[i][j] * m2[h][j]
                r_matrix[h][i] = a % MOD

        return r_matrix

    def _matrix_to_str(self, m: Matrix) -> str:
        """Representación como cadena de una matriz.

        Recorre la matriz uno por uno para ir concatenando el mensaje
        resultante a una cadena.

        Arguments:
            m {Matrix} -- Matriz cifrada o descifrada

        Returns:
            str -- Representación en una cadena de la matriz
        """
        s: str = ''

        for i in range(len(m)):
            for j in range(len(m[i])):
                s += SPANISH_ALPHABET[m[i][j]]

        return s


class Hill_Cipher(Hill_Algorithm):
    """Clase auxiliar para hacer el cifrado dado un mensaje y
    una llave ambas en cadenas.

    Extends:
        Hill_Algorithm
    """

    def __init__(self, msg: str, key: str) -> None:
        """Constructor para inicializar los atributos.

        Arguments:
            msg {str} -- Mensaje a cifrar
            key {str} -- Llave que se aplicará al mensaje
        """
        len_key_matrix: float = sqrt(len(key))
        # Debe cumplir estás condiciones, si no se debe parar su ejecición.
        assert len_key_matrix.is_integer(), 'La raiz de la longtud de la clave no es exacta'
        assert len(msg) % len_key_matrix == 0, 'Mensaje inválido, no se puede formar matrices Nx1'

        super().__init__(msg)
        self.key: str = key
        self.len_key: int = len(key)

    def ciphered_msg(self) -> str:
        """Cifra el mensaje.

        Cifra el mensaje con la llaves dadas.

        Returns:
            str -- El mensaje cifrado
        """
        key_matrix: Matrix = self.__get_key_matrix()
        msg_matrix: Matrix = super()._msg_to_matrix(self.len_key)
        matrix_prod_key_by_msg: Matrix = super()._matrix_multiplication(key_matrix, msg_matrix)
        return super()._matrix_to_str(matrix_prod_key_by_msg)

    def __get_key_matrix(self) -> Matrix:
        """Convierte la llave a una matriz cuadrada

        Con la cadena de la llave, la convierte a una matriz cuadrada
        para después operar con ella.

        Returns:
            Matrix -- Matriz cuadradada de la llave
        """
        n: int = int(sqrt(self.len_key))
        key_matrix: Matrix = [[-1] * n for _ in range(n)]

        c: int = 0
        for i in range(n):
            for j in range(n):
                key_matrix[i][j] = SPANISH_ALPHABET.index(self.key[c % MOD])
                c += 1

        return key_matrix


class Hill_Decipher(Hill_Algorithm):
    """Decifra un mensaje que fue cifrado con el algoritmo de Hill

    Extends:
        Hill_Algorithm
    """

    def __init__(self, msg: str, matrix: Matrix) -> None:
        """Constructor que incializa el mensaje a descifrar y la llave
        que es una matriz.

        Arguments:
            msg {str} -- Mensaje a descifrar
            matrix {Matrix} -- Matriz de cifrado
        """
        # Verificamos que la matriz de cifrado sea invertible, si no,
        # terminar el programa con gracia.
        assert self.__is_invertible(matrix), 'La matriz no es invertible.'

        super().__init__(msg)
        self.matrix: Matrix = matrix
        self.len_key: int = len(key)

    def __is_invertible(self, m) -> bool:
        """Verfifica si una matriz es invertible.

        Por unos teoremas de álgebra lineal podemos verificar si es
        invertible una matriz, pero como es muy talachudo eso
        usamos numpy :v

        Arguments:
            m {Matriz} -- Matriz

        Returns:
            bool -- Si es invertible o no
        """
        aux: numpy.ndarray = numpy.array(m)
        try:
            numpy.linalg.inv(m)
        except numpy.linalg.LinAlgError:
            return False
        return True

    def dechipher_message(self) -> str:
        """Descifra el mensaje con el mensaje y la matriz de cifgrado

        Descifra el mensaje.

        Returns:
            str -- El texto descifrado
        """
        key_matrix_inv: Matrix = self.__modular_matrix_inverse()
        msg_matrix: Matrix = super()._msg_to_matrix(self.len_key)
        matrix_prod_key_inv_by_msg: Matrix = super()._matrix_multiplication(key_matrix_inv, msg_matrix)
        return self._matrix_to_str(matrix_prod_key_inv_by_msg)

    def __modular_matrix_inverse(self) -> Matrix:
        """Obtiene el inverso de la matriz módulo N.

        Se uso sympy para obtener fácilmente inversa módulo N
        de la matriz.

        Returns:
            Matrix -- Inversa de la matriz mod N
        """
        return sympy.Matrix(self.matrix).inv_mod(MOD).tolist()


def normalize_string(s: str) -> str: 
    """Limpia texto.

    Remueve espacios, signos de puntiación y acentos

    Arguments:
        s {str} -- Cadena a normalizar

    Returns:
        str -- Cadena normalizada
    """
    accents_dic = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }

    r = ''
    for x in s:
        if x.isalpha():
            aux = x.upper()
            if aux in accents_dic:
                r += accents_dic[aux]
            else:
                r += x.upper()

    return r


if __name__ == '__main__':
    # Mensaje original
    msg: str = normalize_string('CONSUL')
    key: str = normalize_string('FORTALEZA')

    print(msg)
    print(key)

    # Codificar
    hill_Cipher = Hill_Cipher(msg, key)
    print(hill_Cipher.ciphered_msg())

    # Decodificar
    ciphered_msg: str = normalize_string('KUTÑOB')
    ciphered_matrix: Matrix = [[5, 15, 18], [20, 0, 11], [4, 26, 0]]
    hill_Decipher = Hill_Decipher(ciphered_msg, ciphered_matrix)
    print(hill_Decipher.dechipher_message())
