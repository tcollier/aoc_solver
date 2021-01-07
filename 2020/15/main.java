import java.util.ArrayList;
import java.util.BitSet;

import tcollier.Executor;
import tcollier.Solution;

class Day15Solution implements Solution<Integer> {
  private int part1Rounds;
  private int part2Rounds;

  public Day15Solution(int part1Rounds, int part2Rounds) {
    this.part1Rounds = part1Rounds;
    this.part2Rounds = part2Rounds;
  }

  public String part1Answer(ArrayList<Integer> input) {
    return String.valueOf(playGame(input, part1Rounds));
  }

  public String part2Answer(ArrayList<Integer> input) {
    return String.valueOf(playGame(input, part2Rounds));
  }

  private int playGame(ArrayList<Integer> input, int numRounds) {
    int[] lastUsage = new int[numRounds];
    BitSet used = new BitSet();

    for (int round = 0; round < input.size() - 1; round++) {
      lastUsage[input.get(round)] = round;
      used.set(input.get(round));
    }

    int prevNum = input.get(input.size() - 1);
    int currNum = -1;

    for (int round = input.size(); round < numRounds; round++) {
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
  private final static int[] rawInput = {14, 3, 1, 0, 9, 5};

  public static void main(String[] args) {
    try {
      ArrayList<Integer> input = new ArrayList<Integer>();
      for (int i = 0; i < rawInput.length; i++) {
        input.add(rawInput[i]);
      }
      Executor<Integer> executor = new Executor<Integer>(new Day15Solution(2020, 30000000), input);
      executor.run(args);
    } catch (Exception e) {
      System.out.println(e);
      e.printStackTrace();
    }
  }
}
