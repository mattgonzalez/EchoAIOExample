# Echo ATS Device Guide

The Echo ATS is a precision audio test system designed for automated testing of audio devices. This guide covers ATS-specific features and API functions.

## Device Overview

### Channels

| Type | Count | Description |
|------|-------|-------------|
| Analog Inputs | 8 | Channels 0-7, with selectable gain and input mode |
| Analog Outputs | 4 | Channels 0-3, with configurable output mode |
| Digital I/O | 2 | S/PDIF or Word Clock (channels 8-9 input, 4-5 output) |

### Features

- Selectable input gain (1x, 3x, 10x, 31x, 100x)
- IEPE/CCP constant current power for microphones
- TEDS microphone identification
- Configurable analog input mode (Loopback or External)
- Configurable analog output mode (Line, Amplifier, Headphone)
- S/PDIF or Word Clock digital I/O
- 4-bit AUX GPIO
- Impedance measurement mode
- I2C passthrough for custom hardware

## Detecting an ATS Device

```c
AIO_initialize();

if (AIO_isATSConnected())
{
    printf("ATS device found\n");

    // Get serial number
    unsigned int serial;
    ATS_getSerialNumber(&serial);
    printf("Serial number: %u\n", serial);
}
```

## Input Gain Control

The ATS supports 5 gain multipliers for the analog inputs:

| Multiplier | Approximate dB |
|------------|---------------|
| 1x | 0 dB |
| 3x | 10 dB |
| 10x | 20 dB |
| 31x | 30 dB |
| 100x | 40 dB |

### Setting Input Gain

Use `AIO_setInputGainDirect()` to set the gain multiplier directly:

```c
// Set channel 0 to 10x gain
int result = AIO_setInputGainDirect(0, 10);
if (result != ECHO_AIO_OK)
{
    // Handle error
}

// Read back current gain
int gain;
result = AIO_getInputGain(0, &gain);
printf("Channel 0 gain: %dx\n", gain);  // Prints: Channel 0 gain: 10x
```

### Valid Gain Values

Only these exact multiplier values are accepted:
- `1` - Unity gain (0 dB)
- `3` - ~10 dB gain
- `10` - 20 dB gain
- `31` - ~30 dB gain
- `100` - 40 dB gain

Any other value will return `ECHO_AIO_INVALID_VALUE`.

## Constant Current Power (CCP/IEPE)

Enable constant current power for IEPE microphones:

```c
// Check if channel supports CCP
if (AIO_hasConstantCurrentControl(0))
{
    // Enable CCP on channel 0
    AIO_setConstantCurrentState(0, 1);

    // Verify state
    int enabled;
    AIO_getConstantCurrentState(0, &enabled);
    printf("CCP enabled: %s\n", enabled ? "yes" : "no");
}
```

## Analog Input Mode

Each analog input can be configured for external input or loopback:

| Mode | Value | Description |
|------|-------|-------------|
| Loopback | 0 | Routes corresponding output to input (for self-test) |
| Analog Input | 1 | Uses the external input connector |

```c
// Set channel 0 to use external analog input
ATS_setAnalogInputMode(0, 1);

// Get current mode
int mode;
ATS_getAnalogInputMode(0, &mode);
printf("Input mode: %s\n", mode == 0 ? "Loopback" : "Analog");
```

## Analog Output Mode

Each analog output supports three modes:

| Mode | Value | Description |
|------|-------|-------------|
| Line Level | 0 | Standard line-level output |
| Amplifier | 1 | Higher power output for driving speakers |
| Headphone | 2 | Optimized for headphone loads |

```c
// Set channel 0 to headphone mode
ATS_setAnalogOutputMode(0, 2);

// Get current mode
int mode;
ATS_getAnalogOutputMode(0, &mode);
const char* modeNames[] = {"Line", "Amplifier", "Headphone"};
printf("Output mode: %s\n", modeNames[mode]);
```

## Digital I/O Configuration

The digital I/O port can operate in S/PDIF or Word Clock mode:

| Mode | Value | Description |
|------|-------|-------------|
| S/PDIF | 0 | Standard S/PDIF digital audio |
| Word Clock | 1 | Word clock sync signal |

```c
// Set to word clock mode
ATS_setDigitalIOMode(1);

// Get current mode
unsigned char mode;
ATS_getDigitalIOMode(&mode);
printf("Digital mode: %s\n", mode == 0 ? "S/PDIF" : "Word Clock");
```

### Word Clock Termination

When using word clock mode, you can enable 75-ohm termination:

```c
// Enable word clock termination
ATS_setWordClockTerminated(1);

// Check termination state
int terminated;
ATS_getWordClockTerminated(&terminated);
printf("Termination: %s\n", terminated ? "enabled" : "disabled");
```

## AUX GPIO

The ATS provides 4 general-purpose digital I/O pins:

```c
// Set AUX output bits (4-bit value, 0-15)
ATS_setAuxOut(0x05);  // Set bits 0 and 2 high

// Read AUX output state
unsigned char out_bits;
ATS_getAuxOut(&out_bits);
printf("AUX out: 0x%X\n", out_bits);

// Read AUX input state
unsigned char in_bits;
ATS_getAuxIn(&in_bits);
printf("AUX in: 0x%X\n", in_bits);
```

## Impedance Measurement Mode

Enable impedance measurement mode for speaker impedance testing:

```c
// Enable impedance mode
ATS_setImpedanceMode(1);

// Check mode
int enabled;
ATS_getImpedanceMode(&enabled);
printf("Impedance mode: %s\n", enabled ? "enabled" : "disabled");

// Disable when done
ATS_setImpedanceMode(0);
```

## I2C Passthrough

The ATS provides I2C passthrough for communicating with custom hardware:

```c
// Write to I2C device
unsigned char data = 0x42;
int result = ATS_writeI2C(
    0,          // SDA select
    0x50,       // I2C address
    0x00,       // Register address
    1,          // Register address length (bytes)
    &data       // Data to write
);

// Read from I2C device
unsigned char readData;
result = ATS_readI2C(
    0,          // SDA select
    0x50,       // I2C address
    0x00,       // Register address
    1,          // Register address length (bytes)
    &readData   // Buffer for read data
);
```

## Serial Number

Get the device serial number:

```c
unsigned int serial;
int result = ATS_getSerialNumber(&serial);
if (result == ECHO_AIO_OK)
{
    printf("ATS Serial Number: %u\n", serial);
}
```

## Complete ATS Example

```c
#include <stdio.h>
#include "EchoAIOInterface.h"

int main()
{
    AIO_initialize();

    if (!AIO_isATSConnected())
    {
        printf("No ATS device found\n");
        AIO_shutdown();
        return 1;
    }

    // Get device info
    unsigned int serial;
    ATS_getSerialNumber(&serial);
    printf("ATS Serial: %u\n", serial);
    printf("Inputs: %d, Outputs: %d\n",
           AIO_getNumInputChannels(),
           AIO_getNumOutputChannels());

    // Configure inputs
    for (int ch = 0; ch < 8; ch++)
    {
        // Set to analog input mode
        ATS_setAnalogInputMode(ch, 1);

        // Set gain to 10x
        AIO_setInputGainDirect(ch, 10);

        // Enable CCP for IEPE microphones
        AIO_setConstantCurrentState(ch, 1);
    }

    // Configure outputs
    for (int ch = 0; ch < 4; ch++)
    {
        // Set to line level mode
        ATS_setAnalogOutputMode(ch, 0);
    }

    // Set digital I/O to S/PDIF mode
    ATS_setDigitalIOMode(0);

    printf("ATS configured successfully\n");

    AIO_shutdown();
    return 0;
}
```

## ATS Function Reference

| Function | Description |
|----------|-------------|
| `ATS_getSerialNumber` | Get device serial number |
| `ATS_writeI2C` | Write data via I2C |
| `ATS_readI2C` | Read data via I2C |
| `ATS_getAuxOut` | Get AUX output state |
| `ATS_setAuxOut` | Set AUX output state |
| `ATS_getAuxIn` | Read AUX input state |
| `ATS_getDigitalIOMode` | Get S/PDIF or Word Clock mode |
| `ATS_setDigitalIOMode` | Set S/PDIF or Word Clock mode |
| `ATS_getWordClockTerminated` | Get termination state |
| `ATS_setWordClockTerminated` | Set termination state |
| `ATS_getImpedanceMode` | Get impedance mode state |
| `ATS_setImpedanceMode` | Enable/disable impedance mode |
| `ATS_getAnalogInputMode` | Get input mode (Loopback/Analog) |
| `ATS_setAnalogInputMode` | Set input mode |
| `ATS_getAnalogOutputMode` | Get output mode (Line/Amp/Headphone) |
| `ATS_setAnalogOutputMode` | Set output mode |

See [API Reference](api-reference.md) for complete function documentation.
