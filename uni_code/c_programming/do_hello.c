#include <stdio.h>

int main(){
  int i = 1;
  do{
    if (i<=5){
      printf("Hello\n");
    }else{
      printf("Bye\n");
    }
    i++;
  }while(i<=10);

  return 0;
}
