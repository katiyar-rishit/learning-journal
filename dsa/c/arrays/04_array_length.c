#include <stdio.h>

int main(){
  int arr[] = {10, 20, 30, 40, 50};
  
  int length = sizeof(arr) / sizeof(arr[0]);
  printf("Array length: %d", length);

  return 0;
}
