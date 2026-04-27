#include <iostream>

using namespace std;

class SimpleInterest
{
  private:int principal,rate,time,interest;

  public:
        SimpleInterest()
        {
          interest = 2332;
        }
  public:
        void input();
        void calculate();

};

void SimpleInterest::input(){
    cout<<"Enter principal:";
    cin>>principal;
    cout<<"\nEnter rate:";
    cin>>rate;
    cout<<"\nEnter time:";
    cin>>time;
}

void SimpleInterest::calculate(){
    interest=(principal*rate*time)/100;
    cout<<interest;
}

int main(){
    SimpleInterest s1;
    s1.input();
    s1.calculate();

    SimpleInterest *p = new SimpleInterest;
    p->input();


    return 0;
}




