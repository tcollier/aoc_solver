## 2020

That was one hell of a year! Thankfully we had Advent of Code to get us through the home stretch.
Despite a late start (I didn't get to days 1 - 12 until the 12th), I started the latter half of the challenges on time (midnight EST) and worked with some friends over a Google Meet.

## Solution Performance

Since performance varied wildly from day to day (day 0 solutions were all in the nanoseconds range, whereas day 22's python solution took 17 seconds!), pay close attention to the unit of measure for each metric in the list below.

```
PASS [2020/01 c         ] (part1:   2.85 μs, part2:   3.25 μs, overhead:  11.26 ms)
PASS [2020/01 golang    ] (part1:  11.03 μs, part2:   4.83 μs, overhead:  14.43 ms)
PASS [2020/01 java      ] (part1:   4.87 μs, part2:   8.53 μs, overhead: 104.80 ms)
PASS [2020/01 lisp      ] (part1: 372.92 μs, part2: 154.45 μs, overhead:  33.09 ms)
PASS [2020/01 python    ] (part1:   5.58 μs, part2:  42.27 μs, overhead: 154.89 ms)
PASS [2020/01 ruby      ] (part1:  25.92 μs, part2:  18.92 μs, overhead:  92.59 ms)
PASS [2020/01 rust      ] (part1:   8.66 μs, part2:   3.65 μs, overhead:   8.53 ms)
PASS [2020/01 scala     ] (part1:   1.13 μs, part2:   1.13 μs, overhead: 446.86 ms)
PASS [2020/01 typescript] (part1:   5.34 μs, part2:  26.32 μs, overhead:  79.74 ms)
PASS [2020/02 java      ] (part1: 694.44 μs, part2: 353.36 μs, overhead: 110.83 ms)
PASS [2020/02 python    ] (part1:   2.35 ms, part2:   1.82 ms, overhead:  40.46 ms)
PASS [2020/02 ruby      ] (part1:   3.09 ms, part2:   1.70 ms, overhead:  93.74 ms)
PASS [2020/02 typescript] (part1: 318.47 μs, part2: 184.50 μs, overhead:  54.36 ms)
PASS [2020/03 python    ] (part1: 589.27 μs, part2: 796.13 μs, overhead:  41.62 ms)
PASS [2020/04 python    ] (part1:   1.00 ms, part2:   3.09 ms, overhead:  46.37 ms)
PASS [2020/05 python    ] (part1: 868.98 μs, part2: 881.92 μs, overhead:  38.16 ms)
PASS [2020/06 python    ] (part1:   1.32 ms, part2:   1.45 ms, overhead:  50.15 ms)
PASS [2020/07 python    ] (part1:   3.96 ms, part2:   3.32 ms, overhead:  42.40 ms)
PASS [2020/08 python    ] (part1: 103.33 μs, part2:  13.28 ms, overhead:  54.62 ms)
PASS [2020/09 python    ] (part1: 501.31 μs, part2:   9.30 ms, overhead:  49.09 ms)
PASS [2020/10 python    ] (part1:  18.28 μs, part2:  85.85 μs, overhead:  64.68 ms)
PASS [2020/11 python    ] (part1:   2.64 s,  part2:   2.17 s,  overhead:  44.37 ms)
PASS [2020/12 python    ] (part1: 507.47 μs, part2: 523.11 μs, overhead:  51.88 ms)
PASS [2020/13 python    ] (part1:   7.65 μs, part2: 110.58 μs, overhead:  54.86 ms)
PASS [2020/14 python    ] (part1:   1.95 ms, part2:  55.07 ms, overhead:  47.30 ms)
PASS [2020/15 java      ] (part1:   8.80 μs, part2: 386.50 ms, overhead: 452.85 ms)
PASS [2020/15 python    ] (part1: 284.28 μs, part2:   7.14 s,  overhead:  48.64 ms)
PASS [2020/15 ruby      ] (part1: 228.54 μs, part2:   4.35 s,  overhead: 120.29 ms)
PASS [2020/15 typescript] (part1:  55.49 μs, part2:   4.57 s,  overhead: 157.30 ms)
PASS [2020/16 python    ] (part1:   3.00 ms, part2:  14.58 ms, overhead:  45.31 ms)
PASS [2020/17 python    ] (part1: 150.45 ms, part2:   4.21 s,  overhead:  42.07 ms)
PASS [2020/18 python    ] (part1:  15.64 ms, part2:  17.56 ms, overhead:  45.53 ms)
PASS [2020/18 ruby      ] (part1:   2.72 ms, part2:   2.87 ms, overhead:  93.53 ms)
PASS [2020/19 python    ] (part1:   3.82 ms, part2:  16.90 ms, overhead:  53.40 ms)
PASS [2020/20 python    ] (part1:   4.92 ms, part2: 107.31 ms, overhead:  49.32 ms)
PASS [2020/21 python    ] (part1: 734.72 μs, part2: 662.97 μs, overhead:  39.81 ms)
PASS [2020/22 python    ] (part1:  89.73 μs, part2:  16.64 s,  overhead:  37.21 ms)
PASS [2020/23 java      ] (part1: 931.76 ns, part2: 216.57 ms, overhead: 114.77 ms)
PASS [2020/23 python    ] (part1:  73.92 μs, part2:  10.52 s,  overhead:  50.19 ms)
PASS [2020/24 python    ] (part1:  24.84 ms, part2: 822.38 ms, overhead:  40.98 ms)
PASS [2020/25 python    ] (part1: 314.90 ms, part2: 535.39 ns, overhead: 227.81 ms)
```
