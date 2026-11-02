#include <iostream>
using namespace std;

void xyz(int (*arr)[3]){
  cout<<sizeof(arr);
}

int main(){
  int arr[][3]={1,2,3,4,5,6,7};
  
  xyz(arr);
  return 0;
}
