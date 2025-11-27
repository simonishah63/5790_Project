
#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h>

atomic_int shared_counter = 0;
int non_atomic_shared = 0;

void* safe_increment(void* arg) {
    for (int i = 0; i < 1000; i++) atomic_fetch_add(&shared_counter, 1);
    return NULL;
}

void* unsafe_increment(void* arg) {
    for (int i = 0; i < 1000; i++) non_atomic_shared++;
    return NULL;
}

int buffer[100];
int write_index = 0;

void* producer_unsafe(void* arg) {
    for (int i = 0; i < 100; i++) {
        buffer[write_index] = i;
        write_index = (write_index + 1) % 100;
    }
    return NULL;
}

int main() {
    safe_increment(NULL);
    unsafe_increment(NULL);
    producer_unsafe(NULL);
    return 0;
}
