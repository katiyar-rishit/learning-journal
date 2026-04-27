#include <iostream>

using namespace std;

class Demo
{
  static int count;

    public:Demo()
           {
              count++;
           }
    public: static void disp(){
        cout<<"The value of count="<<count;
            };
};

int Demo::count=0;
int main()
{
  Demo obj1;

  obj1.disp();
  return 0;
}
