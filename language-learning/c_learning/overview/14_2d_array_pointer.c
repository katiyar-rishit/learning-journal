#include <stdio.h>
#include <stdlib.h>

void modify_array(int *ptr, int r, int c){
  for (int i = 0;i < r*c;i++){
    ptr[i] = i + 1;
  }
}

void print_array(int *ptr, int r, int c){
  for (int i = 0;i < r;i++){
    for (int j = 0;j < c;j++){
      printf("\t%d", ptr[i*c+j]);
    }
    printf("\n");
  }
}


int main(){
  int r = 3, c = 4;
  int *ptr = malloc(r*c* sizeof(int));

  modify_array(ptr, r, c);

  print_array(ptr, r, c);
  
  free(ptr);

  return 0;
}
