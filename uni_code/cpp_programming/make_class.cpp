#include <iostream>

class Student
{
  private:
    int marks;

  public:
    int add_marks(); 
};

int Student::add_marks(){
    cin>>marks;
}


int main()
{
  Student s1;
  s1.add_marks();

  return 0;
}
