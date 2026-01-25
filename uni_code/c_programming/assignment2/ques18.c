#include <stdio.h>

int main() {
    int hours, minutes, seconds;

    // Input hours from user
    printf("Enter hours: ");
    scanf("%d", &hours);

    // Convert hours to minutes and seconds
    minutes = hours * 60;
    seconds = hours * 3600;

    // Display the results
    printf("%d hours = %d minutes = %d seconds\n", hours, minutes, seconds);

    return 0;
}

