#!/usr/bin/env python3
"""
Echo ATS-Specific Example

Demonstrates ATS-specific features including:
- Analog input/output mode configuration
- Digital I/O mode
- AUX GPIO control
- Gain configuration with ATS-specific values
"""

import sys
from pathlib import Path

# Add parent directory to path to import echo_api
sys.path.insert(0, str(Path(__file__).parent.parent))

from echo_api import EchoAPIContext


def main():
    print("=" * 60)
    print("Echo ATS Example")
    print("=" * 60)

    with EchoAPIContext() as api:
        # Check for ATS device
        if not api.is_ats_connected():
            print("\nNo ATS device connected!")
            print("This example requires an Echo ATS device.")
            return

        # Get device info
        serial = api.ats_get_serial_number()
        num_inputs = api.get_num_inputs()
        num_outputs = api.get_num_outputs()

        print(f"\nATS Device Connected")
        print(f"  Serial Number: {serial}")
        print(f"  Input Channels: {num_inputs}")
        print(f"  Output Channels: {num_outputs}")

        # =============================================
        # Input Gain Configuration
        # =============================================
        print("\n--- Input Gain Configuration ---")
        print("ATS supports gain multipliers: 1x, 3x, 10x, 31x, 100x")

        # Show current gain for all analog inputs
        for ch in range(8):
            gain = api.get_input_gain(ch)
            print(f"  Channel {ch}: {gain}x")

        # Example: Set channel 0 to each gain value
        print("\nSetting channel 0 through all gain values:")
        gains = [1, 3, 10, 31, 100]
        for gain in gains:
            api.set_input_gain_direct(0, gain)
            readback = api.get_input_gain(0)
            print(f"  Set {gain}x -> Read {readback}x")

        # Restore to 1x
        api.set_input_gain_direct(0, 1)

        # =============================================
        # Analog Input Mode
        # =============================================
        print("\n--- Analog Input Mode ---")
        print("Modes: 0=Loopback (output->input), 1=Analog (external connector)")

        for ch in range(8):
            mode = api.ats_get_analog_input_mode(ch)
            mode_name = "Analog" if mode == 1 else "Loopback"
            print(f"  Channel {ch}: {mode_name}")

        # Example: Toggle mode on channel 0
        original_mode = api.ats_get_analog_input_mode(0)
        new_mode = 0 if original_mode == 1 else 1
        api.ats_set_analog_input_mode(0, new_mode)
        print(f"\nToggled channel 0 to: {'Analog' if new_mode else 'Loopback'}")
        api.ats_set_analog_input_mode(0, original_mode)  # Restore
        print(f"Restored to: {'Analog' if original_mode else 'Loopback'}")

        # =============================================
        # Analog Output Mode
        # =============================================
        print("\n--- Analog Output Mode ---")
        print("Modes: 0=Line Level, 1=Amplifier, 2=Headphone")

        mode_names = {0: "Line", 1: "Amplifier", 2: "Headphone"}
        for ch in range(4):
            mode = api.ats_get_analog_output_mode(ch)
            print(f"  Channel {ch}: {mode_names[mode]}")

        # Example: Cycle through modes on channel 0
        print("\nCycling channel 0 through all output modes:")
        original_out_mode = api.ats_get_analog_output_mode(0)
        for mode in [0, 1, 2]:
            api.ats_set_analog_output_mode(0, mode)
            readback = api.ats_get_analog_output_mode(0)
            print(f"  Set {mode_names[mode]} -> Read {mode_names[readback]}")
        api.ats_set_analog_output_mode(0, original_out_mode)  # Restore

        # =============================================
        # Digital I/O Mode
        # =============================================
        print("\n--- Digital I/O Mode ---")

        dio_mode = api.ats_get_digital_io_mode()
        dio_name = "Word Clock" if dio_mode == 1 else "S/PDIF"
        print(f"Current mode: {dio_name}")

        # Word clock termination (only relevant in word clock mode)
        terminated = api.ats_get_word_clock_terminated()
        print(f"Word clock termination: {'Enabled' if terminated else 'Disabled'}")

        # =============================================
        # AUX GPIO
        # =============================================
        print("\n--- AUX GPIO (4-bit) ---")

        aux_out = api.ats_get_aux_out()
        aux_in = api.ats_get_aux_in()
        print(f"AUX Output: 0x{aux_out:X} (binary: {aux_out:04b})")
        print(f"AUX Input:  0x{aux_in:X} (binary: {aux_in:04b})")

        # Example: Set each AUX bit individually
        print("\nSetting each AUX output bit:")
        original_aux = api.ats_get_aux_out()
        for bit in range(4):
            value = 1 << bit
            api.ats_set_aux_out(value)
            readback = api.ats_get_aux_out()
            print(f"  Bit {bit} (0x{value:X}): Read 0x{readback:X}")
        api.ats_set_aux_out(original_aux)  # Restore
        print(f"Restored to: 0x{original_aux:X}")

        # =============================================
        # CCP (Constant Current Power)
        # =============================================
        print("\n--- CCP Control ---")

        for ch in range(8):
            if api.has_constant_current_control(ch):
                ccp = api.get_constant_current_state(ch)
                print(f"  Channel {ch}: {'ON' if ccp else 'OFF'}")
            else:
                print(f"  Channel {ch}: N/A")

        # =============================================
        # Impedance Mode
        # =============================================
        print("\n--- Impedance Mode ---")

        imp_mode = api.ats_get_impedance_mode()
        print(f"Impedance mode: {'Enabled' if imp_mode else 'Disabled'}")

        print("\n" + "=" * 60)
        print("ATS Example complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
