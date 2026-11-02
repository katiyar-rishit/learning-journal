#include <iostream>
#include <algorithm>
#include <map>
#include <unordered_map>
#include <string>
#include <set>
#include <stack>
#include <queue>

int main(){
  using namespace std;

  //map (dictionary)
  map <int,int> mp;
  mp[5]=10;
  cout << mp[5];


  //unordered_map
  unordered_map <string,int> grades;
  grades["Maths"]=87;
  grades["Digital System"]=87;
  grades["Semiconductor"]=98;


  //set
  set <int> s;
  s.insert(5);


  //stack
  stack <int> st;
  st.push(10);
  st.push(5);
  st.push(3);
  st.pop();


  //queue
  queue <int> q;
  q.push(5);
  q.push(10);
  q.push(15);
  q.pop();


  //priority queue (heap)
  priority_queue<int> pq; //max heap
  priority_queue<int, vector<int>, greater<int>> pq1;

  return 0;
}
