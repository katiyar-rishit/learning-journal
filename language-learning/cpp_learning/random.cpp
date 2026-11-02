#include <iostream>
#include <string>

using namespace std;

class Dwarf{
  private:
    string name;
    string profession;
  
  public:
    Dwarf(string n, string p){
      name = n;
      profession = p;
    }
    void greet(string adv_name){
      cout<<"Greetings and welcome to Camreltone the city of dwarves young adventurer.I am "<< name <<" and will be acting as your guide."<<endl;
    }


};

int main(){
  string adv_name;
  cout<<"State your name: ";
  cin>>adv_name;
  char choice;
  cout<<"Would you like to talk to a guide?(y/n)";
  cin>>choice;
  if (choice=='y'){
    Dwarf d1("Helmor", "guide");
    d1.greet(adv_name);
  }else if (choice=='n'){
    cout<<"Well enjoy your time then.";
  }else{
    cout<<"I am afraid I dont understand your tongue ,maybe you are from some foreign continent.Well hope you leave promptly scum.";
  }



  return 0;
}
