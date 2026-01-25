#include <stdio.h>

int main(){
  char character;

  //taking user input
  printf("Enter character: ");
  scanf("%c", &character);

  //print ascii value
  printf("The ASCII value of %c is %d\n", character, character);

  return 0;
}
