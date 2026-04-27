//O(n) complexity

#include <iostream>
#include <algorithm>

int main(){
  using namespace std;

  int arr[]= {-1, 2, 4, -3, 5, 2, -5, 2};
  int n=sizeof(arr)/sizeof(int);
  int best=0, sum=0;
  for(int a=0;a<n;a++){
    sum=max(arr[a],sum+arr[a]);
    best=max(best,sum);
  }

  cout<<best<<"\n";

  return 0;
}
