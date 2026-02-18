#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/uart.h"

#include "motor_config.h"
#include "motor.h"




int main()
{
    stdio_init_all();

    // Initialise the Wi-Fi chip
    if (cyw43_arch_init()) {
        printf("Wi-Fi init failed\n");
        return -1;
    }

    // Example to turn on the Pico W LED
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    printf("LED ON - Pico W is running\n");

    // Init all the motor
    struct motor m_rear_left = init_motor(Motor_Rear_Left_IN1, Motor_Rear_Left_IN2, Motor_Rear_Left_PWM);
    struct motor m_rear_right = init_motor(Motor_Rear_Right_IN1, Motor_Rear_Right_IN2, Motor_Rear_Right_PWM);
    struct motor m_front_left = init_motor(Motor_Front_Left_IN1, Motor_Front_Left_IN2, Motor_Front_Left_PWM);
    struct motor m_front_right = init_motor(Motor_Front_Right_IN1, Motor_Front_Right_IN2, Motor_Front_Right_PWM);

    struct motor motors[4] = {m_front_left, m_front_right, m_rear_left, m_rear_right};

    char command; 
    while (true){
        command = getchar();
        switch(command){
        case 'z':
            for (int i = 0; i < 4; i++){
                forward(motors[i]);
                set_pwm(motors[i],1);
            }
            break;
        case 's':
            for (int i = 0; i < 4; i++){
                backward(motors[i]);
                set_pwm(motors[i],1);
            }
            break;
        case 'q':
        //LEFT TURN
            forward(m_front_right);
            forward(m_rear_right);
            backward(m_front_left);
            backward(m_rear_left);
            for (int i = 0; i < 4; i++){
                set_pwm(motors[i],1);
            }
            break;
        case 'd':
        //RIGHT TURN
            forward(m_front_left);
            forward(m_rear_left);
            backward(m_front_right);
            backward(m_rear_right);
            for (int i = 0; i < 4; i++){
                set_pwm(motors[i],1);
            }
            break;
        default:
            for (int i = 0; i < 4; i++){
                idle(motors[i]);
                set_pwm(motors[i],0);
            }
        }
    }

    /* // Move forward 1 second
    for (int i = 0; i < 4; i++){
        forward(motors[i]);
    }
    sleep_ms(2000);

    // idle 4 second 
    for (int i = 0; i < 4; i++){
        idle(motors[i]);
    }
    sleep_ms(4000);

    // Move backward 1 second
    for (int i = 0; i < 4; i++){
        backward(motors[i]);
    }
    sleep_ms(2000);

    // idle 4 second 
    for (int i = 0; i < 4; i++){
        idle(motors[i]);
    }
    sleep_ms(4000);

    // turn clockwise for 1 second
    forward(m_front_left);
    forward(m_rear_left);
    backward(m_front_right);
    backward(m_rear_right);
    sleep_ms(2000);

    // idle 4 second 
    for (int i = 0; i < 4; i++){
        idle(motors[i]);
    }
    sleep_ms(4000);

    // turn counterclockwise for 1 second
    forward(m_front_right);
    forward(m_rear_right);
    backward(m_front_left);
    backward(m_rear_left);
    sleep_ms(2000);



    for (int i = 0; i < 4; i++){
        idle(motors[i]);
    }

    */
}
