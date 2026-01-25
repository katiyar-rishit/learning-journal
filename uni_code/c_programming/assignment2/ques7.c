#include <stdio.h>

int main(){
  float length, breadth, perimeter;
  printf("Enter length: ");
  scanf("%f", &length);
  printf("Enter breadth: ");
  scanf("%f", &breadth);

  perimeter = 2 * (length + breadth);

  printf("Perimeter: %f", perimeter);

  return 0;
}
