#ifndef BLE_INIT_H
#define BLE_INIT_H

#include <btstack_config.h>
#include <btstack/hci.h>
#include <btstack/l2cap.h>
#include <btstack/gap.h>
#include <stdint.h>
#include <string.h>

// Simple BLE advertising setup
static void start_ble_advertising(const char *name) {
    // Initialize BLE
    l2cap_init();
    
    // Set up GAP
    gap_init();
    gap_set_local_name(name);
    gap_set_appearance(0x0000); // Generic device
    
    // Create advertising data
    uint8_t adv_data[31];
    int adv_data_len = 0;
    
    // Flags
    adv_data[adv_data_len++] = 0x02; // length
    adv_data[adv_data_len++] = 0x01; // type: flags
    adv_data[adv_data_len++] = 0x06; // flags: LE General Discoverable, BR/EDR not supported
    
    // Local name
    int name_len = strlen(name);
    if (name_len > 27) name_len = 27;
    adv_data[adv_data_len++] = name_len + 1;
    adv_data[adv_data_len++] = 0x09; // type: Complete local name
    memcpy(&adv_data[adv_data_len], name, name_len);
    adv_data_len += name_len;
    
    // Set advertising data
    gap_advertisements_set_data(adv_data_len, adv_data);
    
    // Start advertising
    gap_advertisements_enable(1);
    
    printf("BLE advertising started: %s\n", name);
}

#endif
