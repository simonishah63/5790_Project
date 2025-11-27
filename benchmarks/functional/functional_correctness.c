
#include <stdbool.h>
#include <stdio.h>

/*@ requires divisor != 0;
    ensures \result == numerator / divisor;
*/
int safe_division(int numerator, int divisor) {
    return numerator / divisor;
}

int unsafe_division(int numerator, int divisor) {
    return numerator / divisor;
}

void misra_unsafe_cast() {
    int x = 10;
    char* ptr = (char*)x;
}

void misra_loop_violation() {
    int i = 0;
    while (i < 10) {
        i++;
    }
}

int main() {
    safe_division(10,2);
    unsafe_division(10,2);
    misra_unsafe_cast();
    misra_loop_violation();
    return 0;
}
