#include <stdio.h>

int main() {
    int i;
    float numbers[5], total = 0.0, average;

    for(i = 0; i < 5; i++) {
        printf("Enter number %d: ", i + 1);
        scanf("%f", &numbers[i]);
        total += numbers[i];  // Add to total
    }

    // Calculate average
    average = total / 5;

    // Display results
    printf("Total of 5 numbers: %.2f\n", total);
    printf("Average of 5 numbers: %.2f\n", average);

    return 0;
}

