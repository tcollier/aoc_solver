## Solver Script

I added a script that helps me compile and run my solutions. Once the correct solution is known and saved to `output.txt`, the script will validate the output (to avoid regressions when refactoring) and time the solution. In order to leverage the timing features of the solver script, the solution must be implemented using a [language-specific executor](languages.md).

### Usage

```
usage: solver [-h] [-l LANGUAGE [LANGUAGE ...]] [--save] year [day]

Run Advent of Code solution for a given year/day in the chosen language

positional arguments:
  year                  competition year
  day                   competition day

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE [LANGUAGE ...], --language LANGUAGE [LANGUAGE ...]
                        programming language of the solution to run (available
                        languages: c, golang, haskell, java, kotlin, lisp,
                        python, ruby, rust, scala, typescript)
  --save                save the programs output to output.txt
```

#### Required environment vairables

Ensure that the following environment variables are set

- `AOC_SOLUTIONS_PATH` -- absolute path to the base directory containing all solutions (the expected path to a solution is `$AOC_SOLUTIONS_PATH/<YYYY>/<DD>/main.<ext>`)

#### Example: run solution for a single day

```
% ./bin/solver -y 2020 -d 1
TRY  [2020/01 typescript]
1003971
84035952
```

#### Example: run solution and save known correct solution

Once the solutions for both parts have been verified as correct, you can save the solution using the `--save` flag. This allows you to tweak the implementation and validate against regressions or implement the solution in another language and test along the way.

```
% ./bin/solver -y 2020 -d 1 --save
TRY  [2020/01 typescript]
1003971
84035952
Saved result to 2020/01/output.txt
```

#### Exampe: run solution with saved correct solution

Once the solution output is saved, rerunning the script (without the `--save` flag) will validate the correctness of the new output and print out timing information. In order to leverage the timing features of the solver script, the solution must be implemented using a [language-specific executor](languages.md).

```
% ./bin/solver -y 2020 -d 1
PASS [2020/01 typescript] (part1:   6.77 μs, part2:   4.96 μs, overhead:  46.06 ms)
```

The executor running the solution invokes functions specific to each challenge part multiple times and reports on the average clock time taken per invocation (the `part1` and `part2` metrics). Additionally an `overhead` metric reports the total time taken to invoke the shell command minus time spent acutally computing the solution. This includes time spent booting the virtual machine or loading language libraries and can indicate why a "fast" solution might feel slow (I'm looking at you Scala!).

If the computed solution does _not_ match `output.txt`, then a diff is shown

```
% ./bin/solver -y 2020 -d 1
FAIL [2020/01 typescript]
           Part 2
Expected  84035952
Actual    84035953
```
