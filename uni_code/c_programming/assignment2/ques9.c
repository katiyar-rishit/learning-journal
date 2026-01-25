#include <stdio.h>
#include <math.h>

int main() {
    double principal, rate, time, amount, compound_interest;
    printf("Enter principal amount: ");
    scanf("%lf", &principal);

    printf("Enter annual interest rate (in %%): ");
    scanf("%lf", &rate);

    printf("Enter time in years: ");
    scanf("%lf", &time);

    // Compound Interest formula: A = P * (1 + R/100)^T
    amount = principal * pow(1 + rate / 100, time);

    // Compound Interest = Amount - Principal
    compound_interest = amount - principal;

    printf("Compound interest: %.2lf\n", compound_interest);
    printf("Total amount: %.2lf\n", amount);

    return 0;
}

