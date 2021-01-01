import java.lang.StringBuilder;
import java.util.Arrays;

class Game {
  private int[] cups;
  private int head;

  public Game(int[] labels, int numCups) {
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

  public void move() {
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

class Main {
  private static final int[] labels = {1, 9, 8, 7, 5, 3, 4, 6, 2};

  public static void main(String[] args) {
    Game game1 = new Game(labels, 9);
    for (int i = 0; i < 100; i++) {
      game1.move();
    }
    StringBuilder str = new StringBuilder();
    int curr = game1.labelAt(0);
    while (curr != 1) {
      str.append(curr);
      curr = game1.labelAt(curr - 1);
    }
    System.out.println(str.toString());

    Game game2 = new Game(labels, 1000000);
    for (int i = 0; i < 10000000; i++) {
      game2.move();
    }
    System.out.println((long)game2.labelAt(0) * (long)game2.labelAt(game2.labelAt(0) - 1));
  }
}
