import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import tcollier.Executor;
import tcollier.InputLoader;
import tcollier.Solution;

class PasswordRule {
  public int min;
  public int max;
  public char chr;
  public String pwd;

  public PasswordRule(int min, int max, char chr, String pwd) {
    this.min = min;
    this.max = max;
    this.chr = chr;
    this.pwd = pwd;
  }
}

interface Validator {
  public boolean isValid(PasswordRule rule);
}

class Part1Validator implements Validator {
  public boolean isValid(PasswordRule rule) {
    int charCount = 0;
    for (int i = 0; i < rule.pwd.length(); i++) {
      if (rule.pwd.charAt(i) == rule.chr) {
        charCount++;
        if (charCount > rule.max) {
          return false;
        }
      }
    }
    return charCount >= rule.min;
  }
}

class Part2Validator implements Validator {
  public boolean isValid(PasswordRule rule) {
    boolean validMin = rule.pwd.charAt(rule.min - 1) == rule.chr;
    boolean validMax = rule.pwd.charAt(rule.max - 1) == rule.chr;
    return validMin != validMax;
  }
}

class Day2Solution implements Solution {
  private static Pattern rulePattern = Pattern.compile("^(\\d+)-(\\d+) (\\w): (\\w+)");

  private ArrayList<PasswordRule> rules;

  public Day2Solution(ArrayList<String> rawRules) {
    this.rules = parseRules(rawRules);
  }

  public String part1Answer() {
    return String.valueOf(countValid(new Part1Validator()));
  }

  public String part2Answer() {
    return String.valueOf(countValid(new Part2Validator()));
  }

  private int countValid(Validator validator) {
    int count = 0;
    Iterator<PasswordRule> it = this.rules.iterator();
    while (it.hasNext()) {
      if (validator.isValid(it.next())) {
        count++;
      }
    }
    return count;
  }

  private static ArrayList<PasswordRule> parseRules(ArrayList<String> rawRules) {
    ArrayList<PasswordRule> rules = new ArrayList<PasswordRule>();
    Iterator it = rawRules.iterator();
    while (it.hasNext()) {
      Matcher matcher = rulePattern.matcher((String)it.next());
      matcher.find();
      rules.add(new PasswordRule(
        Integer.parseInt(matcher.group(1)),
        Integer.parseInt(matcher.group(2)),
        matcher.group(3).charAt(0),
        matcher.group(4)
      ));
    }
    return rules;
  }
}

class Main {
  public static void main(String[] args) {
    try {
      ArrayList<String> rawRules = new InputLoader("2020/02/input.txt").getStrings();
      Executor executor = new Executor(new Day2Solution(rawRules));
      executor.run(args);
    } catch (Exception e) {
      System.out.println(e);
      e.printStackTrace();
    }
  }
}
