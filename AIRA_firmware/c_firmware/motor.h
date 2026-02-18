#ifndef PWM_WRAP
#define PWM_WRAP 12501 // => pwm_frequency = 10kH 
#endif


struct motor {
    uint in1;
    uint in2;
    uint pwm;
    uint pwm_slice;
    uint pwm_channel;
};

struct motor init_motor(uint in1, uint in2, uint pwm); // init all gpios and setup the pwm
void forward(struct motor m);
void backward(struct motor m);
void idle(struct motor m);
void set_pwm(struct motor m, float duty_cycle); // duty cycle between 0 and 1
