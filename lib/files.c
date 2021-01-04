#include <stdio.h>
#include <stdlib.h>

void load_input(char *filename, char *lines[])
{
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  ssize_t read;
  int num_lines = 0;

  fp = fopen(filename, "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);

  while ((read = getline(&line, &len, fp)) != -1)
  {
    lines[num_lines] = malloc(len * sizeof(char));
    sprintf(lines[num_lines], "%s", line);
    num_lines++;
  }

  fclose(fp);
  if (line)
    free(line);
}
