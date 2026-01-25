#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    printf("Enter no. of student:");
    scanf("%d", &n);
    
    int *marks = (int*)malloc(n*sizeof(int));
    if (marks == NULL){
      printf("Memory allocation failed");
    }

    for (int i=0;i<n;i++){
        printf("Enter marks:");
        scanf("%d", &marks[i]);
    }
    
    for (int i=0;i<n;i++){
        printf("Student %d: %d\n", i + 1, marks[i]);
    } 
    
    char choice;
    printf("Want to resize no. of students?(Y/N):");
    scanf(" %c",&choice);
    if (choice == 'Y'){
        int new_n;
        printf("Enter new no. of student:");
        scanf("%d",&new_n);
        
        int *temp = (int*)realloc(marks, new_n * sizeof(int));

        if(temp == NULL){
          printf("Memory allocation failed.");
        }
        
        marks = temp;

        for (int i = n; i < new_n; i++) {
            printf("Enter marks of student %d: ", i + 1);
            scanf(" %d", &marks[i]);
        }

        n = new_n;
        
        printf("Final student list");
        for (int i=0;i<n;i++){
            printf("Student %d: %d\n", i + 1, marks[i]);
        }
    }
    free(marks);
    
    return 0;
}

