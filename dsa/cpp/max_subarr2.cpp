#include <iostream>
#include <algorithm>

int main(){
  using namespace std;

  int arr[]={3, 5, 7, -10, 82, -56, 45};
  int best=arr[0];
  int n=sizeof(arr)/sizeof(int);
  for (int a=0;a<n;a++){
    int sum=0;
    for (int b=a;b<n;b++){
      sum+=arr[b];
      best=max(best,sum);
    }
  }
  cout<<best<<"\n";

  return 0;
}
