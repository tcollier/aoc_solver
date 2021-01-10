## Language Support

The languages currently have some level of support in the `solver` script. Most contain an executor that is compatible with performance timing, but some do not. To add support for a new language, see the [adding laguage support documentation](../lib/python/lib/lang/README.md).

### C

C source code is compiled with `gcc` without any fancy options or libraries.

### Timing Support

A c executor exists with the following signature

```c
void executor(
    char *input[],
    char *(*part1_fn)(char **),
    char *(*part2_fn)(char **),
    int argc,
    char *argv[]);
```

Below is template code for using the executor

```c
// main.c
#include "../../lib/c/lib.h"

char *part1_result(char *input[])
{
  // compute part 1 solution
  return solution;
}

char *part2_result(char *input[])
{
  // compute part 2 solution
  return solution;
}

int main(int argc, char *argv[])
{
  // load challenge input
  executor(input, part1_result, part2_result, argc, argv);
}
```

### Golang

**IMPORTANT**: To compile golang code, set your `GOPATH` to the `lib/go` directory of this repository

### Timing Support

A golang executor exists with the following signature

```go
type Input interface{}

type solverFunc func(Input) string

func Executor(input Input, part1 solverFunc, part2 solverFunc, args []string)
```

Below is template code for using the executor

```go
package main

import (
	"os"

	"aoc.com/tcollier"
)

func part1Answer(input tcollier.Input) string {
	return // the answer
}

func part2Answer(input tcollier.Input) string {
	return // the answer
}

func main() {
  var input = // load input
	tcollier.Executor(input, part1Answer, part2Answer, os.Args)
}
```

### Java

### Timing Support

A Java executor exists with the following signature

```java
public interface Solution<T> {
  public String part1Answer(ArrayList<T>);
  public String part2Answer(ArrayList<T>);
}

public class Executor {
  public Executor(Solution<T> solution, ArrayList<T> input);
  public void run(String[] args);
}
```

Below is template code for using the executor

```java
// Main.java
import java.util.ArrayList;

import tcollier.Executor;
import tcollier.Solution;

class Day1Solution implements Solution<String> {
  private ArrayList<String> input;

  public String part1Answer(ArrayList<String> input) {
    // compute part 1 solution
    return solution
  }

  public String part2Answer(ArrayList<String> input) {
    // compute part 2 solution
    return solution
  }
}

class Main {
  public static void main(String[] args) {
    ArrayList<String> input = // load input
    Executor executor = new Executor(new Day1Solution(), input);
    executor.run(args);
  }
}
```

### Lisp

`solver` will run a solution in `main.lisp` using `sbcl` ([download from sbcl.org](http://www.sbcl.org/) or install with HomeBrew).

### Timing Support

Below is template code for using the executor

```lisp
(load "lib/lisp/executor.lisp")

(defun part1 (input)
  (car input)
)

(defun part2 (input)
  (car (cdr input))
)

(executor (list "Hello" "World!") #'part1 #'part2 *posix-argv*)
```

### Python

### Timing Support

A python executor exists, below is template code for using the executor

```python
# main.py
import sys

from lib.executor import Executor


def part1_solution(input):
    # compute part 1 solution
    return solution


def part2_solution(input):
    # compute part 2 solution
    return solution

input = # load input
executor = Executor(input, part1_solution, part2_solution)
executor(sys.argv)
```

### Ruby

### Timing Support

A ruby executor exists, below is template code for using the executor

```ruby
# main.rb
require_relative '../../lib/ruby/executor'

part1_proc = Proc.new { |input| compute_part1_solution(input) }
part2_proc = Proc.new { |input| compute_part2_solution(input) }
executor = Executor.new(load_input, part1_proc, part2_proc)
executor.run(ARGV)
```

### Rust

### Timing Support

**IMPORTANT**: The executor code needs to be soft linked from the challenge day directory in order for rustc to compile correctly, e.g.

```
% cd 2020/01
% ln -s ../../lib/rust/util.rs
```

Below is template code for using the executor

```rs
// main.rs
use std::env;

mod util;

struct Day1Solution {
  input: Vec<String>
}

impl util::Solution for Day1Solution {
  fn part1_result(&self) -> String {
    // compute and return part 1 solution
  }

  fn part2_result(&self) -> String {
    // compute and return part 2 solution
  }
}

fn main() {
  let input = // load input
  let solution = Day1Solution { input: input };
  let executor = util::Executor::new(&solution as &util::Solution);
  let args = env::args().collect();
  executor.run(args);
}
```

### Scala

### Timing Support

A scala executor exists, below is template code for using the executor

```scala
import tcollier.Executor;
import tcollier.Solution;

class Day1Solution() extends Solution {
  def part1Answer(): String = {
    // compute part 1 solution
    return solution
  }

  def part2Answer(): String = {
    // compute part 2 solution
    return solution
  }
}

object Main {
  def main(args: Array[String]): Unit = {
    val input: Array[String] = // load input
    val executor: Executor = new Executor(new Day0Solution(input), input);
    executor.run(args);
  }
}
```

### Typescript

### Requirements

The `solver` script uses `node` to compile typescript files and run the compiled javascript. Ensure `node` and `npm` are installed.

### Timing Support

A typescript executor exists, below is template code for using the executor

```ts
// main.ts
const loadData = (): string[] => // load input

const part1Result = (words: string[]): string => {
  // compute and return part 1 solution
}

const part2Result = (words: string[]): string => {
  // compute and return part 2 solution
}

export { loadData, part1Result, part2Result }
```
