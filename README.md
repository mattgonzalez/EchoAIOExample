# Echo API Library

The Echo API Library provides programmatic control of Echo Digital Audio test interfaces, including the **Echo AIO** and **Echo ATS** devices.

## Supported Devices

### Echo AIO
A modular audio test interface with interchangeable audio modules:
- **AIO-A** - Analog microphone inputs with IEPE/CCP support
- **AIO-S** - Speaker monitor inputs
- **AIO-L** - Line level inputs/outputs
- **AIO-C** - Combo module with programmable power supply and GPIO
- **AIO-H** - Headphone amplifier outputs
- **AIO-T** - TDM digital audio interface
- **AIO-B** - Bluetooth audio module

### Echo ATS
A precision audio test system with:
- 8 analog inputs with selectable gain (1x, 3x, 10x, 31x, 100x)
- 4 analog outputs with configurable modes (Line, Amplifier, Headphone)
- S/PDIF or Word Clock digital I/O
- 4-bit AUX GPIO
- Impedance measurement mode
- I2C passthrough

## Installation

The Echo API Library is installed as part of the Echo Control Panel application.

**Default installation path:**
- Windows: `C:\Program Files\Echo Test Interfaces\EchoAPI.dll`
- macOS: `/Library/Application Support/Echo Test Interfaces/libEchoAPI.dylib`

## Quick Start

### C/C++

```c
#include "EchoAIOInterface.h"

int main()
{
    // Initialize the library
    AIO_initialize();

    // Check for connected devices
    if (AIO_isATSConnected())
    {
        printf("ATS connected\n");

        // Set input gain to 10x on channel 0
        AIO_setInputGainDirect(0, 10);

        // Enable CCP (constant current power) for IEPE microphones
        AIO_setConstantCurrentState(0, 1);
    }
    else if (AIO_isAIOConnected())
    {
        printf("AIO connected\n");

        // Get device info
        int numInputs = AIO_getNumInputChannels();
        int numOutputs = AIO_getNumOutputChannels();
        printf("Inputs: %d, Outputs: %d\n", numInputs, numOutputs);
    }

    // Shutdown
    AIO_shutdown();
    return 0;
}
```

### Python

```python
from echo_api import EchoAPI

# Initialize and use context manager for automatic cleanup
api = EchoAPI()
api.initialize()

try:
    if api.is_ats_connected():
        print("ATS connected")

        # Set input gain to 10x
        api.set_input_gain_direct(0, 10)

        # Get serial number
        serial = api.ats_get_serial_number()
        print(f"Serial: {serial}")

    elif api.is_aio_connected():
        print("AIO connected")
        info = api.get_device_info()
        print(f"Inputs: {info.num_inputs}, Outputs: {info.num_outputs}")

finally:
    api.shutdown()
```

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting-started.md) | Installation and first steps |
| [API Reference](docs/api-reference.md) | Complete function reference |
| [AIO Guide](docs/aio-guide.md) | Echo AIO device guide |
| [ATS Guide](docs/ats-guide.md) | Echo ATS device guide |
| [EchoAIOInterface.h](EchoAIOInterface.h) | C/C++ header with API documentation |

## Repository Contents

```
EchoAIOExample/
├── README.md                    # This file
├── EchoAIOInterface.h           # C/C++ API header (authoritative reference)
├── docs/
│   ├── getting-started.md       # Installation and first steps
│   ├── api-reference.md         # Complete API reference
│   ├── aio-guide.md             # AIO-specific documentation
│   └── ats-guide.md             # ATS-specific documentation
├── C++/
│   ├── Windows/                 # Windows C++ examples
│   └── macOS/                   # macOS C++ examples
├── Python/
│   ├── echo_api.py              # Python wrapper
│   ├── examples/                # Python examples
│   └── README.md                # Python setup guide
└── Matlab/
    └── EchoAIO.mltbx            # MATLAB toolbox
```

## Supported Platforms

| Platform | Architecture | Library |
|----------|--------------|---------|
| Windows 10/11 | x64 | EchoAPI.dll |
| macOS 12+ | Intel/Apple Silicon | libEchoAPI.dylib |

## Error Codes

All API functions that can fail return an integer result code:

| Code | Name | Description |
|------|------|-------------|
| 0 | ECHO_AIO_OK | Success |
| -1 | ECHO_AIO_NOT_INITIALIZED | Library not initialized |
| -2 | ECHO_AIO_INVALID_INPUT_CHANNEL | Invalid input channel number |
| -3 | ECHO_AIO_INVALID_OUTPUT_CHANNEL | Invalid output channel number |
| -4 | ECHO_AIO_INVALID_PARAMETER | Invalid parameter ID |
| -5 | ECHO_AIO_INVALID_BUFFER_SIZE | Buffer too small |
| -6 | ECHO_AIO_NOT_FOUND | Device or resource not found |
| -7 | ECHO_AIO_USB_COMMAND_FAILED | USB communication error |
| -8 | ECHO_AIO_INVALID_MODULE_SLOT | Invalid module slot (must be 0 or 1) |
| -9 | ECHO_AIO_NOT_SUPPORTED | Feature not supported by device |
| -10 | ECHO_AIO_TEDS_DEVICE_NOT_FOUND | TEDS microphone not detected |
| -11 | ECHO_AIO_INVALID_VALUE | Value out of valid range |
| -12 | ECHO_AIO_MISSING_PARAMETER | Required parameter not provided |
| -13 | ECHO_AIO_TIMEOUT | Operation timed out |
| -14 | ECHO_AIO_INVALID_POINTER | Null pointer passed |

Use `AIO_getErrorString()` to get a human-readable error message.

## Support

For more information about Echo test interfaces, visit [https://echotm.com/](https://echotm.com/)

## License

Copyright (c) 2022-2025 Echo Digital Audio Corporation. All rights reserved.
