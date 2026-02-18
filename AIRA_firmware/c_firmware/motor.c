#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include <math.h>
#include "motor.h"





struct motor init_motor(uint in1, uint in2, uint pwm){
    struct motor m;
    m.in1 = in1;
    m.in2 = in2;
    m.pwm = pwm;
    m.pwm_slice = pwm_gpio_to_slice_num(pwm);
    m.pwm_channel = pwm_gpio_to_channel(pwm);
    // Initing all the gpios
    gpio_init(in1);
    gpio_set_dir(in1, GPIO_OUT);
    gpio_put(in1, false);

    gpio_init(in2);
    gpio_set_dir(in2, GPIO_OUT);
    gpio_put(in2, false);

    gpio_set_function(pwm, GPIO_FUNC_PWM);
    pwm_set_wrap(m.pwm_slice, PWM_WRAP);
    pwm_set_chan_level(m.pwm_slice, m.pwm_channel, 0);
    pwm_set_enabled(m.pwm_slice, true);

    return m;
}

void forward(struct motor m){
    gpio_put_masked(1 << m.in1 | 1 << m.in2, 1 << m.in2);
}

void backward(struct motor m){
    gpio_put_masked(1 << m.in1 | 1 << m.in2, 1 << m.in1);
}

void idle(struct motor m){
    gpio_put_masked(1 << m.in1 | 1 << m.in2, 0);
}

void set_pwm(struct motor m, float duty_cycle){ // Duty cycle in between 0 and 1
    pwm_set_chan_level(m.pwm_slice, m.pwm_channel, (int) round(duty_cycle * PWM_WRAP));
}
