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

class Day1Solution implements Solution<Integer> {
  private int sum;

  public Day1Solution(int sum) {
    this.sum = sum;
  }

  public String part1Answer(ArrayList<Integer> numbers) {
    int[] pair = pairWithSum(numbers);
    return String.valueOf(pair[0] * pair[1]);
  }

  public String part2Answer(ArrayList<Integer> numbers) {
    int[] triplet = tripletWithSum(numbers);
    return String.valueOf(triplet[0] * triplet[1] * triplet[2]);
  }

  private int[] pairWithSum(ArrayList<Integer> numbers) {
    int[] pair = new int[2];
    HashSet<Integer> others = new HashSet<Integer>();
    for (int i = 1; i < numbers.size(); i++) {
      others.add(numbers.get(i));
    }
    for (int i = 0; i < numbers.size() - 1; i++) {
      if(others.contains(sum - numbers.get(i))) {
        pair[0] = numbers.get(i);
        pair[1] = sum - numbers.get(i);
        return pair;
      }
    }
    throw new SumNotPossible("Cannot find pair with sum");
  }

  private int[] tripletWithSum(ArrayList<Integer> numbers) {
    Collections.sort(numbers);
    int[] triplet = new int[3];
    for (int i = 0; i < numbers.size() - 2; i++) {
      int j = i + 1;
      int k = numbers.size() - 1;
      while (j < k) {
        int total = numbers.get(i) + numbers.get(j) + numbers.get(k);
        if(total == sum) {
          triplet[0] = numbers.get(i);
          triplet[1] = numbers.get(j);
          triplet[2] = numbers.get(k);
          return triplet;
        } else if (total < sum) {
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
      Executor<Integer> executor = new Executor<Integer>(new Day1Solution(2020), numbers);
      executor.run(args);
    } catch (Exception e) {
      System.out.println(e);
      e.printStackTrace();
    }
  }
}
