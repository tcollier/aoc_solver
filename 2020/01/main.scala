import scala.collection.immutable.Set
import scala.util.Sorting

import tcollier.Executor
import tcollier.InputLoader
import tcollier.Solution

class SumNotPossible(s: String) extends RuntimeException {

}

class Day1Solution(val sum: Int) extends Solution[Int] {
  def part1Answer(numbers: Array[Int]): String = {
    val pair = pairWithSum(numbers)
    return String.valueOf(pair._1 * pair._2)
  }

  def part2Answer(numbers: Array[Int]): String = {
    val triplet = tripletWithSum(numbers)
    return String.valueOf(triplet._1 * triplet._2 * triplet._3)
  }

  def pairWithSum(numbers: Array[Int]): (Int, Int) = {
    val others: Set[Int] = numbers.toSet

    for (i <- 0 to numbers.size - 2) {
      val number: Int = numbers(i)
      if (others(sum - number))
        return (number, sum - number)
    }
    throw new SumNotPossible(s"Cannot find pair with sum $sum")
  }

  def tripletWithSum(numbers: Array[Int]): (Int, Int, Int) = {
    Sorting.quickSort(numbers)

    for (i <- 0 to numbers.size - 3) {
      var j: Int = i + 1
      var k: Int = numbers.size - 1
      while (j < k) {
        val total: Int = numbers(i) + numbers(j) + numbers(k)
        if (total == sum) {
          return (numbers(i), numbers(j), numbers(k))
        } else if (total < sum) {
          j += 1
        } else {
          k -= 1
        }
      }
    }
    throw new SumNotPossible(s"Cannot find triplet with sum $sum")
  }
}


object Main {
  def main(args: Array[String]): Unit = {
    var numbers = new InputLoader("2020/01/input.txt").getInts()
    val executor = new Executor[Int](new Day1Solution(2020), numbers)
    executor.run(args)
  }
}
