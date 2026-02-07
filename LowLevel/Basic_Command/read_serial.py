import serial
import time

ser = serial.Serial('COM10', 115200, timeout=1)
time.sleep(1)

print("Reading output from Pico...")
print("-" * 40)

# Read whatever is already there
data = ser.read_all()
if data:
    print(data.decode('utf-8', errors='ignore'))

print("-" * 40)
print("Waiting for more data (5 seconds)...")

for i in range(5):
    data = ser.read_all()
    if data:
        print(data.decode('utf-8', errors='ignore'), end='')
    time.sleep(1)

ser.close()
print("\nDone")
