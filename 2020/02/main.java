import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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

    public boolean part1Valid() {
        int charCount = 0;
        for (int i = 0; i < this.pwd.length(); i++) {
            if (this.pwd.charAt(i) == this.chr) {
                charCount++;
                if (charCount > this.max) {
                    return false;
                }
            }
        }
        return charCount >= this.min;
    }

    public boolean part2Valid() {
        boolean validMin = this.pwd.charAt(this.min - 1) == this.chr;
        boolean validMax = this.pwd.charAt(this.max - 1) == this.chr;
        return validMin != validMax;
    }
}

class Main {
    public static Pattern pattern = Pattern.compile("^(\\d+)-(\\d+) (\\w): (\\w+)");

    public static ArrayList<PasswordRule> loadRules(String filename) throws FileNotFoundException, IOException {
        ArrayList<PasswordRule> items = new ArrayList<PasswordRule>();
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        try {
            String line = reader.readLine();
            while (line != null) {
                Matcher matcher = pattern.matcher(line);
                matcher.find();
                items.add(new PasswordRule(
                    Integer.parseInt(matcher.group(1)),
                    Integer.parseInt(matcher.group(2)),
                    matcher.group(3).charAt(0),
                    matcher.group(4)
                ));
                line = reader.readLine();
            }
            return items;
        } finally {
            reader.close();
        }
    }

    public static int[] countValid(ArrayList<PasswordRule> rules) {
        int[] counts = {0, 0};
        Iterator<PasswordRule> it = rules.iterator();
        while (it.hasNext()) {
            PasswordRule rule = it.next();
            if (rule.part1Valid()) {
                counts[0]++;
            }
            if (rule.part2Valid()) {
                counts[1]++;
            }
        }
        return counts;
    }

    public static void main(String[] args) {
        try {
            ArrayList<PasswordRule> rules = loadRules("2020/02/input.txt");
            int[] validCounts = countValid(rules);
            System.out.println(validCounts[0]);
            System.out.println(validCounts[1]);
        } catch (Exception e) {
            System.out.println(e);
            e.printStackTrace();
        }
    }
}
