
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
