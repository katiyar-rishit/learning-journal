#include <iostream>
#include <string>

using namespace std;

class Employee
{
  private: int salary,ta,da,hra,total,net;
           string Ename,Emp_id;
                       
  public: void input()
          {
            cout<<"Enter employee id:";
            cin>>Emp_id;
            cout<<"\nEnter name:";
            cin>>Ename;
            cout<<"\nEnter salary:";
            cin>>salary;
          }
  
  public: void calculate()
          {
            ta = salary * 0.05;
            da = salary * 0.07;
            hra = salary * 0.09;
            total = ta+da+hra;
            net=total*0.35;
          }

  public: void display()
          {
            cout<<"Employee id:"<<Emp_id<<'\n';
            cout<<"Employee name:"<<Ename<<'\n';
            cout<<"Salary:"<<salary<<'\n';
            cout<<"----------------------"<<'\n';
            cout<<"TA:"<<ta<<'\n';
            cout<<"DA:"<<da<<'\n';
            cout<<"HRA:"<<hra<<'\n';
            cout<<"Total:"<<total<<'\n';
            cout<<"Net:"<<net<<'\n';
          }
};


int main(){
  Employee emp1;
  emp1.input();
  emp1.calculate();
  emp1.display();


  return 0;

}





