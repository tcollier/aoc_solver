use std::time::{Instant};

pub trait Solution {
  fn part1_result(&self) -> String;
  fn part2_result(&self) -> String;
}

pub struct Executor<'a> {
  solution: &'a (Solution + 'a)
}

struct TimingInfo {
  iterations: u64,
  duration: u64,
}

fn continue_timing(iterations: u64, start: Instant) -> bool {
  if iterations < 100 {
    return start.elapsed().as_secs() < 30;
  } else {
    return start.elapsed().subsec_nanos() < 100000000;
  }
}

fn time_func<F>(f: F) -> TimingInfo where
  F: Fn() -> String {
  let start = Instant::now();
  let mut i: u64 = 0;
  while continue_timing(i, start) {
    f();
    i += 1;
  }
  return TimingInfo {
    iterations: i,
    duration: start.elapsed().as_secs() * 1000000 + (start.elapsed().subsec_nanos() as u64) / 1000
  }
}

impl<'a> Executor<'a> {
  pub fn new(solution: &'a Solution) -> Executor<'a> {
    Executor { solution: solution }
  }

  pub fn run(&self, args: Vec<String>) {
    if args.len() > 0 && args[args.len() - 1] == "--time" {
      let part1 = || self.solution.part1_result();
      let part1_ti = time_func(part1);
      let part2 = || self.solution.part2_result();
      let part2_ti = time_func(part2);
      println!("{{\"part1\":{{\"duration\":{},\"iterations\":{}}},\"part2\":{{\"duration\":{},\"iterations\":{}}}}}", part1_ti.duration,part1_ti.iterations, part2_ti.duration, part2_ti.iterations);
    } else {
      println!("{}", self.solution.part1_result());
      println!("{}", self.solution.part2_result());
    }
  }
}
