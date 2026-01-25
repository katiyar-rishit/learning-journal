#include <stdio.h>

int main() {
    FILE *fp;
    char name[50];
    int age;
    float marks;
    fp = fopen("student.txt","w");
    if (fp==NULL){
        printf("Error opening file for writing\n");
        return 1;
    }

    fscanf(fp, "%s %d %f", name, &age, &marks);
    fclose(fp);
    return 0;
}

