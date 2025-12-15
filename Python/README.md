# Echo API Python Wrapper

Python wrapper for controlling Echo AIO and ATS devices.

## Requirements

- Python 3.8 or later
- Echo Control Panel installed
- Echo AIO or ATS device connected via USB

## Installation

No additional packages are required - the wrapper uses Python's built-in `ctypes` module.

1. Copy `echo_api.py` to your project
2. Import and use:

```python
from echo_api import EchoAPI, EchoAPIContext
```

## Quick Start

### Using Context Manager (Recommended)

```python
from echo_api import EchoAPIContext

with EchoAPIContext() as api:
    if api.is_ats_connected():
        print("ATS connected!")
        api.set_input_gain_direct(0, 10)  # 10x gain
    elif api.is_aio_connected():
        print("AIO connected!")
        info = api.get_device_info()
        print(f"Inputs: {info.num_inputs}")
```

### Manual Initialization

```python
from echo_api import EchoAPI

api = EchoAPI()
api.initialize()

try:
    if api.is_ats_connected():
        serial = api.ats_get_serial_number()
        print(f"ATS Serial: {serial}")
finally:
    api.shutdown()
```

## Custom DLL Path

If the library is installed in a non-default location:

```python
from pathlib import Path
from echo_api import EchoAPI

api = EchoAPI(dll_path=Path("D:/Custom/Path/EchoAPI.dll"))
api.initialize()
```

## Examples

See the `examples/` directory for complete examples:

- `basic_usage.py` - Basic device detection and configuration
- `ats_example.py` - ATS-specific features

## API Reference

### Device Detection

```python
api.is_aio_connected()     # Returns True if AIO connected
api.is_ats_connected()     # Returns True if ATS connected
api.get_device_info()      # Returns DeviceInfo dataclass
```

### Input Channels

```python
api.has_input_gain_control(channel)    # Check if channel has gain
api.get_input_gain(channel)            # Get current gain
api.set_input_gain_direct(channel, multiplier)  # Set gain (1/3/10/31/100)
api.has_constant_current_control(channel)  # Check CCP support
api.get_constant_current_state(channel)    # Get CCP state
api.set_constant_current_state(channel, enabled)  # Enable/disable CCP
```

### Output Channels

```python
api.has_output_gain_control(channel)   # Check if channel has gain
api.get_output_gain(channel)           # Get gain (0-255)
api.set_output_gain(channel, gain)     # Set gain (0-255)
```

### ATS-Specific

```python
api.ats_get_serial_number()            # Get device serial number
api.ats_get_aux_out()                  # Get AUX output state
api.ats_set_aux_out(bits)              # Set AUX output (0-15)
api.ats_get_aux_in()                   # Get AUX input state
api.ats_get_analog_input_mode(ch)      # Get input mode
api.ats_set_analog_input_mode(ch, mode)  # Set input mode (0=Loopback, 1=Analog)
api.ats_get_analog_output_mode(ch)     # Get output mode
api.ats_set_analog_output_mode(ch, mode)  # Set output mode (0=Line, 1=Amp, 2=HP)
```

## Error Handling

All methods that can fail raise `RuntimeError` with an error message:

```python
try:
    api.set_input_gain_direct(0, 999)  # Invalid gain
except RuntimeError as e:
    print(f"Error: {e}")
```

## Data Classes

### DeviceInfo

```python
@dataclass
class DeviceInfo:
    is_aio_connected: bool
    is_ats_connected: bool
    num_inputs: int
    num_outputs: int
    module_slot_0: ModuleType
    module_slot_1: ModuleType
    library_version: str
```

### ChannelConfig

```python
@dataclass
class ChannelConfig:
    channel: int
    has_gain_control: bool
    gain: Optional[int]
    has_ccp_control: bool
    ccp_enabled: Optional[bool]
    has_teds: bool
```

## Enums

### ModuleType

```python
class ModuleType(IntEnum):
    UNKNOWN = -1
    NONE = 0
    A = 1      # Analog mic
    S = 2      # Speaker monitor
    L = 3      # Line
    C = 4      # Combo
    H = 5      # Headphone
    T = 6      # TDM
    B = 7      # Bluetooth
    ATS_A = 8  # ATS analog
    ATS_D = 9  # ATS digital
```

### ClockSource

```python
class ClockSource(IntEnum):
    INTERNAL = 0
    USB = 1
    CENTER_MODULE = 2
    OUTER_MODULE = 3
```
