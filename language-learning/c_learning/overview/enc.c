#include <stdio.h>

int main(){
  int x = 5;
  int *p = &x;

  char * name = "Rishit";
  char ** c = &name;
  
  printf("Name:%s\n", name);
  printf("x:%d\n", x);

  return 0;

}
