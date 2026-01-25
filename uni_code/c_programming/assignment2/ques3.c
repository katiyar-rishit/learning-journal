#include <stdio.h>

int main(){
  float principal, rate, time, simple_interest;
  printf("Enter principal: ");
  scanf("%f", &principal);
  printf("Enter rate: ");
  scanf("%f", &rate);
  printf("Enter time: ");
  scanf("%f", &time);
  
  simple_interest = (principal*rate*time)/100;
  printf("simple interest: %f", simple_interest);
  
  return 0;
}
