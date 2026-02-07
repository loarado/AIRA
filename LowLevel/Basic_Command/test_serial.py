import serial
import time
import sys

def send_raw_repl_command(ser, code):
    """Send command in raw REPL mode"""
    # Enter raw mode with Ctrl-A
    ser.write(b'\x01')
    time.sleep(0.1)
    
    # Send code
    ser.write(code.encode() + b'\x04')
    time.sleep(0.2)
    
    # Read response
    response = ser.read_all()
    return response

try:
    # Open and reset port
    ser = serial.Serial('COM10', 115200, timeout=2)
    ser.reset_input_buffer()
    
    # Try to connect with multiple Ctrl-C
    for i in range(5):
        ser.write(b'\x03')
        time.sleep(0.1)
    
    time.sleep(0.5)
    ser.reset_input_buffer()
    
    # Test basic command
    ser.write(b'print("test")\r\n')
    time.sleep(0.5)
    response = ser.read_all()
    print("Response:", response)
    
    if b'test' in response:
        print("SUCCESS: Board is responding!")
    else:
        print("WARNING: Unexpected response")
    
    ser.close()
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
