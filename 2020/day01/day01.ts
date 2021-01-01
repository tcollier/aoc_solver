const fs = require('fs');

type Pair = [number, number];
type Triplet = [number, number, number];

const pairWithSum = (numbers: number[], sum: number): Pair => {
  let others: Set<number> = new Set();
  for (let i = 1; i < numbers.length; i++) {
    others.add(numbers[i]);
  }
  for (let i = 0; i < numbers.length - 1;i++) {
    if (others.has(sum - numbers[i])) {
      return [numbers[i], sum - numbers[i]];
    }
  }
  throw new Error(`No pair with sum ${sum} found`);
}

const tripletWithSum = (numbers: number[], sum: number): Triplet => {
  numbers.sort((a, b) => a - b);
  for (let i = 0; i < numbers.length - 2; i++) {
    let j = i + 1;
    let k = numbers.length - 1;
    while (j < k) {
      const total = numbers[i] + numbers[j] + numbers[k];
      if (total === sum) {
        return [numbers[i], numbers[j], numbers[k]];
      } else if (total < sum) {
        j++;
      } else {
        k--;
      }
    }
  }
  throw new Error(`No triplet with sum ${sum} found`);
}

const loadNumbers = (): number[] =>
  fs.readFileSync('./2020/day01/day01_input.txt', 'utf8').split("\n").map(l => parseInt(l));

const part1Result = (): number => {
  const pair = pairWithSum(loadNumbers(), 2020);
  return pair[0] * pair[1];

}

const part2Result = (): number => {
  const triplet = tripletWithSum(loadNumbers(), 2020);
  return triplet[0] * triplet[1] * triplet[2];
}

export { part1Result, part2Result }
