#include <stdio.h>

int main(){
  int a, b;
  printf("Enter numbers: ");
  scanf("%d %d", &a , &b);
  if (a > b){
    printf("a is larger number.");
  } else if(b > a){
    printf("b is larger number.");
  }else{
    printf("a and b are equal");
  }

  return 0;
}
