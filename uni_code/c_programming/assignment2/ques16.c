#include <stdio.h>

int main() {
    float rupees, dollars;
    float exchange_rate = 0.012; // Approximate conversion: 1 INR = 0.012 USD

    // Input amount in rupees
    printf("Enter amount in rupees: ");
    scanf("%f", &rupees);

    // Convert to dollars
    dollars = rupees * exchange_rate;

    // Display the result
    printf("%.2f rupees is equal to %.2f dollars\n", rupees, dollars);

    return 0;
}

