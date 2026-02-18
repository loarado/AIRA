#ifndef BTSTACK_CONFIG_H
#define BTSTACK_CONFIG_H

// Port configuration
#define WANT_AD_HOC_CRYPTO_CURVES
#define BTSTACK_LINK_KEY_DB btstack_link_key_db_fs

// Bluetooth Controller / HCI configuration
#define HCI_TRANSPORT HCI_TRANSPORT_H4
#define HCI_CMD_DEFAULT_TIMEOUT_MS 1000

// Bluetooth Core Spec version
#define BLUETOOTH_SPEC_VERSION BLUETOOTH_SPEC_VERSION_5_0

// BTstack features
#define ENABLE_BLE
#define ENABLE_LE_CENTRAL
#define ENABLE_LE_PERIPHERAL
#define ENABLE_LE_EXTENDED_ADVERTISING
#define ENABLE_LE_DATA_LENGTH_EXTENSION
#define ENABLE_LE_2M_PHY
#define ENABLE_LE_CODED_PHY

// L2CAP configuration
#define L2CAP_DYNAMIC_CHANNEL_SUPPORT 0
#define L2CAP_MAX_LE_INITIAL_CHANNELS_DEFAULT 1
#define L2CAP_NUM_FIXED_CHANNELS 3
#define L2CAP_NUM_SERVICES 0
#define L2CAP_NUM_CHANNELS 1

// GATT configuration
#define ENABLE_GATT_SERVICE_GENERIC_ACCESS 0
#define ENABLE_GATT_SERVICE_GENERIC_ATTRIBUTE 0
#define GATT_MAX_SERVICES 0
#define GATT_MAX_CHARACTERISTICS 0
#define GATT_MAX_DESCRIPTORS 0
#define GATT_CLIENT_MAX_SUBSCRIPTIONS 0

// SDP configuration
#define ENABLE_SDP 0

// ATT configuration
#define ATT_DB_UTIL_REMOVE_CONST 1

// SM configuration
#define ENABLE_SM 0

// Security configuration
#define GAP_SECURITY_DB_DEFAULT 1

// NVM configuration (for storing persistent data)
#define NVM_NUM_DEVICE_DB_ENTRIES 1
#define NVM_NUM_LINK_KEY_DB_ENTRIES 1
#define NVM_NUM_LINK_KEYS 1

// Memory pool configuration
#define HCI_ACL_PAYLOAD_SIZE 251

// Logging
#define BTSTACK_PRINTF_HEXDUMP printf
#define BTSTACK_PRINT_ON_INFO(...)
#define BTSTACK_PRINT_ON_DEBUG(...)
#define BTSTACK_PRINT_ON_ERROR(...)

#endif
