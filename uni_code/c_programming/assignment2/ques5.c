#include <stdio.h>

int main(){
  float side, volume;

  //taking user input
  printf("Enter side: ");
  scanf("%f", &side);

  //calculating volume
  volume = side * side * side;

  //printing output
  printf("Volume of cube: %f", volume);

  return 0;
}
