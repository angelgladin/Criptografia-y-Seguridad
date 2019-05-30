import java.math.BigInteger
import java.util.Random


typealias BigIntegerTriple = Triple<BigInteger, BigInteger, BigInteger>

/**
 * Implementación del algoritmo de factorización de números sobre curvas elípticas.
 *
 * @property compositeNumber Número compuesto a factorizar.
 * @property primeUpperBound Cota superior para lla generación de números primos menores que $\sqrt{n}$.
 *
 * @author Angel Ivan Gladin Garcia
 * @author Alinka Atenas Fragoso Martínez
 */
class ECM(private val compositeNumber: BigInteger, private val primeUpperBound: Int) {

    /**
     * Criba de Eratosthenes para calcular primos menores a $\sqrt{n}$.
     * @return Lista con de primos acotados menores que $\sqrt{n}$.
     */
    private fun sieveOfEratosthenes(): List<BigInteger> {
        val n = primeUpperBound
        val b = BooleanArray(n + 1) { true }
        val primeList = mutableListOf<BigInteger>()

        var p = 2
        while (p * p <= n) {
            if (b[p]) {
                primeList.add(p.toBigInteger())
                var i = p * 2
                while (i <= n) {
                    b[i] = false
                    i += p
                }
            }
            p++
        }
        return primeList
    }

    /**
     * Inverso multiplicativo de [a] módulo [m] con ayuda del *gcd*.
     */
    private fun modularInv(a: BigInteger, b: BigInteger): BigIntegerTriple {
        if (b == BigInteger.ZERO) {
            return BigIntegerTriple(BigInteger.ONE, BigInteger.ZERO, a)
        }
        val (q, r) = Pair(a / b, a % b)
        val (x, y, g) = modularInv(b, r)

        return BigIntegerTriple(y, x - q * y, g)
    }

    /**
     * Agrega un punto sobre la curva elíptica.
     * @param p Un punto.
     * @param q Un punto.
     * @param a Constante de la ecuación $y^2 = x^3 + ax + b$.
     * @param b Constante de la ecuación $y^2 = x^3 + ax + b$.
     * @param m El módulo.
     * @return Un nuevo punto.
     */
    private fun ellipticAdd(
        p: BigIntegerTriple,
        q: BigIntegerTriple,
        a: BigInteger,
        @Suppress("UNUSED_PARAMETER") b: BigInteger,
        m: BigInteger
    ): BigIntegerTriple {
        if (p.first == BigInteger.ZERO) {
            return q
        }
        if (q.third == BigInteger.ZERO) {
            return p
        }

        val num: BigInteger
        val denom: BigInteger

        if (p.first == q.first) {
            if ((p.second + q.second) % m == BigInteger.ZERO) {
                return BigIntegerTriple(BigInteger.ZERO, BigInteger.ONE, BigInteger.ZERO)
            }
            num = (BigInteger("3") * p.first * p.first + a) % m
            denom = (BigInteger.TWO * p.second) % m
        } else {
            num = (q.second - p.second) % m
            denom = (q.first - p.first) % m
        }

        val (inv, _, g) = modularInv(denom, m)

        if (g > BigInteger.ONE) {
            return BigIntegerTriple(BigInteger.ZERO, BigInteger.ZERO, denom)
        }

        val z = (num * inv * num * inv - p.first - q.first) % m

        return BigIntegerTriple(z, (num * inv * (p.first - z) - p.second) % m, BigInteger.ONE)
    }

    /**
     * Multiplica dos puntos sobre la curva elíptica.
     * @param k_aux Escalar que será multiplicado por [p_aux].
     * @param p_aux Punto a multiplicar.
     * @param a Constante de la ecuación $y^2 = x^3 + ax + b$.
     * @param b Constante de la ecuación $y^2 = x^3 + ax + b$.
     * @param m El módulo.
     * @return Un nuevo punto.
     */
    private fun ellipticMult(
        k_aux: BigInteger,
        p_aux: BigIntegerTriple,
        a: BigInteger,
        b: BigInteger,
        m: BigInteger
    ): BigIntegerTriple {
        var r = BigIntegerTriple(BigInteger.ZERO, BigInteger.ONE, BigInteger.ZERO)
        var k = k_aux
        var p = p_aux

        while (k > BigInteger.ZERO) {
            if (p.third > BigInteger.ONE) {
                return p
            }
            if (k % BigInteger.TWO == BigInteger.ONE) {
                r = ellipticAdd(p, r, a, b, m)
            }
            k /= BigInteger.TWO
            p = ellipticAdd(p, p, a, b, m)
        }

        return r
    }

    /**
     * Genera un número aleatorio.
     * @param upperBound Cota superior para generar número aleatorio.
     * @return Un número aleatorio entre [0, [upperBound]].
     */
    private fun randomBigInteger(upperBound: BigInteger): BigInteger {
        val len = upperBound.bitLength()
        var r = BigInteger(len, Random())

        while (r >= upperBound)
            r = BigInteger(len, Random())

        return r
    }

    /**
     * Algoritmo `Lenstra elliptic-curve factorization (ECM)` para la factorización
     * de un número *n* de la forma *n=pq*.
     * @return Un factor del número *n*.
     */
    private fun lenstra(): BigInteger? {
        val n = compositeNumber
        var g = n
        var q = BigIntegerTriple(BigInteger.ZERO, BigInteger.ZERO, BigInteger.ZERO)
        var a = BigInteger.ZERO
        var b = BigInteger.ZERO

        while (g == n) {
            q = BigIntegerTriple(randomBigInteger(n), randomBigInteger(n), BigInteger.ONE)
            a = randomBigInteger(n)
            b = (q.second * q.second - q.first * q.first * q.first - a * q.first) % n
            g = n.gcd(BigInteger("4") * a * a * a + BigInteger("27") * b * b)
        }
        if (g > BigInteger.ONE) {
            return g
        }

        sieveOfEratosthenes().forEach { p ->
            var pp = p
            while (pp < primeUpperBound.toBigInteger()) {
                q = ellipticMult(p, q, a, b, n)
                if (q.third > BigInteger.ONE) {
                    return n.gcd(q.third)
                }
                pp *= p
            }
        }

        return null
    }

    /**
     * Regresa los factores de un número de la forma *n=pq* usando el algoritmo de factorización
     * por curvas elípticas de Lenstra.
     */
    fun factors(): Pair<BigInteger, BigInteger> {
        var p = lenstra()
        while (p == null)
            p = lenstra()

        return Pair(p, compositeNumber / p)
    }
}

fun main(args: Array<String>) {
    val compositeNumberArg = args[0]
    val primeCountUpperBoundArg = args[1]
    println("Número a factorizar: $compositeNumberArg")

    val compositeNumber = compositeNumberArg.toBigInteger()
    val primeCountUpperBound = primeCountUpperBoundArg.toInt()

    val ecm = ECM(compositeNumber, primeCountUpperBound)

    println("Sus facotores son: ${ecm.factors()}")
}
