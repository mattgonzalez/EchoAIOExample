# Echo AIO Device Guide

The Echo AIO is a modular audio test interface with interchangeable audio modules. This guide covers AIO-specific features and API usage.

## Device Overview

### Module Slots

The AIO has two module slots:
- **Slot 0 (Center)** - Inner module position
- **Slot 1 (Outer)** - Outer module position

### Module Types

| Type | Name | Description |
|------|------|-------------|
| AIO-A | Analog | IEPE microphone inputs with CCP support |
| AIO-S | Speaker Monitor | High-impedance speaker monitor inputs |
| AIO-L | Line | Balanced line-level inputs and outputs |
| AIO-C | Combo | Programmable power supply, GPIO, and audio |
| AIO-H | Headphone | Headphone amplifier outputs |
| AIO-T | TDM | Digital TDM audio interface |
| AIO-B | Bluetooth | Bluetooth audio connectivity |

## Detecting an AIO Device

```c
AIO_initialize();

if (AIO_isAIOConnected())
{
    printf("AIO device found\n");

    // Check module types
    int slot0 = AIO_getModuleType(0);
    int slot1 = AIO_getModuleType(1);

    const char* moduleNames[] = {
        "None", "AIO-A", "AIO-S", "AIO-L",
        "AIO-C", "AIO-H", "AIO-T", "AIO-B"
    };

    printf("Slot 0: %s\n", moduleNames[slot0]);
    printf("Slot 1: %s\n", moduleNames[slot1]);
}
```

## Input Gain Control

AIO devices with analog input modules (AIO-A, AIO-L) support gain control.

### Gain Values

| Multiplier | Approximate dB |
|------------|---------------|
| 1x | 0 dB |
| 10x | 20 dB |
| 100x | 40 dB |

```c
// Check if channel has gain control
if (AIO_hasInputGainControl(0))
{
    // Set gain to 10x
    AIO_setInputGainDirect(0, 10);

    // Read back
    int gain;
    AIO_getInputGain(0, &gain);
    printf("Gain: %dx\n", gain);
}
```

## Constant Current Power (CCP/IEPE)

IEPE microphones require constant current power. The AIO-A module provides CCP support.

```c
// Check if channel supports CCP
if (AIO_hasConstantCurrentControl(0))
{
    // Enable CCP
    AIO_setConstantCurrentState(0, 1);

    // Verify
    int enabled;
    AIO_getConstantCurrentState(0, &enabled);
    printf("CCP: %s\n", enabled ? "enabled" : "disabled");
}
```

## TEDS Support

TEDS (Transducer Electronic Data Sheet) allows automatic identification of IEPE microphones.

```c
// Check if channel supports TEDS
if (AIO_hasTEDS(0))
{
    // Get required buffer size
    size_t requiredSize;
    AIO_getTEDSProperties(0, NULL, 0, &requiredSize);

    if (requiredSize > 0)
    {
        char* json = malloc(requiredSize + 1);
        AIO_getTEDSProperties(0, json, requiredSize + 1, &requiredSize);
        printf("TEDS data: %s\n", json);
        free(json);
    }
}
```

## Output Gain Control

Some modules (like AIO-H) provide output gain control.

```c
// Check if output has gain control
if (AIO_hasOutputGainControl(0))
{
    // Set output gain (0-255)
    AIO_setOutputGain(0, 200);

    // Read back
    int gain;
    AIO_getOutputGain(0, &gain);
    printf("Output gain: %d\n", gain);
}
```

## AIO-C Combo Module

The AIO-C provides additional features beyond audio:

### Programmable Power Supply

```c
// Enable variable DC power
AIO_setModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_ENABLE, 1);

// Set target voltage (millivolts, 600-5000)
AIO_setModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_TARGET_MILLIVOLTS, 3300);

// Read measured voltage
int measuredMV;
AIO_getModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_MILLIVOLTS, &measuredMV);
printf("Measured: %d mV\n", measuredMV);

// Read measured current
double current;
AIO_getModuleDoubleParameter(0, AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_CURRENT, &current);
printf("Current: %.3f A\n", current);
```

### 5V Power Supply

```c
// Enable 5V supply
AIO_setModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_5VDC_ENABLE, 1);
```

### AUX GPIO

```c
// Set AUX output pins (8-bit)
AIO_setModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_AUX_OUT, 0x55);

// Read AUX input pins
int auxIn;
AIO_getModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_AUX_IN, &auxIn);
printf("AUX in: 0x%02X\n", auxIn);
```

### Current Measurement

```c
// Set current measurement range
// 0 = 0-256 µA
// 1 = 0-1280 µA
// 2 = 0-256 mA
// 3 = 0-1280 mA
AIO_setModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_MEASURED_CURRENT_RANGE, 2);

// Set over-current threshold
AIO_setModuleDoubleParameter(0, AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_THRESHOLD, 0.1);

// Check for over-current condition
int overCurrent;
AIO_getModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_CONDITION, &overCurrent);
if (overCurrent)
{
    printf("Over-current detected!\n");
    // Clear the condition
    AIO_setModuleIntParameter(0, AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_CONDITION, 0);
}
```

## AIO-T TDM Module

The AIO-T provides digital TDM audio connectivity.

### Basic Configuration

```c
// Set bits per word (01=24, 10=32)
AIO_setModuleIntParameter(0, AIO_T_MODULE_PARAMETER_BITS_PER_WORD, 0x02);  // 32-bit

// Set clock sink mode (0=source, 1=sink)
AIO_setModuleIntParameter(0, AIO_T_MODULE_PARAMETER_CLOCK_SINK, 0);  // Clock source

// Apply changes
AIO_updateTDM(0);
```

### Clock Configuration

```c
// Invert SCLK
AIO_setModuleIntParameter(0, AIO_T_MODULE_PARAMETER_INVERT_SCLK, 1);

// Set FSYNC phase delay
AIO_setModuleIntParameter(0, AIO_T_MODULE_PARAMETER_FSYNC_PHASE_DELAY, 0);

// Apply changes
AIO_updateTDM(0);
```

## Clock Source Configuration

Select the device clock source:

```c
// Clock sources:
// 0 = Internal
// 1 = USB
// 2 = Center module (slot 0)
// 3 = Outer module (slot 1)

// Set to internal clock
AIO_setDeviceIntParameter(ECHO_DEVICE_PARAMETER_CLOCK_SOURCE, 0);

// Get current source
int source;
AIO_getDeviceIntParameter(ECHO_DEVICE_PARAMETER_CLOCK_SOURCE, &source);
```

## Windows Audio Configuration

### ASIO Buffer Size

```c
// Get current buffer size
int bufferSize = AIO_getASIOPreferredBufferSize();
printf("Buffer size: %d samples\n", bufferSize);

// Set buffer size
AIO_setASIOPreferredBufferSize(256);
```

### Sample Rate

```c
// Get current sample rate
int sampleRate = AIO_getSampleRate();
printf("Sample rate: %d Hz\n", sampleRate);

// Set sample rate
AIO_setSampleRate(48000);
```

### WASAPI Support

```c
// Check WASAPI status
if (AIO_isWASAPIEnabled())
{
    printf("WASAPI enabled\n");
}

// Enable/disable WASAPI
AIO_setWASAPIEnabled(1);  // Enable
```

## Complete AIO Example

```c
#include <stdio.h>
#include "EchoAIOInterface.h"

int main()
{
    AIO_initialize();

    if (!AIO_isAIOConnected())
    {
        printf("No AIO device found\n");
        AIO_shutdown();
        return 1;
    }

    // Get device info
    int numInputs = AIO_getNumInputChannels();
    int numOutputs = AIO_getNumOutputChannels();
    printf("AIO: %d inputs, %d outputs\n", numInputs, numOutputs);

    // Show module configuration
    int slot0 = AIO_getModuleType(0);
    int slot1 = AIO_getModuleType(1);
    printf("Slot 0: type %d\n", slot0);
    printf("Slot 1: type %d\n", slot1);

    // Configure input channels
    for (int ch = 0; ch < numInputs; ch++)
    {
        if (AIO_hasInputGainControl(ch))
        {
            AIO_setInputGainDirect(ch, 1);  // Unity gain
        }
        if (AIO_hasConstantCurrentControl(ch))
        {
            AIO_setConstantCurrentState(ch, 1);  // Enable CCP
        }
    }

    printf("AIO configured successfully\n");

    AIO_shutdown();
    return 0;
}
```

## Module Parameter Reference

See [API Reference](api-reference.md) for complete parameter constants.
