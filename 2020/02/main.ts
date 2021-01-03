const fs = require('fs');

const loadData = (): string[] =>
  fs.readFileSync('./2020/02/input.txt', 'utf8').split("\n");


const validPart1 = (min: number, max: number, char: string, pwd: string): boolean => {
  let charCount = 0;
  for (let i = 0; i < pwd.length; i++) {
    if (pwd[i] == char) {
      charCount++;
      if (charCount > max) return false;
    }
  }
  return charCount >= min;
}

const validPart2 = (min: number, max: number, char: string, pwd: string): boolean => {
  const minValid = pwd[min - 1] == char;
  const maxValid = pwd[max - 1] == char;
  return minValid != maxValid;
}

const countValid = (rules: string[], validator: Function): number => {
  let count = 0;
  let regex = /^(\d+)-(\d+) (\w): (\w+)/;
  for (let i = 0; i < rules.length; i++) {
    const match = regex.exec(rules[i]);
    if (match && validator(match[1], match[2], match[3], match[4])) {
      count++;
    }
  }
  return count;
}

const part1Result = (rules: string[]) => countValid(rules, validPart1)

const part2Result = (rules: string[]) => countValid(rules, validPart2)

export { loadData, part1Result, part2Result }
