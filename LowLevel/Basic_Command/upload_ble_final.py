#!/usr/bin/env python3
"""
Direct upload of BLE advertising script to Pico W via serial
"""
import serial
import time

# The BLE advertising script
ble_script = """
import bluetooth

def start_ble():
    ble = bluetooth.BLE()
    ble.active(True)
    
    # Simple BLE advertising payload
    # Format: flags (2 bytes) + name (variable)
    name = b'AIRA Motor'
    adv_data = bytes([
        0x02, 0x01, 0x06,  # Flags: LE General Discoverable, BR/EDR not supported
        len(name) + 1, 0x09  # Complete local name
    ]) + name
    
    # Start advertising
    ble.gap_advertise(100000, adv_data)
    print('BLE Advertising: AIRA Motor')

# Run on boot
start_ble()
"""

try:
    print("Connecting to Pico W on COM9...")
    ser = serial.Serial('COM9', 115200, timeout=1)
    time.sleep(1)
    
    # Send Ctrl-C multiple times to interrupt any running code
    print("Interrupting any running code...")
    for _ in range(5):
        ser.write(b'\x03')
        time.sleep(0.05)
    
    time.sleep(0.5)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    # Send Ctrl-A to enter raw REPL
    print("Entering raw REPL...")
    ser.write(b'\x01')
    time.sleep(0.2)
    
    # Create the main.py file
    print("Uploading BLE script...")
    write_code = f"""
with open('/main.py', 'w') as f:
    f.write({repr(ble_script)})
print('\\nBLE script uploaded to /main.py')
"""
    
    ser.write(write_code.encode())
    ser.write(b'\x04')  # Ctrl-D to execute
    time.sleep(1)
    
    # Read response
    response = ser.read_all()
    print("Response:", response.decode('utf-8', errors='ignore'))
    
    if b'uploaded' in response:
        print("\n✓ SUCCESS: BLE script uploaded!")
        print("\nResetting board to run /main.py...")
        time.sleep(0.5)
        ser.write(b'\x04')  # Ctrl-D soft reset
        time.sleep(2)
        
        # Check for startup message
        startup = ser.read_all()
        if startup:
            print("Board output:", startup.decode('utf-8', errors='ignore'))
    else:
        print("\n✗ Upload may have failed. Response:", response)
    
    ser.close()
    print("\nDone! Pico W should now be advertising as 'AIRA Motor'")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
