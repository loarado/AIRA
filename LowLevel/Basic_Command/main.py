import bluetooth
ble = bluetooth.BLE()
ble.active(True)
adv = bytearray([2,1,6,10,9]) + b'AIRA Motor'
ble.gap_advertise(100000, adv)
print('BLE advertising: AIRA Motor')
