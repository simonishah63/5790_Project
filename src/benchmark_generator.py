#!/usr/bin/env python3
import os
from pathlib import Path

class BenchmarkGenerator:
    def __init__(self, base_path="benchmarks"):
        self.base_path = Path(base_path)
        self.create_directories()
    
    def create_directories(self):
        """Create benchmark directory structure"""
        directories = [
            "memory_safety",
            "arithmetic", 
            "resource",
            "functional",
            "advanced"
        ]
        for dir_name in directories:
            (self.base_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    def generate_all_benchmarks(self):
        """Generate all benchmark categories"""
        self.generate_memory_safety_benchmarks()
        self.generate_arithmetic_benchmarks()
        self.generate_resource_benchmarks()
        self.generate_functional_benchmarks()
        self.generate_advanced_benchmarks()
        print("✅ All benchmarks generated successfully!")
    
    def generate_memory_safety_benchmarks(self):
        """B1-B2: Memory safety benchmarks"""
        
        buffer_overflow_code = """
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
                buffer_overflow_unsafe(5);
                buffer_overflow_safe(5);
                return 0;
            }
            """

        null_pointer_code = """
            #include <stdio.h>
            #include <stdlib.h>
            
            void null_pointer_unsafe(int* ptr, int condition) {
                if (condition) ptr = NULL;
                printf("Value: %d\\n", *ptr);
            }

            void null_pointer_safe(int* ptr, int condition) {
                if (condition) ptr = NULL;
                if (ptr != NULL) printf("Value: %d\\n", *ptr);
            }

            int main() {
                buffer_overflow_unsafe(10);
                buffer_overflow_safe(5);
                
                int x = 42;
                null_pointer_unsafe(&x, 1);
                null_pointer_safe(&x, 0);
                
                return 0;
            }
            """
        with open(self.base_path / "memory_safety" / "buffer_overflow.c", "w") as f:
            f.write(buffer_overflow_code)
        with open(self.base_path / "memory_safety" / "null_pointer.c", "w") as f:
            f.write(null_pointer_code)
    
    def generate_arithmetic_benchmarks(self):
        """B3: Arithmetic safety benchmarks"""
        
        arithmetic_code = """
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
            """
        with open(self.base_path / "arithmetic" / "arithmetic_safety.c", "w") as f:
            f.write(arithmetic_code)
    
    def generate_resource_benchmarks(self):
        """B4-B5: Resource usage benchmarks"""
        
        resource_code = """
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
            """
        with open(self.base_path / "resource" / "resource_usage.c", "w") as f:
            f.write(resource_code)
    
    def generate_functional_benchmarks(self):
        """B6-B7: Functional correctness benchmarks"""
        
        functional_code = """
            #include <stdbool.h>
            #include <stdio.h>

            /*@ requires divisor != 0;
                ensures \\result == numerator / divisor;
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
            """
        with open(self.base_path / "functional" / "functional_correctness.c", "w") as f:
            f.write(functional_code)
    
    def generate_advanced_benchmarks(self):
        """B9-B10: Advanced benchmarks"""
        
        concurrency_code = """
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
            """
        statemachine_code = """
            #include <stdbool.h>

            #define MAX_SAFE_SPEED 200
            #define MAX_ACCELERATION 10

            typedef enum {
                CRUISE_OFF,
                CRUISE_STANDBY, 
                CRUISE_ACTIVE,
                CRUISE_FAULT
            } cruise_state_t;

            typedef struct {
                cruise_state_t current_state;
                int target_speed;
                int current_speed;
                bool brake_pressed;
            } cruise_control_t;

            bool activate_cruise_control(cruise_control_t* control) {
                if (control->current_state == CRUISE_OFF && 
                    control->current_speed > 30 && 
                    !control->brake_pressed) {
                    control->current_state = CRUISE_STANDBY;
                    return true;
                }
                return false;
            }

            void regulate_speed_safe(cruise_control_t* control) {
                int diff = control->target_speed - control->current_speed;
                if (diff > MAX_ACCELERATION) diff = MAX_ACCELERATION;
                else if (diff < -MAX_ACCELERATION) diff = -MAX_ACCELERATION;
                control->current_speed += diff;
                if (control->current_speed > MAX_SAFE_SPEED) control->current_speed = MAX_SAFE_SPEED;
            }

            int main() {
                cruise_control_t ctrl = {CRUISE_OFF, 100, 0, false};
                activate_cruise_control(&ctrl);
                regulate_speed_safe(&ctrl);
                return 0;
            }
            """
        with open(self.base_path / "advanced" / "concurrency_safety.c", "w") as f:
            f.write(concurrency_code)
        
        with open(self.base_path / "advanced" / "cruise_control.c", "w") as f:
            f.write(statemachine_code)

if __name__ == "__main__":
    generator = BenchmarkGenerator()
    generator.generate_all_benchmarks()
