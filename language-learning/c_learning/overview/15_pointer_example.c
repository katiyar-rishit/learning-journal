#include <stdio.h>

int main(){
  int i = 25;
  int *ptr = &i;

  printf("Value: %d\n", *ptr);
  printf("Address: %p\n", ptr);
  printf("Address of ptr: %p\n", &ptr);

  return 0;
}
