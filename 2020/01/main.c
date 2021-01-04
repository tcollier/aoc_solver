#include <stdio.h>
#include <stdlib.h>
#include "../../lib/lib.h"

#define BV_TYPE unsigned long int
#define BV_BITS 64 // sizeof(BV_TYPE) * 8
#define BV_MASK BV_BITS - 1
#define BV_SHIFTER 6  // log base 2 of BV_BITS
#define BV_BUCKETS 32 // (2020 >> SHIFTER) + 1

#define INPUT_LENGTH 200
#define TARGET_SUM 2020

typedef enum
{
  false,
  true
} bool;

typedef struct Pair
{
  int a, b;
} Pair;

typedef struct Triplet
{
  int a, b, c;
} Triplet;

void bit_vec_set(BV_TYPE *bv, int n)
{
  bv[n >> BV_SHIFTER] |= ((BV_TYPE)1 << (n & BV_MASK));
}

bool bit_vec_test(BV_TYPE *bv, int n)
{
  return (bv[n >> BV_SHIFTER] & (BV_TYPE)1 << (n & BV_MASK)) > 0;
}

void bit_vec_values(BV_TYPE *bv, int *values)
{
  int i = 0, j, num;
  for (j = 0; j < BV_BUCKETS; j++)
  {
    BV_TYPE bits = bv[j];
    num = BV_BITS * j;
    while (bits > 0)
    {
      if (bits & 1)
      {
        values[i] = num;
        i++;
      }
      bits >>= 1;
      num++;
    }
  }
}

void bit_vec_from_input(BV_TYPE *bv, char **input, int num_values)
{
  for (int i = 0; i < BV_BUCKETS; i++)
    bv[i] = 0;
  for (int i = 0; i < num_values; i++)
  {
    int n = 0;
    for (int c = 0; input[i][c] != '\n'; c++)
    {
      n *= 10;
      n += input[i][c] - '0';
    }
    bit_vec_set(bv, n);
  }
}

Pair pair_with_sum(BV_TYPE *bv, int sum)
{
  int *numbers = malloc(INPUT_LENGTH * sizeof(int));
  bit_vec_values(bv, numbers);

  Pair pair;
  int i;
  for (i = 0; i < INPUT_LENGTH - 1; i++)
  {
    int diff = sum - numbers[i];
    if (bit_vec_test(bv, diff))
    {
      pair.a = numbers[i];
      pair.b = diff;
      free(numbers);
      return pair;
    }
  }
  pair.a = pair.b = -1;
  free(numbers);
  return pair;
}

Triplet triplet_with_sum(BV_TYPE *bv, int sum)
{
  int *numbers = malloc(INPUT_LENGTH * sizeof(int));
  bit_vec_values(bv, numbers);

  Triplet triplet;
  for (int i = 0; i < INPUT_LENGTH - 2; i++)
  {
    int j = i + 1;
    int k = INPUT_LENGTH - 1;
    while (j < k)
    {
      int total = numbers[i] + numbers[j] + numbers[k];
      if (total == sum)
      {
        triplet.a = numbers[i];
        triplet.b = numbers[j];
        triplet.c = numbers[k];
        free(numbers);
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
  free(numbers);
  return triplet;
}

char *part1_result(char *data[])
{
  BV_TYPE *bv = malloc(BV_BUCKETS * sizeof(BV_TYPE));
  bit_vec_from_input(bv, data, INPUT_LENGTH);
  Pair pair = pair_with_sum(bv, TARGET_SUM);
  free(bv);
  int product = pair.a * pair.b;
  int num_digits = 1;
  for (; product > 9; num_digits++)
    product /= 10;

  char *result = malloc(sizeof(char) * (num_digits + 1));
  sprintf(result, "%d", pair.a * pair.b);
  return result;
}

char *part2_result(char *data[])
{
  BV_TYPE *bv = malloc(BV_BUCKETS * sizeof(BV_TYPE));
  bit_vec_from_input(bv, data, INPUT_LENGTH);
  Triplet triplet = triplet_with_sum(bv, TARGET_SUM);
  free(bv);
  int product = triplet.a * triplet.b * triplet.c;
  int num_digits = 1;
  for (; product > 9; num_digits++)
    product /= 10;

  char *result = malloc(sizeof(char) * (num_digits + 1));
  sprintf(result, "%d", triplet.a * triplet.b * triplet.c);
  return result;
}

int main(int argc, char *argv[])
{
  char *data[INPUT_LENGTH];
  load_input("2020/01/input.txt", data);
  executor(data, part1_result, part2_result, argc, argv);
  for (int i = 0; i < INPUT_LENGTH; i++)
  {
    free(data[i]);
  }
}
