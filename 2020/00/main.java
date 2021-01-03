import tcollier.Executor;
import tcollier.Solution;

class Day0Solution implements Solution {
  private String[] data;

  public Day0Solution(String[] data) {
    this.data = data;
  }

  public String part1Answer() {
    return this.data[0];
  }

  public String part2Answer() {
    return this.data[1];
  }
}

class Main {
  public static void main(String[] args) {
    String[] data = {"Hello", "World!"};
    Executor executor = new Executor(new Day0Solution(data));
    executor.run(args);
  }
}
