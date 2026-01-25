#include <stdio.h>

int main() {
    int days, years, weeks, remaining_days;

    // Input total days
    printf("Enter total number of days: ");
    scanf("%d", &days);

    // Calculate years
    years = days / 365;         // 1 year = 365 days

    // Remaining days after years
    remaining_days = days % 365;

    // Calculate weeks
    weeks = remaining_days / 7;

    // Remaining days after weeks
    remaining_days = remaining_days % 7;

    // Display the result
    printf("%d days = %d years, %d weeks, and %d days\n", days, years, weeks, remaining_days);

    return 0;
}

