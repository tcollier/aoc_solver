const timing = process.argv[process.argv.length - 1] === "--time";

const solFile = process.argv[process.argv.length - timing ? 2 : 1];
const solution = require(solFile);

const data = solution.loadData();

const continueTiming = (iterations, durationMillis) => {
  if (iterations < 100) {
    return durationMillis < 30000;
  } else {
    return durationMillis < 100;
  }
}

const timeIt = (fn, data) => {
  let i = 0;
  const startTime = Date.now();

  for (; continueTiming(i, Date.now() - startTime); i++) {
    fn(data);
  }
  return {duration: (Date.now() - startTime) * 1000, iterations: i};

}
if (timing) {
  console.log(JSON.stringify({
    part1: timeIt(solution.part1Result, data),
    part2: timeIt(solution.part2Result, data)}
  ));
} else {
  console.log(solution.part1Result(data));
  console.log(solution.part2Result(data));
}
