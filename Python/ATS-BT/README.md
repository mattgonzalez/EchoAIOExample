# ATS-BT Python Interface

Python scripts for controlling ATS-BT Bluetooth audio test devices.

## Requirements

```bash
pip install pyserial
```

## Files

| File | Description |
|------|-------------|
| `ats_bt_control.py` | Core control library and interactive CLI |
| `ats_bt_a2dp_connect.py` | Interactive A2DP/AVRCP connection workflow |
| `ats_bt_examples.py` | Usage examples |

## Quick Start

### As a Module

```python
from ats_bt_control import ATSBT

bt = ATSBT()  # Auto-detects device
bt.connect()

print(bt.get_mac_address())
print(bt.get_device_info())

bt.disconnect()
```

### Command Line

```bash
# List available serial ports
python ats_bt_control.py --list

# Show device information
python ats_bt_control.py --info

# Send a command
python ats_bt_control.py --cmd "GET STATUS"

# Interactive mode
python ats_bt_control.py --interactive
```

### Connect to Bluetooth Audio Device

```bash
python ats_bt_a2dp_connect.py
```

This interactive script guides you through:
1. Scanning for nearby Bluetooth devices
2. Pairing with a selected device
3. Establishing A2DP audio stream
4. Establishing AVRCP control channel
5. Controlling media playback

## API Reference

### ATSBT Class

```python
bt = ATSBT(port=None, baudrate=115200)
```

**Connection:**
- `connect()` - Connect to device (auto-detects if port not specified)
- `disconnect()` - Close connection
- `is_connected()` - Check connection status

**Device Info:**
- `get_mac_address()` - Get Bluetooth MAC address
- `get_name()` - Get device name
- `get_version()` - Get firmware version
- `get_status()` - Get current status
- `get_device_info()` - Get all info as dictionary

**Bluetooth Operations:**
- `start_discovery()` - Scan for nearby devices
- `pair(address)` - Pair with a device
- `unpair(address)` - Remove pairing
- `connect_audio(address)` - Connect to paired audio device
- `disconnect_audio()` - Disconnect audio

**Media Control (AVRCP):**
- `play()` - Play
- `pause()` - Pause
- `next_track()` - Next track
- `previous_track()` - Previous track
- `volume_up()` - Volume up
- `volume_down()` - Volume down

**Utility:**
- `send_command(cmd)` - Send raw command
- `reset()` - Reset device
