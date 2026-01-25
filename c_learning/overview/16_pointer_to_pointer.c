#include <stdio.h>

int main(){
  int i = 3;
  int *j = &i;
  int **k = &j;

  printf("Value: %d\n", **k);
  printf("Address: %p\n", k);

  return 0;
}
