#include <stdio.h>

int main(){
  int a, b, c;
  printf("Enter three numbers: ");
  scanf("%d %d %d",&a, &b, &c);
  if (a > b){
    if (a > c){
      printf("a is largest number.");
    }else{
      printf("c is largest number.");
    }
  }else{
    if (b > c){
      printf("b is largest number.");
    }else{
      printf("c is largest number.");
    }
  }

  return 0;
}
