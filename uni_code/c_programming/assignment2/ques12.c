#include <stdio.h>
#include <math.h>

int main() {
    double base, exponent, result;

    printf("Enter base: ");
    scanf("%lf", &base);

    printf("Enter exponent: ");
    scanf("%lf", &exponent);

    // Calculating power
    result = pow(base, exponent);

    // Displaying the result
    printf("%.2lf raised to the power %.2lf is %.2lf\n", base, exponent, result);

    return 0;
}

