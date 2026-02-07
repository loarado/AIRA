import serial
import time

ser = serial.Serial('COM10', 115200, timeout=1)
time.sleep(0.5)

print("Sending test character...")
ser.write(b'z')
time.sleep(0.5)

print("Reading response...")
data = ser.read_all()
if data:
    output = data.decode('utf-8', errors='ignore')
    print("Output from Pico:")
    print(output)
else:
    print("No response")

ser.close()
