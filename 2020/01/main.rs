use std::collections::HashSet;
use std::fs;

type Number = u16;
type Product = u64;

type Pair = (Number, Number);
type Triplet = (Number, Number, Number);

fn pair_with_sum(numbers: &Vec<Number>, sum: Number) -> Pair {
  let mut others: HashSet<Number> = HashSet::new();
  for i in 1..numbers.len() {
    others.insert(numbers[i]);
  }
  for i in 0..(numbers.len() - 1) {
    if others.contains(&(sum - numbers[i])) {
      return (numbers[i], sum - numbers[i]);
    }
  }
  panic!("Pair not found");
}

fn triplet_with_sum(numbers: &Vec<Number>, sum: Number) -> Triplet {
  for i in 0..numbers.len() {
    let mut j = i + 1;
    let mut k = numbers.len() - 1;
    while j < k {
      let total = numbers[i] + numbers[j] + numbers[k];
      if total == sum {
        return (numbers[i], numbers[j], numbers[k]);
      } else if total < sum {
        j += 1
      } else {
        k -= 1
      }
    }
  }
  panic!("Triplet not found")
}

fn main() {
  let mut numbers: Vec<Number> = Vec::new();
  let contents = fs::read_to_string("./2020/01/input.txt").expect("File not found");
  for line in contents.lines() {
      numbers.push(line.parse::<Number>().unwrap());
  }

  let pair = pair_with_sum(&numbers, 2020);
  println!("{}", (pair.0 as Product) * (pair.1 as Product));

  numbers.sort();
  let triplet = triplet_with_sum(&numbers, 2020);
  println!("{}", (triplet.0 as Product) * (triplet.1 as Product) * (triplet.2 as Product));
}
