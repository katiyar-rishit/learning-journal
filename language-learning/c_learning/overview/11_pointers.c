//& tells us the memory address of the operand
//* tells us the value stored in variable
//* also helps in declaring a pointer
#include <stdio.h>

int main(){
  int a = 1;

  int * pointer_to_a = &a;
  
  printf("Value of a:%d\n", a);

  //memory address stored in pointer(address of variable a)
  printf("Address of a:%p\n", (void *)pointer_to_a);

  //memory address of pointer itself
  printf("Address of pointer:%p\n", (void *)&pointer_to_a);

  //value pointed by pointer(value of variable)
  printf("Value of a:%d\n", *pointer_to_a);


  return 0;
}
