extern crate bit_set;
use bit_set::BitSet;

fn play_game(num_rounds: usize) -> usize {
  let input: [usize; 6] = [14, 3, 1, 0, 9, 5];
  let mut last_usage = [0 as usize; 30000000];
  let mut used = BitSet::with_capacity(num_rounds);

  for round in 0..(input.len() - 1) {
    last_usage[input[round]] = round;
    used.insert(input[round]);
  }

  let mut prev_num = input[input.len() - 1];
  let mut curr_num = 0;

  for round in input.len()..num_rounds {
    if used.contains(prev_num) {
      curr_num = round - 1 - last_usage[prev_num];
    } else {
      curr_num = 0;
      used.insert(prev_num);
    }
    last_usage[prev_num] = round - 1;
    prev_num = curr_num;
  }

  return curr_num;
}

fn main() {
  let last_value = play_game(30000000);
  println!("{}", last_value);
}
