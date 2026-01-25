#include <stdio.h>

#define pi 3.14

int main(){
  //declaring required variables
  int radius;
  float area;
  //taking user input
  printf("Enter radius of circle: \n");
  scanf("%d", &radius);
  //calculating area
  area = pi * (radius * radius);
  //printing area
  printf("Area of circle of radius %d: %f\n", radius, area);

  return 0;

}
