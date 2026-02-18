#!/usr/bin/env python3
"""
Direct upload of BLE + motor control script to Pico W via serial.
Uploads the full GATT server + motor control main.py.
"""
import serial
import time

# The full BLE GATT + motor control script
ble_script = """
import bluetooth
import time
import sys
import select
from machine import Pin, PWM
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_NUS_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_NUS_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY,)
_NUS_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE,)
_NUS_SERVICE = (_NUS_UUID, (_NUS_TX, _NUS_RX),)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)


class Motor:
    def __init__(self, in1_pin, in2_pin, pwm_pin):
        self.in1 = Pin(in1_pin, Pin.OUT, value=0)
        self.in2 = Pin(in2_pin, Pin.OUT, value=0)
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(10000)
        self.pwm.duty_u16(0)

    def forward(self):
        self.in1.value(1)
        self.in2.value(0)

    def backward(self):
        self.in1.value(0)
        self.in2.value(1)

    def idle(self):
        self.in1.value(0)
        self.in2.value(0)

    def set_speed(self, duty):
        self.pwm.duty_u16(int(duty * 65535))


m_front_left = Motor(3, 4, 2)
m_front_right = Motor(6, 7, 5)
m_rear_left = Motor(26, 27, 28)
m_rear_right = Motor(20, 21, 22)
motors = [m_front_left, m_front_right, m_rear_left, m_rear_right]


def handle_command(cmd):
    if cmd == 'z':
        for m in motors:
            m.forward()
            m.set_speed(1.0)
        return "Forward"
    elif cmd == 's':
        for m in motors:
            m.backward()
            m.set_speed(1.0)
        return "Backward"
    elif cmd == 'q':
        m_front_right.forward()
        m_rear_right.forward()
        m_front_left.backward()
        m_rear_left.backward()
        for m in motors:
            m.set_speed(1.0)
        return "Turn Left"
    elif cmd == 'd':
        m_front_left.forward()
        m_rear_left.forward()
        m_front_right.backward()
        m_rear_right.backward()
        for m in motors:
            m.set_speed(1.0)
        return "Turn Right"
    else:
        for m in motors:
            m.idle()
            m.set_speed(0)
        return "Idle"


def build_advertising_payload(name):
    payload = bytearray()
    payload += bytearray([2, _ADV_TYPE_FLAGS, 0x06])
    name_bytes = name.encode()
    payload += bytearray([len(name_bytes) + 1, _ADV_TYPE_NAME]) + name_bytes
    return payload


class BLEUART:
    def __init__(self, name="AIRA Motor"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_NUS_SERVICE,))
        self._conn_handle = None
        self._name = name
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._conn_handle = conn_handle
            print("BLE connected")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._conn_handle = None
            print("BLE disconnected")
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            if attr_handle == self._rx_handle:
                msg = self._ble.gatts_read(self._rx_handle)
                if msg:
                    for byte in msg:
                        cmd = chr(byte)
                        result = handle_command(cmd)
                        print("BLE cmd:", cmd, "->", result)
                        self._send(result + "\\n")

    def _send(self, text):
        if self._conn_handle is not None:
            self._ble.gatts_notify(self._conn_handle, self._tx_handle, text.encode())

    def _advertise(self):
        payload = build_advertising_payload(self._name)
        self._ble.gap_advertise(100000, payload)
        print("BLE advertising:", self._name)


def main():
    print("AIRA Motor Controller - MicroPython")
    print("Commands: z=forward, s=backward, q=left, d=right, a=idle")
    uart = BLEUART("AIRA Motor")
    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)
    print("Ready. Accepting commands via BLE and serial.")
    while True:
        if poll.poll(0):
            cmd = sys.stdin.read(1)
            if cmd:
                result = handle_command(cmd)
                print("Serial cmd:", cmd, "->", result)
        time.sleep_ms(10)


main()
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
    print("Uploading GATT + motor control script...")
    write_code = f"""
with open('/main.py', 'w') as f:
    f.write({repr(ble_script)})
print('\\nScript uploaded to /main.py')
"""

    ser.write(write_code.encode())
    ser.write(b'\x04')  # Ctrl-D to execute
    time.sleep(1)

    # Read response
    response = ser.read_all()
    print("Response:", response.decode('utf-8', errors='ignore'))

    if b'uploaded' in response:
        print("\nSUCCESS: Script uploaded!")
        print("\nResetting board to run /main.py...")
        time.sleep(0.5)
        ser.write(b'\x04')  # Ctrl-D soft reset
        time.sleep(2)

        # Check for startup message
        startup = ser.read_all()
        if startup:
            print("Board output:", startup.decode('utf-8', errors='ignore'))
    else:
        print("\nUpload may have failed. Response:", response)

    ser.close()
    print("\nDone! Pico W should now be running AIRA Motor Controller with BLE GATT.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
