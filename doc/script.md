## Solver Script

I added a script that helps me compile and run my solutions. Once the correct solution is known and saved to `output.txt`, the script will validate the output (to avoid regressions when refactoring) and time the solution. In order to leverage the timing features of the solver script, the solution must be implemented using a [language-specific executor](#language-support).

### Usage

Ensure that the `PYTHONPATH` path variable is set to `<root of this repo>/lib/python` when running the script. I added this to the first example, but will leave it out of all others to aid readability.

```
usage: solver [-h] [-y YEAR] [-d DAY] [-l LANGUAGE [LANGUAGE ...]] [--all]
              [--save]

Run Advent of Code solution for a given year/day in the chosen language

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  competition year (default: <current year in UTC>)
  -d DAY, --day DAY     competition day (default: <current day of month in UTC>)
  -l LANGUAGE [LANGUAGE ...], --language LANGUAGE [LANGUAGE ...]
                        programming language of the solution to run (available
                        languages: c, golang, java, lisp, python, ruby, rust,
                        scala, typescript)
  --all                 run all challenge days in all languages
  --save                save the programs output to output.txt
```

#### Example: run solution for the current day

When providing no arguments to the script, it will execute any source code for the current day's directory, where the current day is determined by UTC time. The default can be overridden by setting the environment variables `YEAR` and `DAY`.

```
% PYTHONPATH=$HOME/aoc/lib/python ./bin/solver
TRY  [2020/01 typescript]
1003971
84035952
```

#### Example: run solution and save known correct solution

Once the solutions for both parts have been verified as correct, you can save the solution using the `--save` flag. This allows you to tweak the implementation and validate against regressions or implement the solution in another language and test along the way.

```
% ./bin/solver --save
TRY  [2020/01 typescript]
1003971
84035952
Saved result to 2020/01/output.txt
```

#### Exampe: run solution with saved correct solution

Once the solution output is saved, rerunning the script (without the `--save` flag) will validate the correctness of the new output and print out timing information. In order to leverage the timing features of the solver script, the solution must be implemented using a [language-specific executor](#language-support).

```
% ./bin/solver --save
PASS [2020/01 typescript] (part1:   6.77 μs, part2:   4.96 μs, overhead:  46.06 ms)
```

The executor running the solution invokes functions specific to each challenge part multiple times and reports on the average clock time taken per invocation (the `part1` and `part2` metrics). Additionally an `overhead` metric reports the total time taken to invoke the shell command minus time spent acutally computing the solution. This includes time spent booting the virtual machine or loading language libraries and can indicate why a "fast" solution might feel slow (I'm looking at you Scala!).
