#include <stdio.h>
#include <stdlib.h>

int main()
{
  char characterName[] = "John";
  int characterAge = 35;
  printf("There once was a man %s\n", characterName);
  printf("He was %d years old\n", characterAge);

  characterAge = 67;
  printf("He liked the name %s\n", characterName);
  printf("but he did not like being %d\n", characterAge);

  return 0;

}
