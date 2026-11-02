#include <algorithm>
#include <iostream>

int main(){
  using namespace std;

  vector<int> v = {5, 65, 23, 56, 7, 23};
  cout << "unsorted vector:" << '\n';
  for(int i=0;i<v.size();i++){
    cout << v[i] << " ";
  }

  sort(v.begin(), v.end());
  cout << '\n' << "sorted vector:" << '\n';
  for(int j=0;j<v.size();j++){
    cout << v[j] << " ";
  }


  //binary search
  int key=56;
  bool found = binary_search(v.begin(),v.end(),key);
  if (found){
    cout << "Found"<<'\n';
  }else{
    cout<<"Not found"<<'\n';
  }

  //lower bound
  int ans=7;
  int idx = lower_bound(v.begin(), v.end(), ans) - v.begin();
  cout << "Lower bound: "<<idx<<'\n';


  return 0;
}
