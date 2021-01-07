package tcollier;

import java.lang.StringBuilder;
import java.util.ArrayList;

class IterationTimer {
  private long durationInMillis;
  private int iterations;

  public IterationTimer(long durationInMillis, int iterations) {
    this.durationInMillis = durationInMillis;
    this.iterations = iterations;
  }

  public void appendJson(StringBuilder builder) {
    builder.append("{\"duration\":");
    builder.append(durationInMillis * 1000);
    builder.append(",\"iterations\":");
    builder.append(iterations);
    builder.append("}");
  }
}

public class Executor<T> {
  private Solution<T> solution;
  private ArrayList<T> input;

  public Executor(Solution<T> solution, ArrayList<T> input) {
    this.solution = solution;
    this.input = input;
  }

  public void run(String[] args) {
    if (args.length >= 1 && args[args.length - 1].equals("--time")) {
      time();
    } else {
      solve();
    }
  }

  private void solve() {
    System.out.println(solution.part1Answer((ArrayList<T>)input.clone()));
    System.out.println(solution.part2Answer((ArrayList<T>)input.clone()));
  }

  private void time() {
    IterationTimer part1 = timeAnswer(1);
    IterationTimer part2 = timeAnswer(2);
    StringBuilder builder = new StringBuilder();
    builder.append("{\"part1\":");
    part1.appendJson(builder);
    builder.append(",\"part2\":");
    part2.appendJson(builder);
    builder.append("}");
    System.out.println(builder.toString());
  }

  private boolean continueTiming(int iterations, long duration) {
    if (iterations < 100) {
      return duration < 30000l;
    } else {
      return duration < 100l;
    }
  }

  private IterationTimer timeAnswer(int part) {
    int i = 0;
    long runningTime = 0;
    for (; continueTiming(i, runningTime); i++) {
      ArrayList<T> inputClone = (ArrayList<T>)input.clone();
      long startTime = System.currentTimeMillis();
      if (part == 1) {
        solution.part1Answer(inputClone);
      } else {
        solution.part2Answer(inputClone);
      }
      runningTime += System.currentTimeMillis() - startTime;
    }
    return new IterationTimer(runningTime, i);
  }
}
