# Echo API Reference

Complete reference for all Echo API functions. See [EchoAIOInterface.h](../EchoAIOInterface.h) for the authoritative C/C++ header.

## Library Management

### AIO_initialize

Initialize the API library. Must be called before any other API functions.

```c
void AIO_initialize();
```

### AIO_shutdown

Shutdown the API library. Should be called before program exit to release resources.

```c
void AIO_shutdown();
```

### AIO_getLibraryVersion

Get the library version string.

```c
void AIO_getLibraryVersion(char* text, size_t textBufferBytes);
```

**Parameters:**
- `text` - Buffer to receive the version string
- `textBufferBytes` - Size of the buffer in bytes

### AIO_getErrorString

Get a human-readable error message for the most recent error.

```c
void AIO_getErrorString(char* text, size_t textBufferBytes);
```

**Parameters:**
- `text` - Buffer to receive the error string
- `textBufferBytes` - Size of the buffer in bytes

---

## Device Inquiry

### AIO_isAIOConnected

Check if an Echo AIO device is connected.

```c
int AIO_isAIOConnected();
```

**Returns:** Non-zero if an AIO device is connected, zero otherwise.

### AIO_isATSConnected

Check if an Echo ATS device is connected.

```c
int AIO_isATSConnected();
```

**Returns:** Non-zero if an ATS device is connected, zero otherwise.

### AIO_getNumInputChannels

Get the total number of input channels.

```c
int AIO_getNumInputChannels();
```

**Returns:** Number of input channels.

### AIO_getNumOutputChannels

Get the total number of output channels.

```c
int AIO_getNumOutputChannels();
```

**Returns:** Number of output channels.

### AIO_getModuleType

Get the module type installed in a slot (AIO only).

```c
int AIO_getModuleType(int moduleSlot);
```

**Parameters:**
- `moduleSlot` - 0 for center slot, 1 for outer slot

**Returns:** Module type code:
| Value | Module |
|-------|--------|
| -1 | Unknown |
| 0 | None |
| 1 | AIO-A (analog mic) |
| 2 | AIO-S (speaker monitor) |
| 3 | AIO-L (line) |
| 4 | AIO-C (combo) |
| 5 | AIO-H (headphone) |
| 6 | AIO-T (TDM) |
| 7 | AIO-B (Bluetooth) |
| 8 | ATS analog |
| 9 | ATS digital |

### AIO_hasComboModule

Check if a slot has an AIO-C (combo) module.

```c
int AIO_hasComboModule(int moduleSlot);
```

### AIO_hasTModule

Check if a slot has an AIO-T (TDM) module.

```c
int AIO_hasTModule(int moduleSlot);
```

### AIO_hasBluetoothModule

Check if a slot has an AIO-B (Bluetooth) module.

```c
int AIO_hasBluetoothModule(int moduleSlot);
```

---

## Input Channel Control

### AIO_hasInputGainControl

Check if an input channel has gain control.

```c
int AIO_hasInputGainControl(int inputChannel);
```

**Returns:** Non-zero if channel has gain control.

### AIO_getInputGain

Get the current gain for an input channel.

```c
int AIO_getInputGain(int inputChannel, int* gain);
```

**Parameters:**
- `inputChannel` - Channel number (0-based)
- `gain` - Pointer to receive gain value

**Returns:** `ECHO_AIO_OK` on success, negative error code on failure.

**Gain Values:**
- AIO: 1, 10, or 100 (multiplier)
- ATS: 1, 3, 10, 31, or 100 (multiplier)

### AIO_setInputGain

Set the gain for an input channel.

```c
int AIO_setInputGain(int inputChannel, int gain);
```

**Parameters:**
- `inputChannel` - Channel number (0-based)
- `gain` - Gain value

**Returns:** `ECHO_AIO_OK` on success.

### AIO_setInputGainDirect

Set the input gain using direct multiplier values. Recommended for ATS devices.

```c
int AIO_setInputGainDirect(int inputChannel, int gain);
```

**Parameters:**
- `inputChannel` - Channel number (0-based)
- `gain` - Gain multiplier (ATS: 1/3/10/31/100, AIO: 1/10/100)

**Returns:** `ECHO_AIO_OK` on success, `ECHO_AIO_INVALID_VALUE` for invalid gain.

### AIO_hasConstantCurrentControl

Check if an input channel has constant current power (CCP/IEPE) control.

```c
int AIO_hasConstantCurrentControl(int inputChannel);
```

### AIO_getConstantCurrentState

Get the CCP state for an input channel.

```c
int AIO_getConstantCurrentState(int inputChannel, int* enabled);
```

**Parameters:**
- `inputChannel` - Channel number (0-based)
- `enabled` - Pointer to receive state (0=disabled, 1=enabled)

### AIO_setConstantCurrentState

Set the CCP state for an input channel.

```c
int AIO_setConstantCurrentState(int inputChannel, int enabled);
```

**Parameters:**
- `inputChannel` - Channel number (0-based)
- `enabled` - 0 to disable, 1 to enable

### AIO_hasTEDS

Check if an input channel supports TEDS.

```c
int AIO_hasTEDS(int inputChannel);
```

### AIO_getTEDSProperties

Read TEDS data from a microphone and return as JSON.

```c
int AIO_getTEDSProperties(int inputChannel, char* jsonText,
                          size_t jsonBufferBytes, size_t* jsonBytesRequired);
```

**Parameters:**
- `inputChannel` - Channel number (0-based)
- `jsonText` - Buffer for JSON output (can be NULL)
- `jsonBufferBytes` - Buffer size
- `jsonBytesRequired` - Receives required buffer size

---

## Output Channel Control

### AIO_hasOutputGainControl

Check if an output channel has gain control.

```c
int AIO_hasOutputGainControl(int outputChannel);
```

### AIO_getOutputGain

Get the gain for an output channel.

```c
int AIO_getOutputGain(int outputChannel, int* gain);
```

**Parameters:**
- `outputChannel` - Channel number (0-based)
- `gain` - Pointer to receive gain value (0-255)

### AIO_setOutputGain

Set the gain for an output channel.

```c
int AIO_setOutputGain(int outputChannel, int gain);
```

**Parameters:**
- `outputChannel` - Channel number (0-based)
- `gain` - Gain value (0-255)

---

## Channel Parameters

### AIO_getInputChannelIntParameter

Get an integer parameter for an input channel.

```c
int AIO_getInputChannelIntParameter(int inputChannel, int parameter, int* value);
```

### AIO_setInputChannelIntParameter

Set an integer parameter for an input channel.

```c
int AIO_setInputChannelIntParameter(int inputChannel, int parameter, int value);
```

### AIO_getOutputChannelIntParameter

Get an integer parameter for an output channel.

```c
int AIO_getOutputChannelIntParameter(int moduleSlot, int outputChannel,
                                      int parameter, int* value);
```

### AIO_setOutputChannelIntParameter

Set an integer parameter for an output channel.

```c
int AIO_setOutputChannelIntParameter(int moduleSlot, int outputChannel,
                                      int parameter, int value);
```

---

## Module Parameters

### AIO_getModuleIntParameter

Get an integer parameter for a module.

```c
int AIO_getModuleIntParameter(int moduleSlot, int parameter, int* value);
```

### AIO_setModuleIntParameter

Set an integer parameter for a module.

```c
int AIO_setModuleIntParameter(int moduleSlot, int parameter, int value);
```

### AIO_getModuleDoubleParameter

Get a floating-point parameter for a module.

```c
int AIO_getModuleDoubleParameter(int moduleSlot, int parameter, double* value);
```

### AIO_setModuleDoubleParameter

Set a floating-point parameter for a module.

```c
int AIO_setModuleDoubleParameter(int moduleSlot, int parameter, double value);
```

### AIO_updateTDM

Apply TDM module parameter changes to hardware.

```c
int AIO_updateTDM(int moduleSlot);
```

---

## Device Parameters

### AIO_getDeviceIntParameter

Get an integer device-level parameter.

```c
int AIO_getDeviceIntParameter(int parameter, int* value);
```

### AIO_setDeviceIntParameter

Set an integer device-level parameter.

```c
int AIO_setDeviceIntParameter(int parameter, int value);
```

**Clock Source Parameter (0xd000):**
| Value | Source |
|-------|--------|
| 0 | Internal |
| 1 | USB |
| 2 | Center module |
| 3 | Outer module |

---

## Windows Audio (Windows Only)

### AIO_getASIOPreferredBufferSize

Get the ASIO preferred buffer size.

```c
int AIO_getASIOPreferredBufferSize();
```

**Returns:** Buffer size in samples.

### AIO_setASIOPreferredBufferSize

Set the ASIO preferred buffer size.

```c
int AIO_setASIOPreferredBufferSize(int bufferSize);
```

### AIO_getSampleRate

Get the current sample rate.

```c
int AIO_getSampleRate();
```

**Returns:** Sample rate in Hz.

### AIO_setSampleRate

Set the sample rate.

```c
int AIO_setSampleRate(int sampleRate);
```

### AIO_isWASAPIEnabled

Check if WASAPI support is enabled.

```c
int AIO_isWASAPIEnabled();
```

### AIO_setWASAPIEnabled

Enable or disable WASAPI support.

```c
int AIO_setWASAPIEnabled(int enabled);
```

---

## ATS-Specific Functions

These functions are only available when an ATS device is connected.

### ATS_getSerialNumber

Get the ATS device serial number.

```c
int ATS_getSerialNumber(unsigned int* serialNumber);
```

### ATS_writeI2C

Write data via I2C.

```c
int ATS_writeI2C(int sdaSelect, int i2cAddress, int registerAddress,
                 int registerLength, unsigned char* data);
```

### ATS_readI2C

Read data via I2C.

```c
int ATS_readI2C(int sdaSelect, int i2cAddress, int registerAddress,
                int registerLength, unsigned char* data);
```

### ATS_getAuxOut / ATS_setAuxOut

Get or set the AUX output state (4-bit bitmask).

```c
int ATS_getAuxOut(unsigned char* bits);
int ATS_setAuxOut(unsigned char bits);
```

### ATS_getAuxIn

Read the AUX input state.

```c
int ATS_getAuxIn(unsigned char* bits);
```

### ATS_getDigitalIOMode / ATS_setDigitalIOMode

Get or set the digital I/O mode (0=S/PDIF, 1=Word Clock).

```c
int ATS_getDigitalIOMode(unsigned char* mode);
int ATS_setDigitalIOMode(unsigned char mode);
```

### ATS_getWordClockTerminated / ATS_setWordClockTerminated

Get or set word clock termination state.

```c
int ATS_getWordClockTerminated(int* terminated);
int ATS_setWordClockTerminated(int terminated);
```

### ATS_getImpedanceMode / ATS_setImpedanceMode

Get or set impedance measurement mode.

```c
int ATS_getImpedanceMode(int* enabled);
int ATS_setImpedanceMode(int enabled);
```

### ATS_getAnalogInputMode / ATS_setAnalogInputMode

Get or set analog input mode (0=Loopback, 1=Analog).

```c
int ATS_getAnalogInputMode(int channel, int* mode);
int ATS_setAnalogInputMode(int channel, int mode);
```

**Parameters:**
- `channel` - Input channel (0-7)
- `mode` - 0=Loopback (output to input), 1=Analog connector

### ATS_getAnalogOutputMode / ATS_setAnalogOutputMode

Get or set analog output mode.

```c
int ATS_getAnalogOutputMode(int channel, int* mode);
int ATS_setAnalogOutputMode(int channel, int mode);
```

**Parameters:**
- `channel` - Output channel (0-3)
- `mode` - 0=Line, 1=Amplifier, 2=Headphone

---

## Error Codes

| Code | Constant | Description |
|------|----------|-------------|
| 0 | ECHO_AIO_OK | Success |
| -1 | ECHO_AIO_NOT_INITIALIZED | Library not initialized |
| -2 | ECHO_AIO_INVALID_INPUT_CHANNEL | Invalid input channel |
| -3 | ECHO_AIO_INVALID_OUTPUT_CHANNEL | Invalid output channel |
| -4 | ECHO_AIO_INVALID_PARAMETER | Invalid parameter ID |
| -5 | ECHO_AIO_INVALID_BUFFER_SIZE | Buffer too small |
| -6 | ECHO_AIO_NOT_FOUND | Resource not found |
| -7 | ECHO_AIO_USB_COMMAND_FAILED | USB error |
| -8 | ECHO_AIO_INVALID_MODULE_SLOT | Invalid slot (0 or 1) |
| -9 | ECHO_AIO_NOT_SUPPORTED | Feature not supported |
| -10 | ECHO_AIO_TEDS_DEVICE_NOT_FOUND | No TEDS microphone |
| -11 | ECHO_AIO_INVALID_VALUE | Value out of range |
| -12 | ECHO_AIO_MISSING_PARAMETER | Required param missing |
| -13 | ECHO_AIO_TIMEOUT | Operation timed out |
| -14 | ECHO_AIO_INVALID_POINTER | Null pointer |

---

## Module Parameter Constants

### AIO-C Combo Module

| Constant | Value | Description |
|----------|-------|-------------|
| AIO_COMBO_MODULE_PARAMETER_FIRMWARE_VERSION | 0xc0000 | Read-only firmware version |
| AIO_COMBO_MODULE_PARAMETER_SERIAL_NUMBER | 0xc0001 | Read-only serial number |
| AIO_COMBO_MODULE_PARAMETER_AUX_OUT | 0xc0002 | AUX output pin state |
| AIO_COMBO_MODULE_PARAMETER_AUX_IN | 0xc0003 | Read-only AUX input state |
| AIO_COMBO_MODULE_PARAMETER_5VDC_ENABLE | 0xc0004 | 5V power supply enable |
| AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_ENABLE | 0xc0005 | Variable power enable |
| AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_TARGET_MILLIVOLTS | 0xc0006 | Target voltage (600-5000 mV) |
| AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_MILLIVOLTS | 0xc0007 | Read-only measured voltage |
| AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_CURRENT | 0xc0008 | Read-only measured current (double) |
| AIO_COMBO_MODULE_PARAMETER_MEASURED_CURRENT_RANGE | 0xc0009 | Current measurement range |
| AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_THRESHOLD | 0xc000a | Over-current threshold (double) |
| AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_CONDITION | 0xc000b | Over-current status |

### AIO-T TDM Module

| Constant | Value | Description |
|----------|-------|-------------|
| AIO_T_MODULE_PARAMETER_FIRMWARE_VERSION | 0xd000 | Read-only firmware version |
| AIO_T_MODULE_PARAMETER_BITS_PER_WORD | 0xd001 | Bits per word (01=24, 10=32) |
| AIO_T_MODULE_PARAMETER_BITS_PER_FRAME | 0xd002 | Bits per frame |
| AIO_T_MODULE_PARAMETER_FSYNC_PHASE_DELAY | 0xd003 | FSYNC phase delay |
| AIO_T_MODULE_PARAMETER_INVERT_SCLK | 0xd004 | Invert SCLK signal |
| AIO_T_MODULE_PARAMETER_SHIFT_ENABLED | 0xd005 | Enable shift |
| AIO_T_MODULE_PARAMETER_CLOCK_SINK | 0xd006 | Clock sink mode |
| AIO_T_MODULE_PARAMETER_AUDIO_DATA_SHIFT_BITS | 0xd007 | Shift bits (0-7) |
| AIO_T_MODULE_PARAMETER_LOGIC_LEVEL | 0xd008 | Logic level |
| AIO_T_MODULE_PARAMETER_FSYNC_POSITION | 0xd009 | FSYNC start position |
| AIO_T_MODULE_PARAMETER_FSYNC_WIDTH | 0xd00a | FSYNC width |
