import serial
import time
import os

# Read the local file
with open('ble_advertizing.py', 'r') as f:
    code = f.read()

print(f"Uploading {len(code)} bytes...")

# Connect to board
ser = serial.Serial('COM10', 115200, timeout=2)
time.sleep(0.5)

# Interrupt any running code
for i in range(5):
    ser.write(b'\x03')
    time.sleep(0.05)

time.sleep(0.5)
ser.reset_input_buffer()

# Enter raw REPL mode
ser.write(b'\x01')  # Ctrl-A
time.sleep(0.2)

# Write the file using raw REPL
write_cmd = f"""
with open('/main.py', 'w') as f:
    f.write({repr(code)})
print('File written')
"""

ser.write(write_cmd.encode())
ser.write(b'\x04')  # Ctrl-D to execute
time.sleep(2)

response = ser.read_all()
print('Response:', response)

if b'File written' in response:
    print("SUCCESS: File uploaded!")
    
    # Now reset the board
    time.sleep(0.5)
    ser.write(b'\x04')  # Ctrl-D to soft reset
    time.sleep(1)
else:
    print("WARNING: Upload may have failed")
    print("Full response:", response)

ser.close()
