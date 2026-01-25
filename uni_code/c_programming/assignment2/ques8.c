#include <stdio.h>

int main(){
  float subject1, subject2, subject3, total, average;
  printf("Enter subject1 marks: ");
  scanf("%f", &subject1);
  printf("Enter subject2 marks: ");
  scanf("%f", &subject2);
  printf("Enter subject3 marks: ");
  scanf("%f", &subject3);

  total = subject1 + subject2 + subject3;
  average = total / 3;

  printf("Total: %f\n", total);
  printf("Average: %f\n", average);

  return 0;
}
