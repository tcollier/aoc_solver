import java.util.ArrayList;

import tcollier.Executor;
import tcollier.Solution;

class Day0Solution implements Solution<String> {
  public String part1Answer(ArrayList<String> input) {
    return input.get(0);
  }

  public String part2Answer(ArrayList<String> input) {
    return input.get(1);
  }
}

class Main {
  public static void main(String[] args) {
    ArrayList<String> input = new ArrayList<String>();
    input.add("Hello");
    input.add("World!");
    Executor<String> executor = new Executor<String>(new Day0Solution(), input);
    executor.run(args);
  }
}
