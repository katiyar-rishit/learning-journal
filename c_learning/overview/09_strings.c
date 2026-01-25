#include <stdio.h>
#include <string.h>

int main()
{
  //read only string-no modifications
  char * name = "John";

  //can be manipulated
  char identity[] = "Andrew Potts";

  //printing the string
  printf("Hello %s\n", name);
  
  //comparing string - returns o if same
  if (strncmp(name, "John", 4) == 0) {
    printf("Hello %s\n", name);
  } else {
    printf("You aren't John\n");
  }

  //concatenating 
  char dest[20] = "Hello";
  char src[20] = "World";
  strncat(dest, src, 3);
  printf("%s\n", dest);
  strncat(dest, src, 20);
  printf("%s\n", dest);

  return 0;
}
