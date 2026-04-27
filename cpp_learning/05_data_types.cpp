#include <iostream>
#include <string>
#include <vector>

int main(){
  
  using namespace std;

  int x = 10;
  long long y = 1e16;
  char c = 'B';
  string first_name;
  string name;

  cin >> first_name;
  getline(cin, name);

  //vectors
  vector<int> v;
  v.push_back(10);
  v.push_back(20);

  for(int i=0;i<v.size();i++){
    cout << v[i] << '\n';
  }


  //references
  int z = 10;
  int &a = z;
  a++;
  cout << z << '\n';


  return 0;
}
