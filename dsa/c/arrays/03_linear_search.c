#include <stdio.h>

//check each element until we find key

int linearSearch(int arr[], int n, int key){
  for (int i; i < n; i++){
    if (arr[i] == key){
      return i;        //found required thing at index i
    }
  }
  return -1;
}


int main(){
  int arr[] = {5, 6, 7, 8, 9};
  int n = 5, key = 7;

  int index = linearSearch(arr, n, key);
  if (index != -1) printf("Element found at:%d\n", index);
  else printf("Element not found");

  return 0;
}
