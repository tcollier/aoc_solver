import java.util.BitSet;

import tcollier.Executor;
import tcollier.Solution;

class Day15Solution implements Solution {
  private int[] input;
  private int part1Rounds;
  private int part2Rounds;

  public Day15Solution(int[] input, int part1Rounds, int part2Rounds) {
    this.input = input;
    this.part1Rounds = part1Rounds;
    this.part2Rounds = part2Rounds;
  }

  public String part1Answer() {
    return String.valueOf(this.playGame(this.part1Rounds));
  }

  public String part2Answer() {
    return String.valueOf(this.playGame(this.part2Rounds));
  }

  private int playGame(int numRounds) {
    int[] lastUsage = new int[numRounds];
    BitSet used = new BitSet();

    for (int round = 0; round < input.length - 1; round++) {
      lastUsage[input[round]] = round;
      used.set(input[round]);
    }

    int prevNum = input[input.length - 1];
    int currNum = -1;

    for (int round = input.length; round < numRounds; round++) {
      if (used.get(prevNum)) {
        currNum = round - 1 - lastUsage[prevNum];
      } else {
        currNum = 0;
        used.set(prevNum);
      }
      lastUsage[prevNum] = round - 1;
      prevNum = currNum;
    }

    return currNum;
  }
}

class Main {
  private final static int[] input = {14, 3, 1, 0, 9, 5};

  public static void main(String[] args) {
    try {
      Executor executor = new Executor(new Day15Solution(input, 2020, 30000000));
      executor.run(args);
    } catch (Exception e) {
      System.out.println(e);
      e.printStackTrace();
    }
  }
}
