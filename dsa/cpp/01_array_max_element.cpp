#include <iostream>
#include <vector>

using namespace std;

int find_max(vector<int> & v){
  int max=v[0];
  for(int i=1;i<v.size();i++){
    if(v[i]>max){
      max=v[i];
    }
  }
  return max;
}


int main(){
  vector <int> v = {4, 7, 9, 11, 3,};
  cout<<"Max array element:"<<find_max(v)<<'\n';

  return 0;
}
