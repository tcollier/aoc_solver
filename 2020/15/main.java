import java.util.BitSet;

class Main {
  private final static int[] input = {14, 3, 1, 0, 9, 5};

  private static int playGame(int numRounds) {
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

  public static void main(String[] args) {
    System.out.println(playGame(2020));
    System.out.println(playGame(30000000));
  }
}
