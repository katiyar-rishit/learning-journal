#include <stdio.h>

void draw(int x, int y){
  printf("%d, %d", x, y);
}

//one way of defining structures
struct point {
  int x;
  int y;
};

//another way
typedef struct{
  int Maths_mark;
  int Physics_mark;
  char * name;

} Student;


int main(){
  //using structs from first method
  struct point p;
  p.x = 10;
  p.y = 5;
  draw(p.x, p.y);

  //second method
  Student s1;
  s1.name = "Rishit";
  s1.Maths_mark = 73;
  s1.Physics_mark = 84;

  return 0;
}
