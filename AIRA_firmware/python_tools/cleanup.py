import serial
import time

# Force hard interrupt and file deletion
ser = serial.Serial('COM10', 115200, timeout=2)
time.sleep(0.5)

# Send aggressive Ctrl-C to stop any running code
for i in range(10):
    ser.write(b'\x03')
    time.sleep(0.05)

time.sleep(0.5)
ser.reset_input_buffer()
ser.reset_output_buffer()

# Now try to delete main.py and boot.py using raw REPL
ser.write(b'\x01')  # Ctrl-A: enter raw REPL
time.sleep(0.2)

code = """
import os
try:
    os.remove('/main.py')
    print('Deleted main.py')
except:
    print('No main.py')
try:
    os.remove('/boot.py')
    print('Deleted boot.py')
except:
    print('No boot.py')
"""

ser.write(code.encode())
ser.write(b'\x04')  # Ctrl-D: execute
time.sleep(1)

response = ser.read_all()
print('Response:', response)

ser.close()
print('Cleanup complete')
