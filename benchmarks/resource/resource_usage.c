
#include <stdlib.h>

void potential_infinite_loop(int condition) {
    int i = 0;
    while (condition) {
        i++;
        if (i > 10) break; // ensure termination
    }
}

void memory_leak_unsafe() {
    int* ptr = (int*)malloc(sizeof(int) * 100);
}

void memory_leak_safe() {
    int* ptr = (int*)malloc(sizeof(int) * 100);
    if (ptr) free(ptr);
}

void real_time_bound_unsafe() {
    for (int i = 0; i < 1000; i++) {
        // simulate work
    }
}

int main() {
    potential_infinite_loop(1);
    memory_leak_unsafe();
    memory_leak_safe();
    real_time_bound_unsafe();
    return 0;
}
