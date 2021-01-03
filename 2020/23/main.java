import java.lang.StringBuilder;
import java.util.Arrays;

import tcollier.Executor;
import tcollier.Solution;

class Game {
  private int numRounds;
  private int[] cups;
  private int head;

  public Game(int[] labels, int numCups, int numRounds) {
    this.numRounds = numRounds;
    this.cups = new int[numCups];

    if (numCups > labels.length) {
      this.head = numCups - 1;
    } else {
      this.head = labels[labels.length - 1] - 1;
    }

    int curr = this.head;
    int i = 0;
    for (; i < labels.length; i++) {
      this.cups[curr] = labels[i] - 1;
      curr = labels[i] - 1;
    }
    for (; i < numCups; i++) {
      this.cups[curr] = i;
      curr = i;
    }
  }

  public void play() {
    for (int i = 0; i < this.numRounds; i++) {
      this.move();
    }
  }

  private void move() {
    int cup1 = this.cups[this.head];
    int cup2 = this.cups[cup1];
    int cup3 = this.cups[cup2];
    int cup4 = this.cups[cup3];
    int[] pickups = {cup2, cup3, cup4};
    this.cups[cup1] = this.cups[cup4];

    int dest = this.cups[this.head] - 1;
    if (dest < 0) {
        dest = this.cups.length - 1;
    }
    while (dest == cup2 || dest == cup3 || dest == cup4) {
      dest -= 1;
      if (dest < 0) {
        dest = this.cups.length - 1;
      }
    }

    int tmp = this.cups[dest];
    this.cups[dest] = cup2;
    this.cups[cup2] = cup3;
    this.cups[cup3] = cup4;
    this.cups[cup4] = tmp;

    if (dest == this.head) {
      this.head = cup4;
    }

    this.head = this.cups[this.head];
  }

  public int labelAt(int index) {
    return this.cups[index] + 1;
  }
}

class Day23Solution implements Solution {
  private Game game1;
  private Game game2;

  public Day23Solution(Game game1, Game game2) {
    this.game1 = game1;
    this.game2 = game2;
  }

  public String part1Answer() {
    this.game1.play();
    StringBuilder str = new StringBuilder();
    int curr = this.game1.labelAt(0);
    while (curr != 1) {
      str.append(curr);
      curr = this.game1.labelAt(curr - 1);
    }
    return str.toString();
  }

  public String part2Answer() {
    this.game2.play();
    return String.valueOf((long)this.game2.labelAt(0) * (long)this.game2.labelAt(this.game2.labelAt(0) - 1));
  }
}

class Main {
  private static final int[] labels = {1, 9, 8, 7, 5, 3, 4, 6, 2};

  public static void main(String[] args) {
    try {
      Executor executor = new Executor(
        new Day23Solution(
          new Game(labels, 9, 100),
          new Game(labels, 1000000, 10000000)
        )
      );
      executor.run(args);
    } catch (Exception e) {
      System.out.println(e);
      e.printStackTrace();
    }
  }
}
