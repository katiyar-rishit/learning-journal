#include <iostream>
#include <vector>

using namespace std;

int arr_frequency(vector<int> &v,int key){
  int frequency = {0};
  for(int i=0;i<v.size();i++){
    if(v[i]==key){
      frequency+=1;
    }
  }
  return frequency;
}

int main(){
  vector<int> v;
  cout<<"Enter number of element of array:"<<'\n';
  int n;
  cin>>n;
  cout<<"Enter elements:"<<'\n';
  for(int i=0;i<n;i++){
    cout<<"Enter element "<<i<<'\n';
    cin>>v[i];
  }
   
  cout<<"Enter number whose frequency you want:"<<'\n';
  int key;
  cin>>key;
  cout<<"Frequency of "<<key<<"in array: "<<arr_frequency(v, key)<<'\n';

  return 0;
}
