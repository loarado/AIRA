import pygame
import time
import serial
import sys


Deadzone = 0.075 # Deadzone value change between controller
A_Button = 2

################
def calibration(input, range=1): # Apply the deadzone and rescale the input (between -range and range)
    if -Deadzone < input < Deadzone:
        return 0
    elif input > 0:
        return (input - Deadzone) / (1 - Deadzone) * range
    else:
        return (input + Deadzone) / (1 - Deadzone) * range

################


pygame.init()
controller = pygame.joystick.Joystick(0)
port = sys.argv[1] if len(sys.argv) > 1 else "COM9"
s = serial.Serial(port=port, baudrate=115200, timeout=1)
s.flush()

while True:
    pygame.event.pump() # Don't need it if pygame.event.get is called
    if not controller.get_button(A_Button) :
        up_down_axis = controller.get_axis(1)
        left_right_axis = controller.get_axis(0)
        if calibration(up_down_axis) > 0.5:
            s.write('s'.encode("ascii"))
            print('s')
        elif calibration(up_down_axis) < -0.5:
            s.write('z'.encode("ascii"))
            print('z')
        elif calibration(left_right_axis) > 0.5:
            s.write('d'.encode("ascii"))
            print('d')
        elif calibration(left_right_axis) < -0.5:
            s.write('q'.encode("ascii"))
            print('q')
        else:
            s.write('a'.encode("ascii")) 
            print("a")

        
    else:
        s.write('e'.encode("ascii"))
        print("e")


    time.sleep(0.1)