#include <stdio.h>

int main() {
  char a;
  int no_of_page;
  float cost;
  printf("Enter name of book: ");
  scanf("%c", &a);
  printf("Enter no of pages:");
  scanf("%d", &no_of_page);
  printf("Enter cost:");
  scanf("%f", &cost);

  printf("Book name: %c\n",a);
  printf("No. of pages: %d\n", no_of_page);
  printf("Cost of book: %f\n", cost);

  return 0;
}
