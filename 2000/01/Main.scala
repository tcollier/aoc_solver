import tcollier.Executor
import tcollier.Solution

class Day0Solution extends Solution[String] {
  def part1Answer(input: Array[String]): String = {
    return input(0)
  }

  def part2Answer(input: Array[String]): String = {
    return input(1)
  }
}

object Main {
  def main(args: Array[String]) = {
    val input: Array[String] = Array("Hello", "World!")
    val executor = new Executor[String](new Day0Solution(), input)
    executor.run(args)
  }
}
