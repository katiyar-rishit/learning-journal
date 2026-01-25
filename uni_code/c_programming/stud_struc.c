#include <stdio.h>

struct student {
    char name[50];
    char dob[15];
    int roll;
    char address[3][50];
};

int main() {
    int n;
    printf("Enter number of students: ");
    scanf("%d", &n);

    struct student s[n];

    for (int i = 0; i < n; i++) {   
        printf("\n--- Enter details of student %d ---\n", i + 1);

        printf("Roll No: ");
        scanf("%d", &s[i].roll);

        printf("Name: ");
        scanf(" %[^\n]", s[i].name);

        printf("Date of Birth (DD/MM/YYYY): ");
        scanf(" %[^\n]", s[i].dob);

        printf("Enter Address (3 lines):\n");
        for (int j = 0; j < 3; j++) {   
            printf("Line %d: ", j + 1);
            scanf(" %[^\n]", s[i].address[j]);
        }
    }

    printf("\n\n--- Student Details ---\n");
    for (int i = 0; i < n; i++) {
        printf("\nStudent %d\n", i + 1);
        printf("Roll No: %d\n", s[i].roll);
        printf("Name: %s\n", s[i].name);
        printf("DOB: %s\n", s[i].dob);
        printf("Address:\n");
        for (int j = 0; j < 3; j++) {
            printf("  %s\n", s[i].address[j]);
        }
    }

    return 0;
}

