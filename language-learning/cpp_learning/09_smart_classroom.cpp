#include <iostream>
#include <string>

using namespace std;

class Projector{
  public:void project(string slide){
            cout<<"Projecting:"<<slide;
         }
};


class Speaker{
  public:void speak(string audio){
            cout<<"Playing:"<<audio;
         }
};


class Computer{
  private:string presentation;
          bool running = false;

          Projector& projector;
          Speaker& speaker;

  public:
          Computer(Projector& p, Speaker& s): projector(p), speaker(s){};

          void power(){
            char choice;
            cout<<"Turn the computer on?";
            cin>>choice;
            if (choice=='y'){
              running = true;
            }
            else if (choice=='n'){
              running = false;
            }
            else{
              cout<<"Invalid choice."<<'\n';
            }
          }

          void input(){
            if (running){
              cout<<"Which slide should I play?";
              cin>>presentation;
            }
            else {
              cout<<"Can't play on a dead pc.";
            }
          }

          void play(){
          }
};


int main(){
  return 0;
}
