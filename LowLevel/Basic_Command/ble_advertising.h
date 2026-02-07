#ifndef BLE_ADVERTISING_H
#define BLE_ADVERTISING_H

#include <stdint.h>
#include <string.h>

// Advertising payload type constants
#define ADV_TYPE_FLAGS 0x01
#define ADV_TYPE_NAME 0x09
#define ADV_TYPE_UUID16_COMPLETE 0x3
#define ADV_TYPE_UUID32_COMPLETE 0x5
#define ADV_TYPE_UUID128_COMPLETE 0x7
#define ADV_TYPE_APPEARANCE 0x19

// Helper function to append data to advertising payload
static inline void append_to_payload(uint8_t *payload, int *payload_len, uint8_t adv_type, const uint8_t *value, int value_len) {
    payload[(*payload_len)++] = value_len + 1;
    payload[(*payload_len)++] = adv_type;
    memcpy(&payload[*payload_len], value, value_len);
    *payload_len += value_len;
}

// Generate advertising payload (based on ble_advertizing.py)
// Returns the length of the payload
static inline int create_advertising_payload(uint8_t *payload, int max_len, 
                                            const char *device_name, 
                                            const uint16_t *uuid16_services, 
                                            int num_services) {
    int payload_len = 0;
    
    // Add flags (LE General Discoverable, BR/EDR Not Supported)
    uint8_t flags = 0x06;
    if (payload_len + 3 <= max_len) {
        append_to_payload(payload, &payload_len, ADV_TYPE_FLAGS, &flags, 1);
    }
    
    // Add device name if provided
    if (device_name) {
        int name_len = strlen(device_name);
        if (payload_len + 2 + name_len <= max_len) {
            append_to_payload(payload, &payload_len, ADV_TYPE_NAME, (const uint8_t *)device_name, name_len);
        }
    }
    
    // Add UUID16 services
    for (int i = 0; i < num_services && payload_len + 4 <= max_len; i++) {
        uint8_t uuid_bytes[2];
        uuid_bytes[0] = uuid16_services[i] & 0xFF;
        uuid_bytes[1] = (uuid16_services[i] >> 8) & 0xFF;
        append_to_payload(payload, &payload_len, ADV_TYPE_UUID16_COMPLETE, uuid_bytes, 2);
    }
    
    return payload_len;
}

// Decode advertising field from payload
static inline int decode_field(const uint8_t *payload, int payload_len, uint8_t adv_type, uint8_t *result, int max_result_len) {
    int i = 0;
    int result_len = 0;
    
    while (i + 1 < payload_len) {
        if (payload[i + 1] == adv_type) {
            int field_len = payload[i];
            if (field_len > 0 && i + field_len < payload_len && result_len + field_len - 1 <= max_result_len) {
                memcpy(&result[result_len], &payload[i + 2], field_len - 1);
                result_len += field_len - 1;
            }
        }
        i += 1 + payload[i];
    }
    
    return result_len;
}

// Decode device name from advertising payload
static inline int decode_name(const uint8_t *payload, int payload_len, char *name, int max_len) {
    return decode_field(payload, payload_len, ADV_TYPE_NAME, (uint8_t *)name, max_len);
}

#endif // BLE_ADVERTISING_H
