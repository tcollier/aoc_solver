const input = [14, 3, 1, 0, 9, 5];

const playGame = (input: number[], numRounds: number): number => {
  const lastUsage = new Map<number, number>();
  for (let round = 0; round < input.length - 1; round++) {
    lastUsage.set(input[round], round);
  }

  let prevNum = input[input.length - 1];
  let currNum = -1;
  for (let round = input.length; round < numRounds; round++) {
    if (lastUsage.has(prevNum)) currNum = round - 1 - lastUsage.get(prevNum);
    else currNum = 0;
    lastUsage.set(prevNum, round - 1);
    prevNum = currNum
  }
  return currNum;
}

const part1Result = (): number =>
  playGame(input, 2020);

  const part2Result = (): number =>
  playGame(input, 30000000);

export { part1Result, part2Result };
