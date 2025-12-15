#!/usr/bin/env python3
"""
Basic Echo API Usage Example

Demonstrates device detection, configuration reading, and basic control.
Works with both Echo AIO and Echo ATS devices.
"""

import sys
from pathlib import Path

# Add parent directory to path to import echo_api
sys.path.insert(0, str(Path(__file__).parent.parent))

from echo_api import EchoAPIContext, ModuleType


def main():
    print("=" * 60)
    print("Echo API Basic Usage Example")
    print("=" * 60)

    with EchoAPIContext() as api:
        # Get library version
        version = api.get_library_version()
        print(f"\nLibrary version: {version}")

        # Check for connected devices
        if api.is_ats_connected():
            print("\nDevice: Echo ATS")
            serial = api.ats_get_serial_number()
            print(f"Serial number: {serial}")
        elif api.is_aio_connected():
            print("\nDevice: Echo AIO")
        else:
            print("\nNo device connected!")
            return

        # Get device info
        info = api.get_device_info()
        print(f"\nChannel Configuration:")
        print(f"  Input channels: {info.num_inputs}")
        print(f"  Output channels: {info.num_outputs}")

        # Show module types (AIO only)
        if info.is_aio_connected:
            print(f"\nModule Configuration:")
            print(f"  Slot 0 (center): {info.module_slot_0.name}")
            print(f"  Slot 1 (outer): {info.module_slot_1.name}")

        # Read input channel configuration
        print(f"\nInput Channel Details:")
        for ch in range(min(info.num_inputs, 4)):  # Show first 4 channels
            config = api.get_channel_config(ch)
            print(f"\n  Channel {ch}:")
            if config.has_gain_control:
                print(f"    Gain: {config.gain}x")
            else:
                print(f"    Gain: N/A")
            if config.has_ccp_control:
                state = "ON" if config.ccp_enabled else "OFF"
                print(f"    CCP: {state}")
            else:
                print(f"    CCP: N/A")
            print(f"    TEDS: {'Yes' if config.has_teds else 'No'}")

        # Example: Configure channel 0 (if it has gain control)
        if api.has_input_gain_control(0):
            print(f"\n--- Configuring Channel 0 ---")

            # Set gain to 10x
            original_gain = api.get_input_gain(0)
            print(f"Current gain: {original_gain}x")

            api.set_input_gain_direct(0, 10)
            new_gain = api.get_input_gain(0)
            print(f"Set gain to: {new_gain}x")

            # Restore original gain
            api.set_input_gain_direct(0, original_gain)
            print(f"Restored gain to: {original_gain}x")

        # Example: Toggle CCP (if supported)
        if api.has_constant_current_control(0):
            print(f"\n--- CCP Control ---")

            original_ccp = api.get_constant_current_state(0)
            print(f"Current CCP state: {'ON' if original_ccp else 'OFF'}")

            # Toggle CCP
            api.set_constant_current_state(0, not original_ccp)
            new_ccp = api.get_constant_current_state(0)
            print(f"Toggled to: {'ON' if new_ccp else 'OFF'}")

            # Restore
            api.set_constant_current_state(0, original_ccp)
            print(f"Restored to: {'ON' if original_ccp else 'OFF'}")

        print("\n" + "=" * 60)
        print("Example complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
