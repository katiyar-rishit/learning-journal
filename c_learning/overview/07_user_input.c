#include <stdio.h>
#include <stdlib.h>

int main()
{
  int age;
  printf("How old are you?");
  scanf("%d", &age);
  printf("You are %d years old\n", age);

  double gpa;
  printf("How are you doing in college?");
  scanf("%lf", &gpa);
  printf("%f gpa?good\n", gpa);
  
  char grade;
  printf("Enter your grade:");
  scanf(" %c", &grade); //the space before %c tells scanf to ignore \n \t
  printf("Your grade is %c\n", grade);
  
  char name[20];
  printf("Enter your name:");
  scanf("%s", name);
  printf("Hello %s\n", name);
  
  //clear buffer before fgets
  getchar();

  char NAME[20];
  printf("Enter your name:");
  fgets(NAME, 20, stdin);
  printf("Hello %s I am c", NAME);

  return 0;

}






