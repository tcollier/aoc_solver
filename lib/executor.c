#include <stdio.h>
#include <string.h>
#include <sys/time.h>

typedef enum
{
  false,
  true
} bool;

typedef struct TimingInfo
{
  unsigned long iterations;
  double duration;
} TimingInfo;

double time_diff_us(struct timeval x, struct timeval y)
{
  double x_ms, y_ms, diff;

  x_ms = (double)x.tv_sec * 1000000 + (double)x.tv_usec;
  y_ms = (double)y.tv_sec * 1000000 + (double)y.tv_usec;

  diff = (double)y_ms - (double)x_ms;

  return diff;
}

bool continue_iterating(unsigned long iterations, struct timeval before)
{
  struct timeval now;
  gettimeofday(&now, NULL);
  double duration_us = time_diff_us(before, now);

  if (iterations < 100)
  {
    return duration_us < 30000000;
  }
  else
  {
    return duration_us < 100000;
  }
}

TimingInfo time_fn(char *data[], char *(*solver_fn)(char **))
{
  char *result;
  struct timeval before, after;
  TimingInfo ti;
  int i = 0;

  gettimeofday(&before, NULL);

  for (; continue_iterating(i, before); i++)
  {
    (*solver_fn)(data);
  }
  gettimeofday(&after, NULL);
  ti.duration = time_diff_us(before, after);
  ti.iterations = i;
  return ti;
}

void executor(char *data[], char *(*part1_fn)(char **), char *(*part2_fn)(char **), int argc, char *argv[])
{
  if (argc >= 1 && strcmp(argv[argc - 1], "--time") == 0)
  {
    TimingInfo part1_ti = time_fn(data, part1_fn);
    TimingInfo part2_ti = time_fn(data, part2_fn);
    printf(
        "{\"part1\":{\"duration\":%f,\"iterations\":%lu},\"part2\":{\"duration\":%f,\"iterations\":%lu}}\n",
        part1_ti.duration,
        part1_ti.iterations,
        part2_ti.duration,
        part2_ti.iterations);
  }
  else
  {
    printf("%s\n", (*part1_fn)(data));
    printf("%s\n", (*part2_fn)(data));
  }
}
