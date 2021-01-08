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
  let runningTime = 0;

  for (; continueTiming(i, runningTime); i++) {
    const dataCopy = [...data]
    const startTime = Date.now();
    fn(dataCopy);
    runningTime += Date.now() - startTime;
  }
  return {duration: runningTime * 1000, iterations: i};

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
