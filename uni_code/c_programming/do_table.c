#include <stdio.h>

int main(){
  int i = 1;
  do{
    int a = 2*i;
    printf("2X%d:%d\n",i, a);
    i++;
  }while(i<=10);

  return 0;
}
