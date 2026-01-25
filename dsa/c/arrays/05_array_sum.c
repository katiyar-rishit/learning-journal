#include <stdio.h>

int main(){
  int arr[] = {1, 2, 3, 4, 5};
  int sum = 0;
  
  //finding length because idk
  int length = sizeof(arr) / sizeof(arr[0]);
  
  //computing sum
  for (int i=0; i<length; i++){
    sum += arr[i];
  }
  printf("Sum of elements: %d", sum);

  return 0;
}
