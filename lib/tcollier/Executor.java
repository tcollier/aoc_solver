package tcollier;

import java.lang.StringBuilder;

class IterationTimer {
  private long durationInMillis;
  private int iterations;

  public IterationTimer(long durationInMillis, int iterations) {
    this.durationInMillis = durationInMillis;
    this.iterations = iterations;
  }

  public void appendJson(StringBuilder builder) {
    builder.append("{\"duration\":");
    builder.append(this.durationInMillis * 1000);
    builder.append(",\"iterations\":");
    builder.append(this.iterations);
    builder.append("}");
  }
}

public class Executor {
  private Solution solution;

  public Executor(Solution solution) {
    this.solution = solution;
  }

  public void run(String[] args) {
    if (args.length >= 1 && args[args.length - 1].equals("--time")) {
      this.time();
    } else {
      this.solve();
    }
  }

  private void solve() {
    System.out.println(this.solution.part1Answer());
    System.out.println(this.solution.part2Answer());
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
    long startTime = System.currentTimeMillis();
    for (; this.continueTiming(i, System.currentTimeMillis() - startTime); i++) {
      if (part == 1) {
        this.solution.part1Answer();
      } else {
        this.solution.part2Answer();
      }
    }
    return new IterationTimer(System.currentTimeMillis() - startTime, i);
  }
}
