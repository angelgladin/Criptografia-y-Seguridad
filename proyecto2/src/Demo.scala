import BigInt._
import scala.util.Random
import scala.collection.mutable.StringBuilder


class RSA {
  // Para asegurar que la longitud del primo es de al menos 100 dígitos
  val bitLength = 512

  // Dos números primos aleatorios
  val p: BigInt = probablePrime(bitLength, Random)
  val q: BigInt = probablePrime(bitLength, Random)
  // $n = p*q$
  val n: BigInt = p * q
  // Cota superior para elegir `e`
  private val phi: BigInt = (p - 1) * (q - 1)

  private var e_aux: BigInt = probablePrime(bitLength / 2, Random)
  // $e$ tal que $gcd(e,\phi(n)) = 1$
  val e: BigInt = {
    while (phi.gcd(e_aux) > 1) e_aux += 1

    e_aux
  }
  // Satisface la congruencia $de \cog \mod{\phi(n)}$
  val d = e.modInverse(phi)

  /** Cifrado de un mensaje usando RSA.
    *
    * @param n Producto de dos primos `p` y `q`
    * @param e Primo relativo von $\phi(n)$
    * @param m Mensaje a cifrar
    * @return Un arreglo con el texto cifrado
    */
  def encrypt(n: BigInt, e: BigInt, m: String): Array[BigInt] = {
    val length = m.length
    var arr_r = Array.ofDim[BigInt](length)

    for (i <- 0 until length) {
      arr_r(i) = BigInt(m(i).toInt).modPow(e, n)
    }

    arr_r
  }

  /** Descifrado de un arreglo que contiene números para después
    * hacer su conversión a una cadena.
    *
    * @param n Producto de dos primos `p` y `q`
    * @param d Módulo inverso tal que $de \cog \mod{\phi(n)}
    * @param m Mensaje cifrado representado como un arreglo de enteros
    * @return El texto descifrado
    */
  def decrypt(n: BigInt, d: BigInt, m: Array[BigInt]): String = {
    val length = m.length
    val msg = new StringBuilder()

    for (i <- 0 until length) {
      msg.append(m(i).modPow(d, n).toChar)
    }

    msg.toString
  }

}


object Demo {
  def main(args: Array[String]): Unit = {
    // Creación de la instancia del cifrado RSA
    val rsa = new RSA()
    // Valor a usar en el cifrado y descifrado
    val n: BigInt = rsa.n
    val e: BigInt = rsa.e
    val d: BigInt = rsa.d

    println("Las llaves son:")
    println(s"p = ${rsa.p}")
    println(s"q = ${rsa.q}")
    println("--------------------------------")
    println(s"N = ${n}")
    println("--------------------------------")
    println(s"e = ${e}")
    println(s"d = ${d}")
    println("--------------------------------")

    println("Mensaje a cifrar:")
    val msg: String = "Cryptography rulez! B-)"
    println(msg)

    val encryptedMessage: Array[BigInt] = rsa.encrypt(n, e, msg)

    println("Mensaje cifrado:")
    println(encryptedMessage.mkString)

    println("--------------------------------")
    println("Mensaje descifrado:")
    println(rsa.decrypt(n, d, encryptedMessage))
  }
}
