const loadData = (): number[] => [14, 3, 1, 0, 9, 5]

const playGame = (initalNums: number[], numRounds: number): number => {
  const lastUsage = new Map<number, number>();
  for (let round = 0; round < initalNums.length - 1; round++) {
    lastUsage.set(initalNums[round], round);
  }

  let prevNum = initalNums[initalNums.length - 1];
  let currNum = -1;
  for (let round = initalNums.length; round < numRounds; round++) {
    if (lastUsage.has(prevNum)) currNum = round - 1 - lastUsage.get(prevNum);
    else currNum = 0;
    lastUsage.set(prevNum, round - 1);
    prevNum = currNum
  }
  return currNum;
}

const part1Result = (initalNums: number[]): number =>
  playGame(initalNums, 2020);

  const part2Result = (initalNums: number[]): number =>
  playGame(initalNums, 30000000);

export { loadData, part1Result, part2Result };
