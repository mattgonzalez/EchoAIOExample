'''
  ==============================================================================

    EchoAIOInterface library exports for Bluetooth module

    Copyright (c) 2023 - Echo Digital Audio Corporation

  ==============================================================================
'''

import ctypes

#
# AIO Bluetooth Module Return Values
#
class AIOBluetoothReturnValue(ctypes.c_int):
    AIO_invalidAddress = 0xb00
    AIO_radioNotPresent = 0xb01
    AIO_connectionError = 0xb02
    AIO_radioError = 0xb03

#
# AIO Bluetooth Constrants
#
class AIOBluetoothModuleLocalDevices(ctypes.c_int):
    AIO_bluetoothDeviceModule = 0xb0
    AIO_bluetoothDeviceRadio1 = 0xb1
    AIO_bluetoothDeviceRadio2 = 0xb2
    AIO_numBluetoothRadiosPerModule = 2

class AIOBluetoothModuleCommands(ctypes.c_int):
    AIO_bluetoothGetFirmwareVersionCommand = 0xb000
    AIO_bluetoothGetInfoCommand = 0xb001
    AIO_bluetoothWriteStringCommand = 0xb002
    AIO_bluetoothReadStringCommand = 0xb003

class AIOBluetoothA2DPStates(ctypes.c_int):
    AIO_BLUETOOTH_A2DP_DISCONNECTED = 0
    AIO_BLUETOOTH_A2DP_SUSPENDED = 1
    AIO_BLUETOOTH_A2DP_STREAMING = 2

class AIOBluetoothAVRCPStates(ctypes.c_int):
    AIO_BLUETOOTH_AVRCP_DISCONNECTED = 0
    AIO_BLUETOOTH_AVRCP_STOPPED = 1
    AIO_BLUETOOTH_AVRCP_PLAYING = 2

class AIOBluetoothHFPStates(ctypes.c_int):
    AIO_BLUETOOTH_HFP_DISCONNECTED = 0
    AIO_BLUETOOTH_HFP_IDLE = 1
    AIO_BLUETOOTH_HFP_INCOMING = 2
    AIO_BLUETOOTH_HFP_ACTIVE = 3

#
# JSON Property Names
#
AIO_commandProperty = "Command"
AIO_responseProperty = "Response"
AIO_moduleSlotProperty = "ModuleSlot"
AIO_localDeviceProperty = "LocalDevice"
AIO_writeStringProperty = "WriteString"
AIO_readStringProperty = "ReadString"