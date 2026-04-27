 #include <iostream>

using namespace std;

class SimpleInterest
{
  private: int principal,rate,time,SI;

  public: void input()
          {
            cout<<"Enter principal:";
            cin>>principal;

            cout<<"Enter rate:";
            cin>>rate;

            cout<<"Enter time";
            cin>>time;
          }

  public: void calculate()
          {
            SI = (principal*rate*time)/100;
          }

  public: void display()
          {
            cout<<"SI:"<<SI;
          }
};


int main()
{
  SimpleInterest obj;
  obj.input();
  obj.calculate();
  obj.display();

  return 0;
}








