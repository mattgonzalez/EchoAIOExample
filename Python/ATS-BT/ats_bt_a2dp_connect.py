#!/usr/bin/env python3
"""
ATS-BT A2DP/AVRCP Connection Example
=====================================
Interactive script for connecting to a classic Bluetooth audio device
(headphones, speakers) via A2DP (audio) and AVRCP (remote control).

Usage:
    python ats_bt_a2dp_connect.py

This script will guide you through:
1. Scanning for nearby Bluetooth devices
2. Pairing with a selected device
3. Establishing A2DP audio stream
4. Establishing AVRCP control channel
5. Controlling media playback

Author: ATS Engineering
"""

from ats_bt_control import ATSBT
import time
import re
import sys


class A2DPConnection:
    """
    Manages A2DP/AVRCP connections to Bluetooth audio devices.
    """

    def __init__(self, bt: ATSBT):
        self.bt = bt
        self.paired_address: str = None
        self.a2dp_link_id: str = None
        self.avrcp_link_id: str = None

    def scan_for_devices(self, duration: int = 5) -> list:
        """
        Scan for nearby Bluetooth devices.

        Args:
            duration: Scan duration in seconds (default 5)

        Returns:
            List of discovered devices with address, name, and RSSI
        """
        print(f"\nScanning for Bluetooth devices ({duration} seconds)...")
        print("Make sure your audio device is in pairing mode!\n")

        # Use raw serial for better control of async responses
        self.bt.serial.reset_input_buffer()
        self.bt.serial.write(f"INQUIRY {duration}\r".encode('ascii'))
        self.bt.serial.flush()

        # Collect responses for duration + buffer time
        import time
        lines = []
        start = time.time()
        while time.time() - start < duration + 3:
            if self.bt.serial.in_waiting > 0:
                line = self.bt.serial.readline().decode('ascii', errors='ignore').strip()
                if line:
                    lines.append(line)
                    # Print progress
                    if 'INQUIRY' in line and 'INQU_OK' not in line:
                        print(f"  Found device...")
            time.sleep(0.05)

        # Parse discovered devices
        # Format: INQUIRY <addr> "<name>" <cod> <rssi> dBm
        # May have PENDING prefix concatenated
        devices = []
        for line in lines:
            # Handle PENDING prefix concatenation
            if 'PENDINGINQUIRY' in line:
                line = line.replace('PENDINGINQUIRY', 'INQUIRY')

            # Match INQUIRY result lines (not INQU_OK or INQUIRY_COMPLETE)
            if 'INQUIRY ' in line and 'INQU_OK' not in line and 'INQUIRY_' not in line:
                # Extract with regex for quoted names
                # Format: INQUIRY F84E1776FDB1 "LinkBuds S" 240404 -61 dBm
                match = re.search(
                    r'INQUIRY\s+([0-9A-Fa-f]{12})\s+"([^"]+)"\s+([0-9A-Fa-f]+)\s+(-?\d+)',
                    line
                )
                if match:
                    devices.append({
                        'address': match.group(1),
                        'name': match.group(2),
                        'rssi': int(match.group(4))
                    })
                else:
                    # Try unquoted format
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'INQUIRY' and i + 1 < len(parts):
                            addr = parts[i + 1]
                            if len(addr) == 12 and all(c in '0123456789ABCDEFabcdef' for c in addr):
                                devices.append({
                                    'address': addr,
                                    'name': 'Unknown',
                                    'rssi': None
                                })
                            break

        return devices

    def pair_device(self, address: str) -> bool:
        """
        Pair with a Bluetooth device.

        Args:
            address: Bluetooth MAC address

        Returns:
            True if pairing successful
        """
        print(f"\nPairing with {address}...")
        response = self.bt.send_command(f"PAIR {address}", timeout=30.0)

        if 'OK' in response or 'PAIR_OK' in response:
            self.paired_address = address
            print("Pairing successful!")
            return True
        elif 'ERROR' in response:
            print(f"Pairing failed: {response}")
            return False
        else:
            # Some responses may indicate pending - device may need confirmation
            print(f"Pairing response: {response}")
            self.paired_address = address
            return True

    def _open_profile(self, address: str, profile: str, default_link_id: str, timeout: float = 10.0) -> tuple:
        """
        Open a Bluetooth profile connection with async response handling.

        Args:
            address: Bluetooth address
            profile: Profile name (A2DP or AVRCP)
            default_link_id: Default link ID if not in response
            timeout: Connection timeout in seconds

        Returns:
            Tuple of (success: bool, link_id: str or None)
        """
        import time

        self.bt.serial.reset_input_buffer()
        self.bt.serial.write(f"OPEN {address} {profile}\r".encode('ascii'))
        self.bt.serial.flush()

        # Collect responses
        start = time.time()
        lines = []
        while time.time() - start < timeout:
            if self.bt.serial.in_waiting > 0:
                line = self.bt.serial.readline().decode('ascii', errors='ignore').strip()
                if line:
                    lines.append(line)
                    # Check for completion
                    if 'OPEN_OK' in line or 'ERROR' in line:
                        break
            time.sleep(0.05)

        response = '\n'.join(lines)

        # Look for OPEN_OK with link ID
        if 'OPEN_OK' in response:
            match = re.search(r'OPEN_OK[^\d]*(\d+)', response)
            link_id = match.group(1) if match else default_link_id
            return True, link_id
        elif 'ERROR' in response:
            return False, None
        elif 'PENDING' in response:
            # Connection in progress, wait a bit more for result
            time.sleep(2.0)
            # Check for any additional response
            while self.bt.serial.in_waiting > 0:
                line = self.bt.serial.readline().decode('ascii', errors='ignore').strip()
                if 'OPEN_OK' in line:
                    match = re.search(r'OPEN_OK[^\d]*(\d+)', line)
                    link_id = match.group(1) if match else default_link_id
                    return True, link_id
            # Assume pending means it will connect
            return True, default_link_id
        else:
            return False, None

    def open_a2dp(self, address: str = None) -> bool:
        """
        Open A2DP audio stream connection.

        Args:
            address: Bluetooth address (uses paired address if not specified)

        Returns:
            True if connection successful
        """
        addr = address or self.paired_address
        if not addr:
            print("Error: No device address specified")
            return False

        print(f"\nOpening A2DP audio stream to {addr}...")
        success, link_id = self._open_profile(addr, "A2DP", "10", timeout=15.0)

        if success:
            self.a2dp_link_id = link_id
            print(f"A2DP connected! Link ID: {self.a2dp_link_id}")
            return True
        else:
            print("A2DP connection failed")
            return False

    def open_avrcp(self, address: str = None) -> bool:
        """
        Open AVRCP control channel.

        Args:
            address: Bluetooth address (uses paired address if not specified)

        Returns:
            True if connection successful
        """
        addr = address or self.paired_address
        if not addr:
            print("Error: No device address specified")
            return False

        print(f"\nOpening AVRCP control channel to {addr}...")
        success, link_id = self._open_profile(addr, "AVRCP", "11", timeout=15.0)

        if success:
            self.avrcp_link_id = link_id
            print(f"AVRCP connected! Link ID: {self.avrcp_link_id}")
            return True
        else:
            print("AVRCP connection failed")
            return False

    def music_play(self) -> str:
        """Send play command via AVRCP."""
        if not self.avrcp_link_id:
            return self.bt.send_command("AVRCP PLAY")
        return self.bt.send_command(f"MUSIC {self.avrcp_link_id} PLAY")

    def music_pause(self) -> str:
        """Send pause command via AVRCP."""
        if not self.avrcp_link_id:
            return self.bt.send_command("AVRCP PAUSE")
        return self.bt.send_command(f"MUSIC {self.avrcp_link_id} PAUSE")

    def music_stop(self) -> str:
        """Send stop command via AVRCP."""
        if not self.avrcp_link_id:
            return self.bt.send_command("AVRCP STOP")
        return self.bt.send_command(f"MUSIC {self.avrcp_link_id} STOP")

    def set_volume(self, level: int) -> str:
        """
        Set volume level.

        Args:
            level: Volume level 0-127
        """
        level = max(0, min(127, level))
        # Use AVRCP link ID for volume control
        link_id = self.avrcp_link_id or "11"
        return self.bt.send_command(f"VOLUME {link_id} {level}")

    def disconnect(self) -> None:
        """Close all connections."""
        if self.a2dp_link_id:
            print(f"Closing A2DP link {self.a2dp_link_id}...")
            self.bt.send_command(f"CLOSE {self.a2dp_link_id}")
            self.a2dp_link_id = None

        if self.avrcp_link_id:
            print(f"Closing AVRCP link {self.avrcp_link_id}...")
            self.bt.send_command(f"CLOSE {self.avrcp_link_id}")
            self.avrcp_link_id = None


def print_devices(devices: list) -> None:
    """Print discovered devices in a formatted table."""
    if not devices:
        print("No devices found.")
        return

    print("\nDiscovered Devices:")
    print("-" * 60)
    print(f"{'#':<4} {'Address':<14} {'RSSI':<6} {'Name'}")
    print("-" * 60)
    for i, dev in enumerate(devices, 1):
        rssi_str = f"{dev['rssi']}dB" if dev['rssi'] else "N/A"
        print(f"{i:<4} {dev['address']:<14} {rssi_str:<6} {dev['name']}")
    print("-" * 60)


def select_device(devices: list) -> dict:
    """Prompt user to select a device."""
    while True:
        try:
            choice = input("\nEnter device number to connect (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None
            num = int(choice)
            if 1 <= num <= len(devices):
                return devices[num - 1]
            print(f"Please enter a number between 1 and {len(devices)}")
        except ValueError:
            print("Invalid input. Enter a number or 'q' to quit.")


def media_control_menu(conn: A2DPConnection) -> None:
    """Interactive media control menu."""
    print("\n" + "=" * 50)
    print("Media Control")
    print("=" * 50)
    print("Commands:")
    print("  p  - Play")
    print("  s  - Pause/Stop")
    print("  v+ - Volume up")
    print("  v- - Volume down")
    print("  q  - Quit")
    print()

    volume = 64  # Start at mid-level

    while True:
        try:
            cmd = input("media> ").strip().lower()

            if cmd == 'q':
                break
            elif cmd == 'p':
                print(conn.music_play())
            elif cmd == 's':
                print(conn.music_pause())
            elif cmd == 'v+':
                volume = min(127, volume + 10)
                print(f"Volume: {volume}")
                print(conn.set_volume(volume))
            elif cmd == 'v-':
                volume = max(0, volume - 10)
                print(f"Volume: {volume}")
                print(conn.set_volume(volume))
            elif cmd:
                print("Unknown command. Use p/s/v+/v-/q")

        except KeyboardInterrupt:
            print()
            break


def main():
    """Main interactive connection workflow."""
    print("=" * 60)
    print("ATS-BT A2DP/AVRCP Connection Tool")
    print("=" * 60)

    # Connect to ATS-BT
    bt = ATSBT()
    if not bt.connect():
        print("\nFailed to connect to ATS-BT device.")
        print("Use 'python ats_bt_control.py --list' to check available ports.")
        return 1

    print(f"Connected to ATS-BT at {bt.port}")
    print(f"Device MAC: {bt.get_mac_address()}")

    conn = A2DPConnection(bt)

    try:
        # Step 1: Prompt user to prepare their device
        print("\n" + "-" * 60)
        print("STEP 1: Prepare Your Audio Device")
        print("-" * 60)
        print("Put your Bluetooth headphones/speaker into PAIRING MODE.")
        print("(Usually: hold power button until LED flashes rapidly)")
        print()
        input("Press ENTER when your device is in pairing mode...")

        # Step 2: Scan for devices
        print("\n" + "-" * 60)
        print("STEP 2: Scanning for Devices")
        print("-" * 60)
        devices = conn.scan_for_devices(duration=5)

        if not devices:
            print("\nNo devices found. Make sure your device is in pairing mode.")
            rescan = input("Try scanning again? (y/n): ").strip().lower()
            if rescan == 'y':
                devices = conn.scan_for_devices(duration=8)

        if not devices:
            print("No devices found. Exiting.")
            return 1

        print_devices(devices)

        # Step 3: Select device
        print("\n" + "-" * 60)
        print("STEP 3: Select Device")
        print("-" * 60)
        selected = select_device(devices)
        if not selected:
            print("Cancelled.")
            return 0

        print(f"\nSelected: {selected['name']} ({selected['address']})")

        # Step 4: Pair
        print("\n" + "-" * 60)
        print("STEP 4: Pairing")
        print("-" * 60)
        if not conn.pair_device(selected['address']):
            print("Pairing failed. Device may need to accept pairing request.")
            proceed = input("Continue anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                return 1

        # Step 5: Open A2DP
        print("\n" + "-" * 60)
        print("STEP 5: Establishing A2DP Audio Connection")
        print("-" * 60)
        if not conn.open_a2dp():
            print("Failed to open A2DP connection.")
            return 1

        # Step 6: Open AVRCP
        print("\n" + "-" * 60)
        print("STEP 6: Establishing AVRCP Control Channel")
        print("-" * 60)
        if not conn.open_avrcp():
            print("Warning: AVRCP connection failed. Media controls may not work.")

        # Step 7: Media controls
        print("\n" + "-" * 60)
        print("CONNECTION COMPLETE!")
        print("-" * 60)
        print(f"Device: {selected['name']}")
        print(f"Address: {selected['address']}")
        print(f"A2DP Link: {conn.a2dp_link_id}")
        print(f"AVRCP Link: {conn.avrcp_link_id}")

        # Enter media control mode
        media_control_menu(conn)

        # Cleanup
        print("\nDisconnecting...")
        conn.disconnect()

    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        conn.disconnect()

    finally:
        bt.disconnect()

    print("Done.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
