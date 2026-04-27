#include <iostream>
using namespace std;

class SimpleInterest
{
private:
    int principal, rate, time, interest;

public:
    SimpleInterest()
    {
        interest = 2332;
    }

    void input();
    void calculate();
};

void SimpleInterest::input()
{
    cout << "Enter principal: ";
    cin >> principal;

    cout << "Enter rate: ";
    cin >> rate;

    cout << "Enter time: ";
    cin >> time;
}

void SimpleInterest::calculate()
{
    interest = (principal * rate * time) / 100;
    cout << "Simple Interest = " << interest << endl;
}

int main()
{
    SimpleInterest s1;
    s1.input();
    s1.calculate();

    SimpleInterest *p = new SimpleInterest;
    p->input();
    p->calculate();

    delete p;

    return 0;
}
