# Getting Started with the Echo API

This guide walks you through installing the Echo API Library and writing your first program to control an Echo AIO or ATS device.

## Prerequisites

- **Windows**: Windows 10 or later (x64)
- **macOS**: macOS 12 (Monterey) or later (Intel or Apple Silicon)
- Echo AIO or Echo ATS device connected via USB
- Echo Control Panel application installed

## Installation

The Echo API Library is automatically installed with the Echo Control Panel application.

### Windows

1. Download and install the Echo Control Panel from [echotm.com](https://echotm.com/)
2. The library is installed to: `C:\Program Files\Echo Test Interfaces\EchoAPI.dll`
3. Copy `EchoAIOInterface.h` from this repository to your project

### macOS

1. Download the Echo Control Panel DMG from [echotm.com](https://echotm.com/)
2. Mount the DMG and copy `libEchoAPI.dylib` to your project directory
3. Copy `EchoAIOInterface.h` from this repository to your project

## Verifying Your Installation

### Check Device Connection

Before writing code, verify your device is recognized:

1. Connect your Echo AIO or ATS via USB
2. Open the Echo Control Panel application
3. Verify the device appears and is controllable

### Library Location

Verify the library exists at the expected path:

**Windows (PowerShell):**
```powershell
Test-Path "C:\Program Files\Echo Test Interfaces\EchoAPI.dll"
```

**macOS (Terminal):**
```bash
ls -la ./libEchoAPI.dylib
```

## Your First Program

### C++ (Windows)

Create a new C++ project and add this code:

```cpp
#include <stdio.h>
#include <windows.h>

// Include the API header
#include "EchoAIOInterface.h"

// Function pointer types
typedef void (*AIO_initialize_t)();
typedef void (*AIO_shutdown_t)();
typedef void (*AIO_getLibraryVersion_t)(char*, size_t);
typedef int (*AIO_isAIOConnected_t)();
typedef int (*AIO_isATSConnected_t)();
typedef int (*AIO_getNumInputChannels_t)();
typedef int (*AIO_getNumOutputChannels_t)();

int main()
{
    // Load the DLL
    HMODULE dll = LoadLibraryA("C:\\Program Files\\Echo Test Interfaces\\EchoAPI.dll");
    if (!dll)
    {
        printf("Failed to load EchoAPI.dll\n");
        return 1;
    }

    // Get function pointers
    auto AIO_initialize = (AIO_initialize_t)GetProcAddress(dll, "AIO_initialize");
    auto AIO_shutdown = (AIO_shutdown_t)GetProcAddress(dll, "AIO_shutdown");
    auto AIO_getLibraryVersion = (AIO_getLibraryVersion_t)GetProcAddress(dll, "AIO_getLibraryVersion");
    auto AIO_isAIOConnected = (AIO_isAIOConnected_t)GetProcAddress(dll, "AIO_isAIOConnected");
    auto AIO_isATSConnected = (AIO_isATSConnected_t)GetProcAddress(dll, "AIO_isATSConnected");
    auto AIO_getNumInputChannels = (AIO_getNumInputChannels_t)GetProcAddress(dll, "AIO_getNumInputChannels");
    auto AIO_getNumOutputChannels = (AIO_getNumOutputChannels_t)GetProcAddress(dll, "AIO_getNumOutputChannels");

    // Initialize the library
    AIO_initialize();

    // Get library version
    char version[256];
    AIO_getLibraryVersion(version, sizeof(version));
    printf("Echo API Library version: %s\n", version);

    // Check for connected devices
    if (AIO_isATSConnected())
    {
        printf("Echo ATS connected!\n");
    }
    else if (AIO_isAIOConnected())
    {
        printf("Echo AIO connected!\n");
    }
    else
    {
        printf("No device connected\n");
        AIO_shutdown();
        FreeLibrary(dll);
        return 1;
    }

    // Get channel counts
    int numInputs = AIO_getNumInputChannels();
    int numOutputs = AIO_getNumOutputChannels();
    printf("Input channels: %d\n", numInputs);
    printf("Output channels: %d\n", numOutputs);

    // Cleanup
    AIO_shutdown();
    FreeLibrary(dll);

    return 0;
}
```

### Python

Python provides a simpler approach using ctypes. See the [Python README](../Python/README.md) for the complete wrapper.

Quick example:

```python
import ctypes
from pathlib import Path

# Load the DLL
dll_path = Path("C:/Program Files/Echo Test Interfaces/EchoAPI.dll")
dll = ctypes.WinDLL(str(dll_path))

# Initialize
dll.AIO_initialize()

# Check for device
if dll.AIO_isATSConnected():
    print("ATS connected")
elif dll.AIO_isAIOConnected():
    print("AIO connected")
else:
    print("No device")

# Get version
buffer = ctypes.create_string_buffer(256)
dll.AIO_getLibraryVersion(buffer, len(buffer))
print(f"Version: {buffer.value.decode()}")

# Cleanup
dll.AIO_shutdown()
```

## Basic API Pattern

All Echo API programs follow this pattern:

1. **Load the library** - Load the DLL/dylib
2. **Initialize** - Call `AIO_initialize()` before any other functions
3. **Check device** - Use `AIO_isAIOConnected()` or `AIO_isATSConnected()`
4. **Configure and control** - Set gains, enable CCP, read TEDS, etc.
5. **Shutdown** - Call `AIO_shutdown()` before unloading

## Error Handling

Most API functions return an integer result code:

- `0` (ECHO_AIO_OK) indicates success
- Negative values indicate errors

Always check return values and use `AIO_getErrorString()` for details:

```cpp
int result = AIO_setInputGain(0, 10);
if (result != ECHO_AIO_OK)
{
    char errorMsg[256];
    AIO_getErrorString(errorMsg, sizeof(errorMsg));
    printf("Error: %s\n", errorMsg);
}
```

## Next Steps

- [API Reference](api-reference.md) - Complete function documentation
- [AIO Guide](aio-guide.md) - Echo AIO-specific features
- [ATS Guide](ats-guide.md) - Echo ATS-specific features
- [Python Examples](../Python/examples/) - Python code examples
