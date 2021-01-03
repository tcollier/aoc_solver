import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;

import tcollier.Executor;
import tcollier.InputLoader;
import tcollier.Solution;

class SumNotPossible extends RuntimeException {
  public SumNotPossible(String message) {
    super(message);
  }
}

class Day1Solution implements Solution {
  private ArrayList<Integer> numbers;
  private int sum;

  public Day1Solution(ArrayList<Integer> numbers, int sum) {
    this.numbers = numbers;
    this.sum = sum;
  }

  public String part1Answer() {
    int[] pair = this.pairWithSum();
    return String.valueOf(pair[0] * pair[1]);
  }

  public String part2Answer() {
    int[] triplet = this.tripletWithSum();
    return String.valueOf(triplet[0] * triplet[1] * triplet[2]);
  }

  private int[] pairWithSum() {
    int[] pair = new int[2];
    HashSet<Integer> others = new HashSet<Integer>();
    for (int i = 1; i < this.numbers.size(); i++) {
      others.add(this.numbers.get(i));
    }
    for (int i = 0; i < this.numbers.size() - 1; i++) {
      if(others.contains(this.sum - this.numbers.get(i))) {
        pair[0] = this.numbers.get(i);
        pair[1] = this.sum - this.numbers.get(i);
        return pair;
      }
    }
    throw new SumNotPossible("Cannot find pair with sum");
  }

  private int[] tripletWithSum() {
    int[] triplet = new int[3];
    Collections.sort(this.numbers);
    for (int i = 0; i < this.numbers.size() - 2; i++) {
      int j = i + 1;
      int k = this.numbers.size() - 1;
      while (j < k) {
        int total = this.numbers.get(i) + this.numbers.get(j) + this.numbers.get(k);
        if(total == this.sum) {
          triplet[0] = this.numbers.get(i);
          triplet[1] = this.numbers.get(j);
          triplet[2] = this.numbers.get(k);
          return triplet;
        } else if (total < this.sum) {
          j++;
        } else {
          k--;
        }
      }
    }
    throw new SumNotPossible("Cannot find triplet with sum");
  }
}

class Main {
  public static void main(String[] args) {
    try {
      ArrayList<Integer> numbers = new InputLoader("2020/01/input.txt").getIntegers();
      Executor executor = new Executor(new Day1Solution(numbers, 2020));
      executor.run(args);
    } catch (Exception e) {
      System.out.println(e);
      e.printStackTrace();
    }
  }
}
