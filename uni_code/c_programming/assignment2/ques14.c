#include <stdio.h>
#define PI 3.14159265

int main() {
    float radius, volume;

    printf("Enter radius of the sphere: ");
    scanf("%f", &radius);

    // Calculating volume
    volume = (4.0 / 3.0) * PI * radius * radius * radius;

    // Displaying the result
    printf("Volume of the sphere with radius %.2f is %.2f\n", radius, volume);

    return 0;
}

