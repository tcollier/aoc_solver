#include <stdio.h>
#include <stdlib.h>

struct Pair
{
  int a, b;
};

struct Triplet
{
  int a, b, c;
};

struct Pair pair_with_sum(int *numbers, int numbers_len, int sum)
{
  struct Pair pair;
  int i;
  int bv[32];

  for (i = 1; i < numbers_len; i++)
  {
    bv[numbers[i] >> 6] |= 1 << (numbers[i] & 63);
  }
  for (i = 0; i < numbers_len - 1; i++)
  {
    int remainder = sum - numbers[i];
    if (bv[remainder >> 6] >> (remainder & 63) & 1)
    {
      pair.a = numbers[i];
      pair.b = remainder;
      return pair;
    }
  }
  pair.a = pair.b = -1;
  return pair;
}

int compare(const void *a, const void *b)
{
  int int_a = *((int *)a);
  int int_b = *((int *)b);

  if (int_a == int_b)
    return 0;
  else if (int_a < int_b)
    return -1;
  else
    return 1;
}

struct Triplet triplet_with_sum(int *numbers, int numbers_len, int sum)
{
  struct Triplet triplet;
  for (int i = 0; i < numbers_len - 2; i++)
  {
    int j = i + 1;
    int k = numbers_len - 1;
    while (j < k)
    {
      int total = numbers[i] + numbers[j] + numbers[k];
      if (total == sum)
      {
        triplet.a = numbers[i];
        triplet.b = numbers[j];
        triplet.c = numbers[k];
        return triplet;
      }
      else if (total < sum)
      {
        j++;
      }
      else
      {
        k--;
      }
    }
  }
  triplet.a = triplet.b = triplet.c = -1;
  return triplet;
}

int main()
{
  int numbers[200];
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  ssize_t read;
  fp = fopen("2020/01/input.txt", "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);

  int index = 0;
  while ((read = getline(&line, &len, fp)) != -1)
  {
    numbers[index] = 0;
    for (int i = 0; i < read - 1; i++)
    {
      numbers[index] *= 10;
      numbers[index] += line[i] - '0';
    }
    index++;
  }

  fclose(fp);
  if (line)
    free(line);

  qsort(numbers, 200, sizeof(int), compare);

  struct Pair pair = pair_with_sum(numbers, 200, 2020);
  printf("%d\n", pair.a * pair.b);

  struct Triplet triplet = triplet_with_sum(numbers, 200, 2020);
  printf("%d\n", triplet.a * triplet.b * triplet.c);

  exit(EXIT_SUCCESS);
}
