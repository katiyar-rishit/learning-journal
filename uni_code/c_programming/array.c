#include <stdio.h>

int main(){
  int arr[5];
  for (int i=0;i<5;i++){
    printf("\nEnter element: ");
    scanf("%d", &arr[i]);
  }
  for (int i=0;i<5;i++){
    printf("%d ", arr[i]);
  }
  printf("\n");

  //sum of elements
  int sum = 0;
  for (int i=0;i<5;i++){
    sum += arr[i];
  }

  //maximum element
  int max = arr[0];
  for (int i=0;i<5;i++){
    if (arr[i] > max){
      max = arr[i];
    }
  }

  //occurence of value
  int count = 0;
  int key;
  printf("Enter key: ");
  scanf("%d", &key);
  for (int i=0;i<5;i++){
    if (arr[i] == key){
      count++;
    }
  }
  printf("No. of occurences: %d", count);

  return 0;
}




