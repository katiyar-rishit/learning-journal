#include <stdio.h>

int main(){
  char rangoli[4][4];
  for (int i = 0;i<4;i++){
    for (int j = 0;j<4;j++){
      rangoli[i][j] = '*';
      printf("%c", rangoli[i][j]);
    }
    printf("\n");
    

  }

  return 0;
}
