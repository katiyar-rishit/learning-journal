#include <iostream>

using namespace std;

class Student
{
private:
    int marks;

public:
    void add_marks();
    void display_marks();
};

void Student::add_marks(){
    cout<<"Enter your marks:";
    cin >> marks;
    cout<<"Marks entered successfully.\n";
}

void Student::display_marks(){
    cout<<marks;
}

int main()
{
    Student s1;
    s1.add_marks();
    s1.display_marks();

    return 0;
}
