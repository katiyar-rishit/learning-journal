#include <iostream>

using namespace std;

class Number{
  private:int num;

  public:void input()
        {
          cout<<"Enter number:";
          cin>>num;
        }

  public:void sign()
         {
            if(num>0)
            {
              cout<<"+"<<'\n';
            }
            else if(num==0)
            {
              cout<<"0"<<'\n';
            }
            else
            {
              cout<<"-"<<'\n';
            }
          }
  
    public:

};
