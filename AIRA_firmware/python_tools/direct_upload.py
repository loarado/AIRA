#!/usr/bin/env python3
"""
Direct serial upload to Pico W - bypasses mpremote entirely
"""
import serial
import time
import sys

def send_command(ser, cmd, wait=0.3):
    """Send a command to the REPL and get response"""
    ser.write(cmd.encode() + b'\r\n')
    time.sleep(wait)
    response = ser.read_all()
    return response

def main():
    # Simple minimal advertising script that won't hang
    script = """
import bluetooth
ble = bluetooth.BLE()
ble.active(True)
adv_data = b'\\x02\\x01\\x06\\x0b\\x09AIRA Motor'
ble.gap_advertise(100000, adv_data)
print('BLE advertising: AIRA Motor')
"""

    try:
        # Open serial connection
        print("Connecting to Pico W on COM9...")
        ser = serial.Serial('COM9', 115200, timeout=1)
        time.sleep(1)
        
        # Interrupt any running code
        print("Interrupting board...")
        for _ in range(5):
            ser.write(b'\x03')  # Ctrl-C
            time.sleep(0.1)
        
        time.sleep(0.5)
        ser.reset_input_buffer()
        
        # Try to access REPL
        print("Entering command mode...")
        ser.write(b'\r\n')
        time.sleep(0.3)
        
        # Create the main.py file using direct REPL
        print("Writing main.py...")
        
        # Use cat command approach
        write_cmd = f"""
with open('/main.py', 'w') as f:
    f.write({repr(script)})
print('Done')
"""
        
        response = send_command(ser, write_cmd, wait=1)
        print("Response:", response)
        
        if b'Done' in response or b'>>>>' in response:
            print("SUCCESS: File uploaded!")
        else:
            print("Response incomplete, trying soft reset...")
            ser.write(b'\x04')  # Ctrl-D
            time.sleep(1)
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
