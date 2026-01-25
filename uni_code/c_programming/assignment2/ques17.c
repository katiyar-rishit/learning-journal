#include <stdio.h>

int main() {
    float weight, height, bmi;

    // Input weight and height
    printf("Enter weight in kilograms: ");
    scanf("%f", &weight);

    printf("Enter height in meters: ");
    scanf("%f", &height);

    // Calculate BMI
    bmi = weight / (height * height);

    // Display result
    printf("Your BMI is: %.2f\n", bmi);

    return 0;
}

