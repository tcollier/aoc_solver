## 2020

That was one hell of a year! Thankfully we had Advent of Code to get us through the home stretch.
Despite a late start (I didn't get to days 1 - 12 until the 12th), I started the latter half of the challenges on time (midnight EST) and worked with some friends over a Google Meet.

## Solution Performance

Since performance varied wildly from day to day (day 0 solutions were all in the nanoseconds range, whereas day 22's python solution took 17 seconds!), pay close attention to the unit of measure for each metric in the list below.

```
PASS [2020/00 c         ] (part1:  29.06 ns, part2:  29.01 ns, overhead:  12.82 ms)
PASS [2020/00 golang    ]
PASS [2020/00 java      ] (part1:  27.17 ns, part2:  26.72 ns, overhead: 431.41 ms)
PASS [2020/00 lisp      ]
PASS [2020/00 python    ] (part1: 593.47 ns, part2: 607.20 ns, overhead: 424.85 ms)
PASS [2020/00 ruby      ] (part1: 363.34 ns, part2: 358.78 ns, overhead: 478.14 ms)
PASS [2020/00 rust      ] (part1: 114.96 ns, part2: 115.34 ns, overhead:  13.29 ms)
PASS [2020/00 scala     ] (part1:  26.61 ns, part2:  26.61 ns, overhead: 609.37 ms)
PASS [2020/00 typescript] (part1:  57.49 ns, part2:  62.48 ns, overhead:  51.98 ms)
PASS [2020/01 c         ] (part1:   2.98 μs, part2:   3.52 μs, overhead:  10.88 ms)
PASS [2020/01 golang    ]
PASS [2020/01 java      ] (part1:   5.21 μs, part2:   9.10 μs, overhead: 121.08 ms)
PASS [2020/01 lisp      ]
PASS [2020/01 python    ] (part1:   5.18 μs, part2:  43.93 μs, overhead: 162.81 ms)
PASS [2020/01 ruby      ] (part1:  26.64 μs, part2:  20.77 μs, overhead: 175.08 ms)
PASS [2020/01 rust      ] (part1:   8.60 μs, part2:   3.68 μs, overhead:   4.96 ms)
PASS [2020/01 scala     ] (part1:   1.46 μs, part2:   1.46 μs, overhead: 475.41 ms)
PASS [2020/01 typescript] (part1:   7.38 μs, part2:   5.00 μs, overhead:  49.06 ms)
PASS [2020/02 java      ] (part1: 847.46 μs, part2: 411.52 μs, overhead: 120.59 ms)
PASS [2020/02 python    ] (part1:   2.41 ms, part2:   1.86 ms, overhead:  44.75 ms)
PASS [2020/02 ruby      ] (part1:   3.36 ms, part2:   1.90 ms, overhead: 179.28 ms)
PASS [2020/02 typescript] (part1: 343.64 μs, part2: 200.00 μs, overhead:  47.58 ms)
PASS [2020/03 python    ] (part1: 618.53 μs, part2: 823.60 μs, overhead:  39.67 ms)
PASS [2020/04 python    ] (part1:   1.05 ms, part2:   3.42 ms, overhead:  46.99 ms)
PASS [2020/05 python    ] (part1: 923.17 μs, part2: 948.65 μs, overhead:  47.00 ms)
PASS [2020/06 python    ] (part1:   1.42 ms, part2:   1.50 ms, overhead:  42.37 ms)
PASS [2020/07 python    ] (part1:   4.16 ms, part2:   3.57 ms, overhead:  42.99 ms)
PASS [2020/08 python    ] (part1: 115.26 μs, part2:  14.71 ms, overhead:  54.11 ms)
PASS [2020/09 python    ] (part1: 533.11 μs, part2:  10.17 ms, overhead:  42.63 ms)
PASS [2020/10 python    ] (part1:  19.63 μs, part2:  93.78 μs, overhead:  59.77 ms)
PASS [2020/11 python    ] (part1:   3.49 s,  part2:   2.45 s,  overhead:  46.39 ms)
PASS [2020/12 python    ] (part1: 540.66 μs, part2: 552.18 μs, overhead:  46.42 ms)
PASS [2020/13 python    ] (part1:   7.52 μs, part2: 120.28 μs, overhead:  58.83 ms)
PASS [2020/14 python    ] (part1:   2.16 ms, part2:  64.10 ms, overhead:  39.06 ms)
PASS [2020/15 java      ] (part1:  10.39 μs, part2: 538.80 ms, overhead: 376.99 ms)
PASS [2020/15 python    ] (part1: 302.00 μs, part2:   8.90 s,  overhead:  41.35 ms)
PASS [2020/15 ruby      ] (part1: 246.53 μs, part2:   4.94 s,  overhead: 206.16 ms)
PASS [2020/15 typescript] (part1:  60.98 μs, part2:   5.48 s,  overhead: 168.43 ms)
PASS [2020/16 python    ] (part1:   3.27 ms, part2:  16.15 ms, overhead:  41.12 ms)
PASS [2020/17 python    ] (part1: 163.66 ms, part2:   4.66 s,  overhead:  48.89 ms)
PASS [2020/18 python    ] (part1:  17.35 ms, part2:  19.17 ms, overhead:  48.86 ms)
PASS [2020/18 ruby      ] (part1:   3.02 ms, part2:   3.21 ms, overhead: 167.65 ms)
PASS [2020/19 python    ] (part1:   3.82 ms, part2:  18.24 ms, overhead:  50.46 ms)
PASS [2020/20 python    ] (part1:   5.60 ms, part2: 118.04 ms, overhead:  52.85 ms)
PASS [2020/21 python    ] (part1: 794.13 μs, part2: 721.42 μs, overhead:  38.54 ms)
PASS [2020/22 python    ] (part1:  96.53 μs, part2:  18.96 s,  overhead:  36.62 ms)
PASS [2020/23 java      ] (part1:   1.62 μs, part2: 375.95 ms, overhead: 167.49 ms)
PASS [2020/23 python    ] (part1:  80.76 μs, part2:  11.94 s,  overhead:  40.51 ms)
PASS [2020/24 python    ] (part1:  26.70 ms, part2: 889.84 ms, overhead:  35.39 ms)
PASS [2020/25 python    ] (part1: 309.99 ms, part2: 581.75 ns, overhead: 229.32 ms)
```
