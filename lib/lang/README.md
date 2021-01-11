## Language Support

The files contained within this directory define which languages are supported and the implementation of compilation and execution. To add support for a new language (e.g. `newlang`), create a new file with the following contents

```python
# lib/python/lib/lang/newlang.py
from lib.lang.registry import LanguageSettings, register_language


@register_language(name="newlang", extension="nlg", timing=False)
class NewlangSettings(LanguageSettings):
    def compile(self):
        yield f"newlangc --output {self._bin_file} {self.file}"

    def solve(self):
        return os.path.join(".", self._bin_file)
```

If compilation is not necessary, you can remove the `compile` function. The `register_language` decorator must decorate the class and takes the following arguments

- `name` - the name used to reference the language in the registry, which mirrors the name used in the solver script (e.g. `solver 2000 1 --language newlang`); convention dictates this is one word, all lowercase.
- `extension` - the file extension of source code for the language, the solver script will only look for solutions with this extension.
- `timing` - (defalut `True`) wether solutions in this language support the `--time` flag, which entails printing out timing information (see the [Timing section](#timing) below).

The base `LanguageSettings` class implements a `time` function that simply adds ` --time` to the command returned from `solve`. This function can be overriden if a language requires different options for timing.

See the [java file](java.py) for a more complicated example.

### Executor Pattern

Since the solver script expects a specific format for output in both the standard case of attempting a solution and in the case of timing it, most languages provide an executor class/interface/function. Since every language has its own patterns and nuances, each implmentation will be unique. However, the general arguments to the executor are

- The puzzle input (this is typically a list of numbers or a list of strings)
- References to the part 1 and part 2 solution functions
- The command line arguments (currently only the `--time` optional is supported)

The solver script will call the executable (as defined in either `NewlangSettings#solve` or `NewlangSettings#time`) in a new shell. Thus solutions must be implemented using the standard entry point for the language (e.g. a `main` function)

#### Solving

When the executor is invoked without the `--time` flag, it should print the attempted solution of part 1 on a line, then part 2 on a second line, e.g. if the output for part 1 is `314` and for part 2 is `525600`, then the following should be printed

```
314
525600
```

#### Timing

After the solver script attempts a solution, if the output matches the known good solution and the language was registered with `timing=True`, then the script will invoke the solution again with the `--time` flag. The output of this should be a single JSON-encoded string in a single line of the form

```json
{ "part1": { "iterations": 1234, "duration": 999784 }, "part1": { "iterations": 567, "duration": 394555 } }
```

- `iterations` - number of times the part-specific solution was invoked in the timing loop
- `duration` - total time (in microseconds) it took to invoke all iterations of the solver function

##### Input Handling

It is important to ensure the input passed to solver function is the same raw input each time. For example, if a solver function sorts the input in place, the next time the function is invoked, it should get the input in the original order. This often requires copying the original input before passing it into the solver function. In order to not penalize a solution for this copy procedure, the time spent copying should not be included in the total duration. Pseudocode for this looks like

```
iterations = 0
running_time = 0
# see below for guidance on implementation of `continue_timing?`
while continue_timing?(iterations, running_time)
  copy_of_input = input.copy
  start_time = now()  # if the time isn't in microseconds, it will need to be converted
  solver_function(copy_of_input)
  running_time += now() - start_time
  iterations += 1
end
```

##### Number of Iterations

To ensure a statistically significant number of iterations in the timing loop, the following logic is used in most executors

```
def continue_timing?(iterations, running_time)
  if iterations < 100
    return duration < 30_000_000
  else
    return duration < 100_000
  end
end
```
