import scala.io.Source
import scala.collection.immutable.Set

class SumNotPossible(s: String) extends RuntimeException {

}

object Main {
  def pairWithSum(numbers: Array[Int], sum: Int): (Int, Int) = {
    val others: Set[Int] = numbers.toSet
    for (number <- numbers)
      if (others(sum - number))
        return (number, sum - number)
    throw new SumNotPossible(s"Cannot find pair with sum $sum")
  }

  def tripletWithSum(numbers: Array[Int], sum: Int): (Int, Int, Int) = {
    val sorted = numbers.sortWith(_ < _)
    for (i <- 0 to sorted.length - 3) {
      var j: Int = i + 1
      var k: Int = sorted.length - 1
      while (j < k) {
        val total: Int = sorted(i) + sorted(j) + sorted(k)
        if (total == sum) {
          return (sorted(i), sorted(j), sorted(k))
        } else if (total < sum) {
          j += 1
        } else {
          k -= 1
        }
      }
    }
    throw new SumNotPossible(s"Cannot find triplet with sum $sum")
  }

  def main(args: Array[String]): Unit = {
    var numbers: Array[Int] = new Array[Int](200)
    val source = Source.fromFile("2020/01/input.txt")
    var i: Int = 0
    for (line <- source.getLines()) {
      numbers(i) = line.toInt
      i += 1
    }
    source.close()

    val pair = pairWithSum(numbers, 2020)
    println(pair._1 * pair._2)

    val triplet = tripletWithSum(numbers, 2020)
    println(triplet._1 * triplet._2 * triplet._3)
  }
}
