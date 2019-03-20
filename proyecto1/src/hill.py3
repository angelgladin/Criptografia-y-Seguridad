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

    def _msg_to_matrix(self) -> Matrix:
        n_columns: int = int(sqrt(self.len_key))
        n_rows: int = self.len_msg // n_columns
        msg_matrix: Matrix = [[-1]*n_columns for _ in range(n_rows)]

        c: int = 0
        for i in range(n_rows):
            for j in range(n_columns):
                msg_matrix[i][j] = SPANISH_ALPHABET.index(self.msg[c%MOD])
                c += 1

        return msg_matrix

    def _matrix_multiplication(self, m1: Matrix, m2: Matrix) -> Matrix:
        r_matrix: Matrix = [[-1]*(len(m2[0])) for _ in range(len(m2))]

        for h in range(len(r_matrix)):
            for i in range(len(m1)):
                a: int = 0
                for j in range(len(m2[0])):
                    a += m1[i][j] * m2[h][j]
                r_matrix[h][i] = a % MOD

        return r_matrix

    def _matrix_to_str(self, m: Matrix) -> str:
        s: str = ''

        for i in range(len(m)):
            for j in range(len(m[i])):
                s += SPANISH_ALPHABET[m[i][j]]

        return s


class Hill_Cipher(Hill_Algorithm):

    def __init__(self, msg: str, key: str) -> None:
        len_key_matrix: float = sqrt(len(key))
        assert len_key_matrix.is_integer(), 'La raiz de la longtud de la clave no es exacta'
        assert len(msg) % len_key_matrix == 0, 'Mensaje inválido, no se puede formar matrices Nx1'

        self.msg: str = msg
        self.key:str = key

        self.len_msg: int = len(msg)
        self.len_key: int = len(key)
        
    def ciphered_msg(self) -> str:
        key_matrix: Matrix = self.__get_key_matrix()
        msg_matrix: Matrix = super()._msg_to_matrix()
        matrix_prod_key_by_msg: Matrix = super()._matrix_multiplication(key_matrix, msg_matrix)
        return super()._matrix_to_str(matrix_prod_key_by_msg)
    
    def __get_key_matrix(self) -> Matrix:
        n: int = int(sqrt(self.len_key))
        key_matrix: Matrix = [[-1]*n for _ in range(n)]

        c: int = 0
        for i in range(n):
            for j in range(n):
                key_matrix[i][j] = SPANISH_ALPHABET.index(self.key[c%MOD])
                c += 1

        return key_matrix


class Hill_Decipher(Hill_Algorithm):

    def __init__(self, msg: str, matrix: Matrix) -> None:
        assert self.__is_invertible(matrix), 'La matriz no es invertible.'

        self.msg: str = msg
        self.matrix: Matrix = matrix

        self.len_msg: int = len(msg)
        self.len_key: int = len(key)

    def __is_invertible(self, m) -> bool:
        aux: numpy.ndarray = numpy.array(m)
        try:
            numpy.linalg.inv(m)
        except numpy.linalg.LinAlgError:
            return False
        return True

    def dechipher_message(self) -> str:
        key_matrix_inv: Matrix = self.__modular_matrix_inverse()
        msg_matrix: Matrix = super()._msg_to_matrix()
        matrix_prod_key_inv_by_msg: Matrix = super()._matrix_multiplication(key_matrix_inv, msg_matrix)
        return self._matrix_to_str(matrix_prod_key_inv_by_msg)

    def __modular_matrix_inverse(self) -> Matrix:
        return sympy.Matrix(self.matrix).inv_mod(MOD).tolist()


if __name__ == '__main__':
    # Mensaje original
    msg: str = 'CONSUL'
    key: str = 'FORTALEZA'

    print(msg)
    print(key)

    # Codificar
    hill_Cipher = Hill_Cipher(msg, key)
    print(hill_Cipher.ciphered_msg())

    # Decodificar
    ciphered_msg: str = 'KUTÑOB'
    ciphered_matrix: Matrix = [[5, 15, 18], [20, 0, 11], [4, 26, 0]]
    hill_Decipher = Hill_Decipher(ciphered_msg, ciphered_matrix)
    print(hill_Decipher.dechipher_message())
