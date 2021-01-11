#include "../../ext/c/lib.h"

char *part1_result(char *data[])
{
  return data[0];
}

char *part2_result(char *data[])
{
  return data[1];
}

int main(int argc, char *argv[])
{
  char *data[2];
  data[0] = "Hello";
  data[1] = "World!";

  executor(data, part1_result, part2_result, argc, argv);
}
