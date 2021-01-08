use std::env;

mod util;

struct Day0Solution {
  input: Vec<String>
}

impl util::Solution for Day0Solution {
  fn part1_result(&self) -> String {
    self.input[0].to_string()
  }

  fn part2_result(&self) -> String {
    self.input[1].to_string()
  }
}

fn main() {
  let input = vec!["Hello".to_string(), "World!".to_string()];
  let solution = Day0Solution { input: input };
  let executor = util::Executor::new(&solution as &util::Solution);
  let args = env::args().collect();
  executor.run(args);
}
