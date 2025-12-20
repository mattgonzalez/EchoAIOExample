#!/usr/bin/env python3
"""
ATS-BT Control Examples
========================
Example scripts showing how to use the ATS-BT Python interface.

Run these examples:
    python ats_bt_examples.py

Or import and use in your own scripts:
    from ats_bt_control import ATSBT
"""

from ats_bt_control import ATSBT
import time


def example_basic_info():
    """Example: Get basic device information"""
    print("\n" + "=" * 50)
    print("Example: Basic Device Information")
    print("=" * 50)

    bt = ATSBT()

    if not bt.connect():
        print("Could not connect to device")
        return

    try:
        # Get device info
        print(f"\nMAC Address: {bt.get_mac_address()}")
        print(f"Device Name: {bt.get_name()}")
        print(f"Firmware:    {bt.get_version()}")
        print(f"Status:      {bt.get_status()}")

    finally:
        bt.disconnect()


def example_check_connection():
    """Example: Check Bluetooth connection status"""
    print("\n" + "=" * 50)
    print("Example: Connection Status Check")
    print("=" * 50)

    bt = ATSBT()

    if not bt.connect():
        return

    try:
        if bt.is_paired():
            print("\n✓ Device has an active Bluetooth connection")
        else:
            print("\n✗ Device is not connected to any Bluetooth host")

        if bt.is_discoverable():
            print("✓ Device is discoverable")
        else:
            print("✗ Device is not in discoverable mode")

    finally:
        bt.disconnect()


def example_send_commands():
    """Example: Send custom commands"""
    print("\n" + "=" * 50)
    print("Example: Sending Custom Commands")
    print("=" * 50)

    bt = ATSBT()

    if not bt.connect():
        return

    try:
        # List of commands to try
        commands = [
            "VERSION",
            "STATUS",
            "GET NAME",
            "GET LOCAL_ADDR",
            "LIST",  # List paired devices
        ]

        for cmd in commands:
            print(f"\n>>> {cmd}")
            response = bt.send_command(cmd)
            print(response)
            time.sleep(0.2)  # Small delay between commands

    finally:
        bt.disconnect()


def example_media_control():
    """Example: Media playback control (when connected to audio source)"""
    print("\n" + "=" * 50)
    print("Example: Media Control")
    print("=" * 50)

    bt = ATSBT()

    if not bt.connect():
        return

    try:
        if not bt.is_paired():
            print("\nDevice is not connected to an audio source.")
            print("Connect a phone/computer first to test media controls.")
            return

        print("\nSending play command...")
        print(bt.play())

        time.sleep(2)

        print("Sending pause command...")
        print(bt.pause())

    finally:
        bt.disconnect()


def example_scripted_setup():
    """Example: Automated device setup script"""
    print("\n" + "=" * 50)
    print("Example: Automated Setup Script")
    print("=" * 50)

    bt = ATSBT()

    if not bt.connect():
        return

    try:
        # Get device info
        mac = bt.get_mac_address()
        print(f"\nDevice MAC: {mac}")

        # Get current status
        status = bt.get_status()
        print(f"Current Status: {status}")

        # You can add your own setup commands here

        # Example: Check paired devices
        paired = bt.get_paired_devices()
        print(f"\nPaired Devices:\n{paired}")

    finally:
        bt.disconnect()


def example_monitor_status():
    """Example: Monitor device status in a loop"""
    print("\n" + "=" * 50)
    print("Example: Status Monitor (Ctrl+C to stop)")
    print("=" * 50)

    bt = ATSBT()

    if not bt.connect():
        return

    try:
        print("\nMonitoring device status... (Press Ctrl+C to stop)")
        print("-" * 40)

        while True:
            status = bt.get_status()
            connected = "YES" if bt.is_paired() else "NO"
            print(f"Connected: {connected} | Status: {status.replace(chr(10), ' ')}")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\nStopped monitoring.")

    finally:
        bt.disconnect()


def run_all_examples():
    """Run all examples"""
    print("\n" + "#" * 60)
    print("#  ATS-BT Control Examples")
    print("#" * 60)

    # First, check if device is available
    port = ATSBT.find_device()
    if not port:
        print("\nNo ATS-BT device found!")
        print("\nAvailable ports:")
        for p in ATSBT.list_ports():
            marker = " <-- ATS-BT" if p['is_ats_bt'] else ""
            print(f"  {p['device']}: {p['description']}{marker}")
        return

    print(f"\nFound ATS-BT device at: {port}")

    # Run examples
    example_basic_info()
    example_check_connection()
    example_send_commands()
    example_scripted_setup()

    # These are interactive, uncomment to run:
    # example_media_control()
    # example_monitor_status()

    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)


if __name__ == '__main__':
    run_all_examples()
