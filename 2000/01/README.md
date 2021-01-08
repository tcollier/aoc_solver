## Day 1

This directory contains "Hello, World" solutions for every supported language as reference implementations I can easily test with. The timing metrics also provide a good baseline for how fast a solution could be in a given language.

Notice the performance differences between java and python despite the fact that both solutions are just returning a string passed in. Also notice that while scala can "compute" the solution just as fast as any other language, it takes nearly half a second just to spin up the VM.

## Solution Performance

```
PASS [2020/00 c         ] (part1:  36.51 ns, part2:  37.46 ns, overhead:   5.14 ms)
PASS [2020/00 golang    ]
PASS [2020/00 java      ] (part1:  26.63 ns, part2:  25.02 ns, overhead:  89.16 ms)
PASS [2020/00 lisp      ]
PASS [2020/00 python    ] (part1: 944.47 ns, part2: 944.58 ns, overhead:  38.98 ms)
PASS [2020/00 ruby      ] (part1: 378.63 ns, part2: 378.82 ns, overhead: 156.04 ms)
PASS [2020/00 rust      ] (part1: 180.71 ns, part2: 181.09 ns, overhead:  10.66 ms)
PASS [2020/00 scala     ] (part1:  26.31 ns, part2:  24.54 ns, overhead: 413.41 ms)
PASS [2020/00 typescript] (part1:  56.31 ns, part2:  60.08 ns, overhead:  49.85 ms)
```
