# Advent of Code

This repository is my collection of solutions for [Advent of Code](https://adventofcode.com/) coding challenges. I've tackled challenges using [various languages](doc/languages.md) and have added several utilities for building, running, and timing (yes, performance matters!) my solutions.

## Structure

Solutions to daily challenges live in a subdirectory for the given challenge date (`YYYY/DD/`), some subdirectories contain solutions in multiple languages. The solver script only looks for solutions named `main.xxx` or `Main.xxx` (where `xxx` is the standard file extension for the language).

For consistency's sake, each solution prints out 2 lines, the first is the answer to part 1 and the second to part 2. Daily subdirectories may also contain a file with my input (`input.txt`) for the challenge and and a file with the correct anwsers (`output.txt`) for my given input. Some days have very simple input, in which case the input may be hard-coded in the source file.

For example, you can find the following solutions (along with my input and correct solutions) for the challenge on day 15 of Advent of Code in 2020

```
+-- 2020
  +-- 15
    +-- input.txt
    +-- Main.java
    +-- main.py
    +-- main.rb
    +-- output.txt
```

## Solver Script

I added a script that helps me compile and run my solutions. Once the correct solution is known and saved to `output.txt`, the script will validate the output (to avoid regressions when refactoring) and time the solution. In order to leverage the timing features of the solver script, the solution must be implemented using a [language-specific executor](doc/languages.md).

With basic usage, you can easily compile (if necessary) and run your solutions

```
% PYTHONPATH=$HOME/aoc/lib/python ./bin/solver
TRY  [2020/01 typescript]
1003971
84035952
```

See [Script](doc/script.md) documentation for more details and examples.

## Language Support

Below is a list of currently supported langauges, see the [Language Support](doc/languages.md) documetation for more details

- [C](doc/languages.md#c)
- [Golang](doc/languages.md#golang)
- [Java](doc/languages.md#java)
- [Lisp](doc/languages.md#lisp)
- [Python](doc/languages.md#python)
- [Ruby](doc/languages.md#ruby)
- [Rust](doc/languages.md#rust)
- [Scala](doc/languages.md#scala)
- [Typescript](doc/languages.md#typescript)

## Playground

Some of the challenges spark ideas for experimentation that might not be a great fit for that challenge (e.g. my own [hash map implementation](playground/hash_map.rb)). The `playground` directory is a warehouse of code snippets for my tangential adventures.
