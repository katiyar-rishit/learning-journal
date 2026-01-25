#include <stdio.h>

int main(){
  int a, b, c;

  //taking user input
  printf("Enter a: ");
  scanf("%d", &a);
  printf("Enter b: ");
  scanf("%d", &b);
  
  //main logic
  c = a;
  a = b;
  b = c;
  
  //printing swapped values
  printf("a: %d\n", a);
  printf("b: %d\n", b);

  return 0;
}
