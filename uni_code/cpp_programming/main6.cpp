#include <bits/stdc++.h>
using namespace std;

void display(int arr[1][3]) {
    cout << "Size of one element: " << sizeof(arr[0][0]) << " bytes\n";

    cout << "Total size of array: " << sizeof(arr) << " bytes\n";
}

int main() {

    int arr[] [3]= {10, 20, 30, 40, 50};
    cout << "Size of one element1: " << sizeof(arr[0][0]) << " bytes\n";

    cout << "Total size of array1: " << sizeof(arr) << " bytes\n";

    cout << "Number of elements1: "
         << sizeof(arr) / sizeof(arr[0][0]) << "\n";

    display(arr);

    return 0;
}
