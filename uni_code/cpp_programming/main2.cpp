#include <iostream>
using namespace std;

void xyz(int *arr[5]){
  cout<< sizeof(&arr);
}


int main(){
  int arr[5] = {1, 2, 3, 4, 5};

  xyz(&arr);

  return 0;

}
