
#include <stdio.h>
#include <stdlib.h>

void buffer_overflow_unsafe(int index) {
    char buffer[10];
    if (index >= 0 && index <= 10) {
        buffer[index] = 'x';
    }
}

void buffer_overflow_safe(int index) {
    char buffer[10];
    if (index >= 0 && index < 10) {
        buffer[index] = 'x';
    }
}

int main() {
    buffer_overflow_unsafe(10);
    buffer_overflow_safe(5);
    return 0;
}

