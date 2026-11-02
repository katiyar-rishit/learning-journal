#include <cmath>
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    constexpr int WIDTH = 80;
    constexpr int HEIGHT = 40;

    float A = 0.0f; // rotation around X
    float B = 0.0f; // rotation around Z

    // Hide cursor
    std::cout << "\033[?25l";

    while (true) {
        char output[HEIGHT][WIDTH];
        float zbuffer[HEIGHT][WIDTH];

        // Clear frame
        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                output[y][x] = ' ';
                zbuffer[y][x] = 0.0f;
            }
        }

        // Generate donut
        for (float theta = 0; theta < 2 * M_PI; theta += 0.07f) {
            for (float phi = 0; phi < 2 * M_PI; phi += 0.02f) {

                float costheta = cos(theta);
                float sintheta = sin(theta);
                float cosphi = cos(phi);
                float sinphi = sin(phi);

                // Donut dimensions
                float R1 = 1.0f;
                float R2 = 2.0f;

                float circlex = R2 + R1 * costheta;
                float circley = R1 * sintheta;

                // 3D point after rotation
                float x =
                    circlex *
                    (cosphi * cos(B) + sinphi * sin(A) * sin(B))
                    - circley * cos(A) * sin(B);

                float y =
                    circlex *
                    (cosphi * sin(B) - sinphi * sin(A) * cos(B))
                    + circley * cos(A) * cos(B);

                float z =
                    circlex * sinphi * cos(A)
                    + circley * sin(A)
                    + 5.0f;

                // Projection
                float invz = 1.0f / z;

                int xp = static_cast<int>(WIDTH / 2 + 30 * invz * x);
                int yp = static_cast<int>(HEIGHT / 2 - 15 * invz * y);

                // Surface normal
                float nx =
                    costheta *
                    (cosphi * cos(B) + sinphi * sin(A) * sin(B))
                    - sintheta * cos(A) * sin(B);

                float ny =
                    costheta *
                    (cosphi * sin(B) - sinphi * sin(A) * cos(B))
                    + sintheta * cos(A) * cos(B);

                float nz =
                    costheta * sinphi * cos(A)
                    + sintheta * sin(A);

                // Light direction
                float Lx = -0.4f;
                float Ly = 0.7f;
                float Lz = -1.0f;

                float luminance =
                    nx * Lx +
                    ny * Ly +
                    nz * Lz;

                // Clamp
                if (luminance < 0)
                    luminance = 0;

                // ASCII brightness
                const char* shades = ".,-~:;=!*#$@";
                int shadeIndex =
                    static_cast<int>(luminance * 11);

                if (shadeIndex > 11)
                    shadeIndex = 11;

                if (xp >= 0 && xp < WIDTH &&
                    yp >= 0 && yp < HEIGHT) {

                    if (invz > zbuffer[yp][xp]) {
                        zbuffer[yp][xp] = invz;
                        output[yp][xp] = shades[shadeIndex];
                    }
                }
            }
        }

        // Move cursor to top-left instead of clearing terminal
        std::cout << "\033[2J\033[H";

        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                std::cout << output[y][x];
            }
            std::cout << '\n';
        }

        // Rotation
        A += 0.04f;
        B += 0.02f;

        std::this_thread::sleep_for(
            std::chrono::milliseconds(30)
        );
    }

    // Show cursor again
    std::cout << "\033[?25h";
}
