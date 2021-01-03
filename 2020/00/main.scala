import tcollier.Executor;
import tcollier.Solution;

class Day0Solution(val input: Array[String]) extends Solution {
  def part1Answer(): String = {
    return input(0)
  }

  def part2Answer(): String = {
    return input(1)
  }
}

object Main {
  def main(args: Array[String]): Unit = {
    val data: Array[String] = Array("Hello", "World!");
    val executor: Executor = new Executor(new Day0Solution(data));
    executor.run(args);
  }
}
