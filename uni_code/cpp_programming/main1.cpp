#include <iostream>

using namespace std;

class Account{
  public:int accountNumber=22323;

  protected: int balance=2324343;
};

class SavingAccount:protected Account{
  public:
    void display(){
      cout<<"Account no.:"<<accountNumber<<endl;
      cout<<"Balance:"<<balance<<endl;
    }

    void withdraw(int amount){
      if (amount>balance){
        cout<<"Insufficient balance.";
      }
      else if(amount <= balance){
        balance = balance - amount;
        cout<<"Amount withdrawn:"<<amount<<endl;
      }
    }

    void showBalance(){
      cout<<"Balance:"<<balance<<endl;
    }


};


int main(){
  SavingAccount s1432;
  s1432.display();
  s1432.withdraw(2344);
  s1432.showBalance();

  return 0;
}





