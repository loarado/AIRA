import bluetooth
ble = bluetooth.BLE()
ble.active(True)
ble.gap_advertise(100000, b'\x02\x01\x06\x0b\x09AIRA Motor')
print('BLE advertising started: AIRA Motor')
