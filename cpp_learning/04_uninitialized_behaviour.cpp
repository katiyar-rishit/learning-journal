#include <iostream>

int main()
{
  int x; //uninitialized variable
  
  std::cout << x << '\n'; //who knows what we'll get
  
  return 0;
}
