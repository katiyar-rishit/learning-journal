#include <stdio.h>

int main()
{
  int arr[5] = {10, 20, 30, 40, 50};
  
  //access
  printf("First element: %d\n", arr[0]);
  printf("Last element: %d\n", arr[4]);
  
  //modify
  arr[4] = 90;
  printf("New last element: %d\n", arr[4]);

  return 0;
}
