#include <stdio.h>
#include <stdlib.h>

#define BV_TYPE unsigned long int
#define BV_BITS 64 // sizeof(BV_TYPE) * 8
#define BV_MASK BV_BITS - 1
#define BV_SHIFTER 6  // log base 2 of BV_BITS
#define BV_BUCKETS 32 // (2020 >> SHIFTER) + 1

#define TARGET_SUM 2020

typedef enum
{
  false,
  true
} bool;

struct Pair
{
  int a, b;
};

struct Triplet
{
  int a, b, c;
};

void bit_vec_set(BV_TYPE *bv, int n)
{
  bv[n >> BV_SHIFTER] |= ((BV_TYPE)1 << (n & BV_MASK));
}

bool bit_vec_test(BV_TYPE *bv, int n)
{
  return (bv[n >> BV_SHIFTER] & (BV_TYPE)1 << (n & BV_MASK)) > 0;
}

void bit_vec_values(BV_TYPE *bv, int bv_len, int *values)
{
  int i, j, num;
  i = 0;
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

struct Pair pair_with_sum(int *numbers, int numbers_len, BV_TYPE *bv, int sum)
{
  struct Pair pair;
  int i;
  for (i = 0; i < numbers_len - 1; i++)
  {
    int diff = sum - numbers[i];
    if (bit_vec_test(bv, diff))
    {
      pair.a = numbers[i];
      pair.b = diff;
      return pair;
    }
  }
  pair.a = pair.b = -1;
  return pair;
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
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  ssize_t read;
  int numbers_len = 0;
  fp = fopen("2020/01/input.txt", "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);

  BV_TYPE *bv = malloc(BV_BUCKETS * sizeof(BV_TYPE));
  while ((read = getline(&line, &len, fp)) != -1)
  {
    int num = 0;
    for (int i = 0; i < read - 1; i++)
    {
      num *= 10;
      num += line[i] - '0';
    }
    numbers_len++;
    bit_vec_set(bv, num);
  }

  fclose(fp);
  if (line)
    free(line);

  int *numbers = malloc(numbers_len * sizeof(int));
  bit_vec_values(bv, 64, numbers);

  struct Pair pair = pair_with_sum(numbers, numbers_len, bv, TARGET_SUM);
  printf("%d\n", pair.a * pair.b);

  struct Triplet triplet = triplet_with_sum(numbers, numbers_len, TARGET_SUM);
  printf("%d\n", triplet.a * triplet.b * triplet.c);

  free(numbers);
  free(bv);
  exit(EXIT_SUCCESS);
}
