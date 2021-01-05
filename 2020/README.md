## 2020

That was one hell of a year! Thankfully we had Advent of Code to get us through the home stretch.
Despite a late start (I didn't get to days 1 - 12 until the 12th), I started the latter half of the challenges on time (midnight EST) and worked with some friends over a Google Meet.

## Solution Performance

Since performance varied wildly from day to day (day 0 solutions were all in the nanoseconds range, whereas day 22's python solution took 17 seconds!), pay close attention to the unit of measure for each metric in the list below.

```
PASS [2020/00 c         ] (part1:  36.59 ns, part2:  35.93 ns, overhead:   4.88 ms)
PASS [2020/00 golang    ]
PASS [2020/00 java      ] (part1:  27.08 ns, part2:  24.04 ns, overhead: 102.00 ms)
PASS [2020/00 lisp      ]
PASS [2020/00 python    ] (part1: 866.51 ns, part2: 882.32 ns, overhead:  40.53 ms)
PASS [2020/00 ruby      ] (part1: 387.81 ns, part2: 419.12 ns, overhead: 155.34 ms)
PASS [2020/00 rust      ] (part1: 185.37 ns, part2: 180.84 ns, overhead:   6.73 ms)
PASS [2020/00 scala     ] (part1:  26.95 ns, part2:  24.31 ns, overhead: 407.51 ms)
PASS [2020/00 typescript] (part1:  57.37 ns, part2:  60.41 ns, overhead:  44.12 ms)
PASS [2020/01 c         ] (part1:   4.95 μs, part2:   5.08 μs, overhead:   8.19 ms)
PASS [2020/01 golang    ]
PASS [2020/01 java      ] (part1:   5.85 μs, part2: 639.63 ns, overhead:  93.62 ms)
PASS [2020/01 lisp      ]
PASS [2020/01 python    ] (part1: 241.92 μs, part2: 300.48 μs, overhead:  32.34 ms)
PASS [2020/01 ruby      ] (part1:  26.62 μs, part2:  10.74 μs, overhead: 154.41 ms)
PASS [2020/01 rust      ] (part1: 214.91 μs, part2:  81.73 μs, overhead:  15.81 ms)
PASS [2020/01 scala     ] (part1:  34.57 μs, part2:  98.72 μs, overhead: 412.37 ms)
PASS [2020/01 typescript] (part1:   6.59 μs, part2:   4.08 μs, overhead:  46.85 ms)
PASS [2020/02 java      ] (part1:  50.18 μs, part2:   8.06 μs, overhead: 110.55 ms)
PASS [2020/02 python    ] (part1:   2.33 ms, part2:   1.78 ms, overhead:  37.13 ms)
PASS [2020/02 ruby      ] (part1:   3.06 ms, part2:   1.74 ms, overhead: 159.01 ms)
PASS [2020/02 typescript] (part1: 344.83 μs, part2: 184.05 μs, overhead:  49.44 ms)
PASS [2020/03 python    ] (part1: 594.03 μs, part2: 772.16 μs, overhead:  37.54 ms)
PASS [2020/04 python    ] (part1: 997.03 μs, part2:   3.12 ms, overhead:  33.09 ms)
PASS [2020/05 python    ] (part1: 892.00 μs, part2: 886.06 μs, overhead:  38.09 ms)
PASS [2020/06 python    ] (part1:   1.42 ms, part2:   1.45 ms, overhead:  38.17 ms)
PASS [2020/07 python    ] (part1:   3.82 ms, part2:   3.79 ms, overhead:  40.42 ms)
PASS [2020/08 python    ] (part1: 101.85 μs, part2:  65.18 μs, overhead:  41.75 ms)
PASS [2020/09 python    ] (part1: 511.76 μs, part2:   9.69 ms, overhead:  39.08 ms)
PASS [2020/10 python    ] (part1:  18.58 μs, part2:  96.08 μs, overhead:  38.07 ms)
PASS [2020/11 python    ] (part1:   2.73 s,  part2:   2.32 s,  overhead:  41.14 ms)
PASS [2020/12 python    ] (part1: 524.05 μs, part2: 532.79 μs, overhead:  37.91 ms)
PASS [2020/13 python    ] (part1:   8.11 μs, part2: 117.97 μs, overhead:  39.87 ms)
PASS [2020/14 python    ] (part1:   2.02 ms, part2:  58.66 ms, overhead:  30.79 ms)
PASS [2020/15 java      ] (part1:   8.48 μs, part2: 442.72 ms, overhead: 453.00 ms)
PASS [2020/15 python    ] (part1: 297.75 μs, part2:   7.84 s,  overhead:  38.21 ms)
PASS [2020/15 ruby      ] (part1: 234.19 μs, part2:   4.56 s,  overhead: 191.16 ms)
PASS [2020/15 typescript] (part1:  58.93 μs, part2:   4.86 s,  overhead:  86.39 ms)
PASS [2020/16 python    ] (part1:   3.12 ms, part2:  15.04 ms, overhead:  40.33 ms)
PASS [2020/17 python    ] (part1: 153.55 ms, part2:   4.35 s,  overhead:  37.66 ms)
PASS [2020/18 python    ] (part1:  17.02 ms, part2:  19.32 ms, overhead:  35.35 ms)
PASS [2020/18 ruby      ] (part1:   3.09 ms, part2:   3.16 ms, overhead: 169.13 ms)
PASS [2020/19 python    ] (part1:   3.76 ms, part2:  17.07 ms, overhead:  38.69 ms)
PASS [2020/20 python    ] (part1:   5.17 ms, part2: 112.77 ms, overhead:  35.72 ms)
PASS [2020/21 python    ] (part1: 756.01 μs, part2: 690.35 μs, overhead:  40.24 ms)
PASS [2020/22 python    ] (part1:  93.28 μs, part2:  17.69 s,  overhead:  42.39 ms)
PASS [2020/23 java      ] (part1:   1.02 μs, part2: 679.67 ms, overhead: 100.05 ms)
PASS [2020/23 python    ] (part1:  81.98 μs, part2:  10.49 s,  overhead:  41.11 ms)
PASS [2020/24 python    ] (part1:  28.37 ms, part2: 856.55 ms, overhead:  39.21 ms)
PASS [2020/25 python    ] (part1: 295.43 ms, part2: 933.41 ns, overhead:  39.07 ms)
```
