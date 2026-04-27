#include <iostream>
#include <algorithm>

int main(){
  using namespace std;

  int arr[5] = {2, 4, -6 , -7, 2};
  int n=sizeof(arr)/sizeof(int);
  int best=arr[0];
  for (int a=0;a<n;a++){
    for (int b=a;b<n;b++){
      int sum=0;
      for (int k=a;k<=b;k++){
        sum += arr[k];
      }
      best= max(best,sum);
    }
  }
  cout<<best<<"\n";
  
  return 0;
}
