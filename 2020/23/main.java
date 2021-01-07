import java.lang.StringBuilder;
import java.util.ArrayList;
import java.util.Arrays;

import tcollier.Executor;
import tcollier.Solution;

class Game {
  private int numRounds;
  private int[] cups;
  private int head;

  public Game(ArrayList<Integer> labels, int numCups, int numRounds) {
    this.numRounds = numRounds;
    this.cups = new int[numCups];

    if (numCups > labels.size()) {
      head = numCups - 1;
    } else {
      head = labels.get(labels.size() - 1) - 1;
    }

    int curr = head;
    int i = 0;
    for (; i < labels.size(); i++) {
      cups[curr] = labels.get(i) - 1;
      curr = labels.get(i) - 1;
    }
    for (; i < numCups; i++) {
      cups[curr] = i;
      curr = i;
    }
  }

  public void play() {
    for (int i = 0; i < numRounds; i++) {
      move();
    }
  }

  private void move() {
    int cup1 = cups[head];
    int cup2 = cups[cup1];
    int cup3 = cups[cup2];
    int cup4 = cups[cup3];
    int[] pickups = {cup2, cup3, cup4};
    cups[cup1] = cups[cup4];

    int dest = cups[head] - 1;
    if (dest < 0) {
        dest = cups.length - 1;
    }
    while (dest == cup2 || dest == cup3 || dest == cup4) {
      dest -= 1;
      if (dest < 0) {
        dest = cups.length - 1;
      }
    }

    int tmp = cups[dest];
    cups[dest] = cup2;
    cups[cup2] = cup3;
    cups[cup3] = cup4;
    cups[cup4] = tmp;

    if (dest == head) {
      head = cup4;
    }

    head = cups[head];
  }

  public int labelAt(int index) {
    return cups[index] + 1;
  }
}

class Day23Solution implements Solution<Integer> {
  public String part1Answer(ArrayList<Integer> labels) {
    Game game = new Game(labels, 9, 100);
    game.play();
    StringBuilder str = new StringBuilder();
    int curr = game.labelAt(0);
    while (curr != 1) {
      str.append(curr);
      curr = game.labelAt(curr - 1);
    }
    return str.toString();
  }

  public String part2Answer(ArrayList<Integer> labels) {
    Game game = new Game(labels, 1000000, 10000000);
    game.play();
    return String.valueOf((long)game.labelAt(0) * (long)game.labelAt(game.labelAt(0) - 1));
  }
}

class Main {
  private static final int[] rawLabels = {1, 9, 8, 7, 5, 3, 4, 6, 2};

  public static void main(String[] args) {
    ArrayList<Integer> labels = new ArrayList<Integer>();
    for (int i = 0; i < rawLabels.length; i++) {
      labels.add(rawLabels[i]);
    }
    Executor<Integer> executor = new Executor<Integer>(new Day23Solution(), labels);
    executor.run(args);
  }
}
