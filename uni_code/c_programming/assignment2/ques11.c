#include <stdio.h>

int main() {
    float kilometers, miles;

    // Ask user to input kilometers
    printf("Enter distance in kilometers: ");
    scanf("%f", &kilometers);

    // Conversion formula: 1 km = 0.621371 miles
    miles = kilometers * 0.621371;

    // Display the result
    printf("%.2f kilometers is equal to %.2f miles.\n", kilometers, miles);

    return 0;
}

