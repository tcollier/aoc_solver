const solution = require(process.argv[process.argv.length - 1]);

const data = solution.loadData();

console.log(solution.part1Result(data));
console.log(solution.part2Result(data));
