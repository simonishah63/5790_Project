
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

// B2: Null pointer dereference
void null_pointer_unsafe(int* ptr, int condition) {
    if (condition) ptr = NULL;
    printf("Value: %d\n", *ptr);
}

void null_pointer_safe(int* ptr, int condition) {
    if (condition) ptr = NULL;
    if (ptr != NULL) printf("Value: %d\n", *ptr);
}

// Auto-generated main() for CBMC/Frama-C/E-ACSL
int main() {
    buffer_overflow_unsafe(10);
    buffer_overflow_safe(5);
    
    int x = 42;
    null_pointer_unsafe(&x, 1);
    null_pointer_safe(&x, 0);
    
    return 0;
}
