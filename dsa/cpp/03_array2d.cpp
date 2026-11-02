#include <iostream>
#include <vector>
using namespace std;

class Solution{
  public:
    void Arithmetic(vector<vector<int>> num1, vector<vector<int>> num2){
      vector<vector<int>> sum(num1.size(), vector<int> n);
      
      for(int i=0;i<num1.size();i++){
        for(int j=0;j<num1[0].size();j++){
          int s = 0;
          vector<int> su;
          s = num1[i][j] + num2[i][j];
          su.push_back(s);
        }
        sum.push_back(su);
      }

      cout<< sum;
    }
  
};

int main(){
  vector<vector<int>> n1 = [[1,2,3],[4,5,6],[7,8,9]];
  vector<vector<int>> n2 = [[3,2,1],[6,5,4],[9,8,7]];

  Solution s1;
  s1.Arithmeticl(n1, n2);

  return 0;
}
