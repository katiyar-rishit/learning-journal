#include <iostream>

using namespace std;

class Arithmetic
{
  private: int num1,num2,sum,sub,product,divide,mod1,mod2;

  public: void input()
  {
    cout<<"Enter first number:";
    cin>>num1;

    cout<<"\nEnter second number:";
    cin>>num2; 
  }

  public: void calculate()
  {
    sum = num1 + num2;
    sub = num1 - num2;
    product = num1 * num2;
    divide = num1 / num2;
    if(num1>=0)
    {
      mod1 = num1;
    }
    else if(num1<0)
    {
      mod1 = -num1;
    }

    if(num2>=0)
    {
      mod2 = num2;
    }
    else if(num2<0)
    {
      mod2 = -num2;
    }
  }

  public: void display()
  {
      cout<<num1<<'+'<<num2<<'='<<sum<<'\n';
      cout<<num1<<'-'<<num2<<'='<<sub<<'\n';
      cout<<num1<<'*'<<num2<<'='<<product<<'\n';
      cout<<num1<<'/'<<num2<<'='<<divide<<'\n';
      cout<<"mod of num1:"<<mod1<<'\n';
      cout<<"mod of num2:"<<mod2<<'\n';
  }
};



int main(){
  Arithmetic obj;
  obj.input();
  obj.calculate();
  obj.display();

  return 0;
}








