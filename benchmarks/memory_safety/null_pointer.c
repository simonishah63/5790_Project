
#include <stdio.h>
#include <stdlib.h>

void null_pointer_unsafe(int* ptr, int condition) {
    if (condition) ptr = NULL;
    printf("Value: %d\n", *ptr);
}

void null_pointer_safe(int* ptr, int condition) {
    if (condition) ptr = NULL;
    if (ptr != NULL) printf("Value: %d\n", *ptr);
}

int main() {
    buffer_overflow_unsafe(10);
    buffer_overflow_safe(5);
    
    int x = 42;
    null_pointer_unsafe(&x, 1);
    null_pointer_safe(&x, 0);
    
    return 0;
}
