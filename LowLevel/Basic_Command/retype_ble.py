#!/usr/bin/env python3
"""
Upload BLE script via simulated typing into MicroPython REPL
"""
import subprocess
import time

# Simple BLE script - very minimal
ble_code = """import bluetooth
ble=bluetooth.BLE()
ble.active(True)
ble.gap_advertise(100000,b'\\x02\\x01\\x06\\x0a\\x09AIRA Motor')
print('BLE advertising')
"""

commands = [
    # Enter raw REPL
    "python -m mpremote connect COM9 repl",
]

# Try connecting with mpremote and send commands via stdin
try:
    print("Attempting to connect via mpremote...")
    proc = subprocess.Popen(
        ["python", "-m", "mpremote", "connect", "COM9", "repl"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for REPL prompt
    time.sleep(2)
    
    # Send the code line by line
    print("Sending BLE code...")
    for line in ble_code.strip().split('\n'):
        print(f"Sending: {line}")
        proc.stdin.write(line + '\n')
        proc.stdin.flush()
        time.sleep(0.3)
    
    # Exit REPL
    proc.stdin.write('\x1d')  # Ctrl-]
    proc.stdin.flush()
    
    # Read output
    time.sleep(1)
    proc.terminate()
    stdout, stderr = proc.communicate(timeout=2)
    
    if stdout:
        print("Output:", stdout)
    if stderr:
        print("Errors:", stderr)
    
except Exception as e:
    print(f"Error: {e}")
