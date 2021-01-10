package tcollier

class IterationTimer(val durationInMillis: Long, val iterations: Int) {
  def asJson(): String = {
    return s"""{"duration":${durationInMillis * 1000},"iterations":${iterations}}"""
  }
}

class Executor[T](solution: Solution[T] , input: Array[T]) {
  def run(args: Array[String]) = {
    if (args.size >= 1 && args(args.size - 1).equals("--time")) {
      time()
    } else {
      solve()
    }
  }

  def solve() = {
    println(solution.part1Answer(input))
    println(solution.part2Answer(input))
  }

  def time() = {
    val part1: IterationTimer = timeAnswer(1)
    val part2: IterationTimer = timeAnswer(2)
    println(s"""{"part1":${part2.asJson()},"part2":${part2.asJson()}}""")
  }

  def continueTiming(iterations: Int, duration: Long): Boolean = {
    if (iterations < 100) {
      return duration < 30000L
    } else {
      return duration < 100L
    }
  }

  def timeAnswer(part: Int): IterationTimer = {
    var i: Int = 0
    var runningTime: Long = 0
    while (continueTiming(i, runningTime)) {
      val List[T] inputClone = (List<T>)input.clone()
      val startTime: Long = System.currentTimeMillis()
      if (part == 1) {
        solution.part1Answer(inputClone)
      } else {
        solution.part2Answer(inputClone)
      }
      runningTime += System.currentTimeMillis() - startTime
      i += 1
    }
    return new IterationTimer(runningTime, i)
  }
}
