
#include <stdio.h>
#include <limits.h>

int integer_overflow_unsafe(int a, int b) {
    return a + b;
}

int integer_overflow_safe(int a, int b) {
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) return 0;
    return a + b;
}

int division_by_zero_unsafe(int a, int b) {
    return a / b;
}

int division_by_zero_safe(int a, int b) {
    if (b == 0) return 0;
    return a / b;
}

int main() {
    integer_overflow_unsafe(INT_MAX, 1);
    integer_overflow_safe(INT_MAX, 1);
    division_by_zero_unsafe(10, 0);
    division_by_zero_safe(10, 2);
    return 0;
}
