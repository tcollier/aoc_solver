import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;

class SumNotPossible extends RuntimeException {
    public SumNotPossible(String message) {
        super(message);
    }
}

class Day01 {
    public static int[] pairWithSum(int[] numbers, int sum) {
        int[] pair = new int[2];
        HashSet<Integer> others = new HashSet<Integer>();
        for (int i = 1; i < numbers.length; i++) {
            others.add(numbers[i]);
        }
        for (int i = 0; i < numbers.length - 1; i++) {
            if(others.contains(sum - numbers[i])) {
                pair[0] = numbers[i];
                pair[1] = sum - numbers[i];
                return pair;
            }
        }
        throw new SumNotPossible("Cannot find pair with sum");
    }

    public static int[] tripletWithSum(int[] numbers, int sum) {
        int[] triplet = new int[3];
        Arrays.sort(numbers);
        for (int i = 0; i < numbers.length - 2; i++) {
            int j = i + 1;
            int k = numbers.length - 1;
            while (j < k) {
                int total = numbers[i] + numbers[j] + numbers[k];
                if(total == sum) {
                    triplet[0] = numbers[i];
                    triplet[1] = numbers[j];
                    triplet[2] = numbers[k];
                    return triplet;
                } else if (total < sum) {
                    j++;
                } else {
                    k--;
                }
            }
        }
        triplet[0] = numbers[0];
        triplet[1] = numbers[1];
        triplet[2] = sum;
        throw new SumNotPossible("Cannot find triplet with sum");
    }

    public static int[] loadNumbers(String filename) throws FileNotFoundException, IOException {
        int[] numbers = new int[200];
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        try {
            int index = 0;
            String line = reader.readLine();
            while (line != null) {
                numbers[index] = Integer.parseInt(line);
                line = reader.readLine();
                index++;
            }
            return numbers;
        } finally {
            reader.close();
        }
    }

    public static void main(String[] args) {
        try {
            int[] numbers = loadNumbers("day01_input.txt");
            int[] pair = pairWithSum(numbers, 2020);
            System.out.println(pair[0] * pair[1]);
            int[] triplet = tripletWithSum(numbers, 2020);
            System.out.println(triplet[0] * triplet[1] * triplet[2]);
        } catch (Exception e) {
            System.out.println(e);
            e.printStackTrace();
        }
    }
}
