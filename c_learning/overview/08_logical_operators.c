#include <stdio.h>

int main()
{
  //and & or operator
  int value1 = 13;
  int value2 = 15;
  int value3 = 17;
  if (value1 < value2 && value2 < value3)
  {
    printf("value2 is greater than value1 and smaller than value3\n");
  }else if(value1 < value2 || value3 < value2)
  {
    printf("value2 is greater than value1 or value3 is smaller than value2\n");
  }
 
  //not operator
  int target = 10;
  if (target != 11)
  {
    printf("Target is not equal to 11.\n");
  }

  return 0;
}
