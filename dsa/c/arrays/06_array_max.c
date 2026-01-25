#include <stdio.h>

int main(){
  int arr[5] = {10, 20, 30, 40, 50};
  int max = arr[0];

  for (int i = 0; i < 5; i++){
    if (arr[i] > max){
      max = arr[i];
    }
  }
  printf("Maximum element:%d", max);

  return 0;
}
