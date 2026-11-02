#include <stdio.h>
#include <stdlib.h>

typedef struct{
  int age;
  char * name;
  char * gender;
}person;


int main(){
  person * myperson = (person *) malloc(sizeof(person));
  
  myperson->name = "Rishit";
  myperson->age = 18;
  myperson->gender = "Male";
  
  printf("Hello %s\n", myperson->name);
  printf("The system identifies you as an %d year old %s.\n",myperson->age, myperson->gender);
  
  free(myperson);

  return 0;
}
