#!/usr/bin/env python3
"""
ATS-BT Control Script
======================
Simple Python interface for controlling ATS-BT Bluetooth devices on macOS/Linux/Windows.

Installation:
    pip install pyserial

Usage:
    # As a module
    from ats_bt_control import ATSBT

    bt = ATSBT()  # Auto-detect device
    bt.connect()
    print(bt.get_device_info())
    bt.disconnect()

    # From command line
    python ats_bt_control.py --list              # List available ports
    python ats_bt_control.py --info              # Show device info
    python ats_bt_control.py --cmd "GET STATUS"  # Send a command
    python ats_bt_control.py --interactive       # Interactive mode

Author: ATS Engineering
"""

import serial
import serial.tools.list_ports
import time
import sys
import argparse
from typing import Optional, List, Dict, Tuple


class ATSBT:
    """
    ATS-BT Bluetooth Device Controller

    Provides a simple interface to control ATS-BT devices via USB serial.

    Example:
        bt = ATSBT()
        bt.connect()

        # Get device information
        info = bt.get_device_info()
        print(f"Device: {info['name']}")
        print(f"MAC: {info['mac_address']}")

        # Check connection status
        if bt.is_paired():
            print("Device is paired!")

        bt.disconnect()
    """

    # STM32 USB CDC identifiers
    STM32_VID = 0x0483
    STM32_PID = 0x5740

    # Command timing (IDC777 requirement)
    COMMAND_DELAY = 0.15  # 150ms between commands
    DEFAULT_TIMEOUT = 2.0  # 2 second response timeout

    def __init__(self, port: Optional[str] = None, baudrate: int = 115200):
        """
        Initialize ATS-BT controller.

        Args:
            port: Serial port path (e.g., '/dev/cu.usbmodem1234' on macOS)
                  If None, will auto-detect the device.
            baudrate: Serial baudrate (default 115200)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial: Optional[serial.Serial] = None
        self._cached_mac: Optional[str] = None

    @classmethod
    def list_ports(cls) -> List[Dict]:
        """
        List all available serial ports.

        Returns:
            List of dictionaries with port information
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'description': port.description,
                'vid': port.vid,
                'pid': port.pid,
                'is_ats_bt': (port.vid == cls.STM32_VID and port.pid == cls.STM32_PID)
            })
        return ports

    @classmethod
    def find_device(cls) -> Optional[str]:
        """
        Auto-detect ATS-BT device port.

        Returns:
            Port path if found, None otherwise
        """
        for port in serial.tools.list_ports.comports():
            # Check VID:PID for STM32 CDC
            if port.vid == cls.STM32_VID and port.pid == cls.STM32_PID:
                return port.device
            # Fallback: check description
            if any(x in port.description.upper() for x in ['STM32', 'CDC', 'ATS']):
                return port.device
        return None

    def connect(self) -> bool:
        """
        Connect to the ATS-BT device.

        Returns:
            True if connection successful, False otherwise
        """
        # Auto-detect port if not specified
        if self.port is None:
            self.port = self.find_device()
            if self.port is None:
                print("Error: No ATS-BT device found. Use list_ports() to see available devices.")
                return False

        try:
            self.serial = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.DEFAULT_TIMEOUT,
                write_timeout=self.DEFAULT_TIMEOUT
            )
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            time.sleep(0.5)  # Let device settle
            return True
        except Exception as e:
            print(f"Error connecting to {self.port}: {e}")
            return False

    def disconnect(self):
        """Disconnect from the device."""
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.serial = None

    def is_connected(self) -> bool:
        """Check if connected to device."""
        return self.serial is not None and self.serial.is_open

    def send_command(self, command: str, timeout: Optional[float] = None) -> str:
        """
        Send a command to the device and return the response.

        Args:
            command: Command string (carriage return added automatically)
            timeout: Response timeout in seconds (default 2.0)

        Returns:
            Response string

        Raises:
            RuntimeError: If not connected
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to device. Call connect() first.")

        # Ensure command ends with CR
        if not command.endswith('\r'):
            command += '\r'

        # Clear input buffer
        self.serial.reset_input_buffer()

        # Send command
        self.serial.write(command.encode('ascii'))
        self.serial.flush()

        # Read response
        response_timeout = timeout if timeout is not None else self.DEFAULT_TIMEOUT
        response_lines = []
        start_time = time.time()

        while time.time() - start_time < response_timeout:
            if self.serial.in_waiting > 0:
                try:
                    line = self.serial.readline().decode('ascii', errors='ignore').strip()
                    if line:
                        response_lines.append(line)
                        # Check for terminal responses
                        if any(term in line for term in ['OK', 'ERROR', 'PENDING', 'ACK']):
                            break
                except Exception:
                    break
            time.sleep(0.01)

        # Required delay before next command
        time.sleep(self.COMMAND_DELAY)

        return '\n'.join(response_lines)

    # ==================== Device Information ====================

    def get_mac_address(self) -> str:
        """
        Get the device's Bluetooth MAC address.

        Returns:
            MAC address string (e.g., "00:1A:2B:3C:4D:5E")
        """
        if self._cached_mac:
            return self._cached_mac

        response = self.send_command("GET LOCAL_ADDR")
        # Parse response - format is typically "LOCAL_ADDR=XX:XX:XX:XX:XX:XX"
        for line in response.split('\n'):
            if 'LOCAL_ADDR' in line and '=' in line:
                value = line.split('=')[1].strip()
                # Strip trailing OK and CR (device sends without proper line ending)
                if value.endswith('OK'):
                    value = value[:-2]
                value = value.strip()
                self._cached_mac = value
                return self._cached_mac
            # Also handle space-separated format
            if 'LOCAL_ADDR' in line:
                parts = line.split()
                if len(parts) >= 2:
                    value = parts[-1].strip()
                    if value.endswith('OK'):
                        value = value[:-2]
                    value = value.strip()
                    self._cached_mac = value
                    return self._cached_mac
        return response

    def get_name(self) -> str:
        """Get the device's Bluetooth name."""
        response = self.send_command("GET NAME")
        for line in response.split('\n'):
            if 'NAME' in line and '=' in line:
                value = line.split('=')[1].strip()
                # Strip trailing OK and CR (device sends without proper line ending)
                if value.endswith('OK'):
                    value = value[:-2]
                return value.strip()
        return response

    def get_version(self) -> str:
        """Get firmware version."""
        return self.send_command("VERSION")

    def get_status(self) -> str:
        """Get device status."""
        response = self.send_command("STATUS")
        # Strip trailing OK (device may send it without newline)
        if response.endswith('OK'):
            response = response[:-2].rstrip()
        return response

    def get_device_info(self) -> Dict:
        """
        Get comprehensive device information.

        Returns:
            Dictionary with device info
        """
        return {
            'mac_address': self.get_mac_address(),
            'name': self.get_name(),
            'version': self.get_version(),
            'status': self.get_status(),
            'port': self.port
        }

    # ==================== Bluetooth Status ====================

    def is_paired(self) -> bool:
        """Check if device is paired with a host."""
        status = self.get_status()
        return 'CONNECTION' in status.upper() or 'PAIRED' in status.upper()

    def is_discoverable(self) -> bool:
        """Check if device is in discoverable mode."""
        status = self.get_status()
        return 'DISCOVERABLE' in status.upper()

    # ==================== Bluetooth Operations ====================

    def get_paired_devices(self) -> str:
        """Get list of paired devices."""
        return self.send_command("LIST")

    def start_discovery(self) -> str:
        """Start Bluetooth discovery/inquiry."""
        return self.send_command("INQUIRY", timeout=10.0)

    def stop_discovery(self) -> str:
        """Stop Bluetooth discovery."""
        return self.send_command("INQUIRY OFF")

    def pair(self, address: str) -> str:
        """
        Initiate pairing with a device.

        Args:
            address: Bluetooth address to pair with
        """
        return self.send_command(f"PAIR {address}", timeout=30.0)

    def unpair(self, address: str) -> str:
        """
        Remove pairing with a device.

        Args:
            address: Bluetooth address to unpair
        """
        return self.send_command(f"UNPAIR {address}")

    def connect_audio(self, address: str) -> str:
        """
        Connect to a paired audio device.

        Args:
            address: Bluetooth address to connect
        """
        return self.send_command(f"CONNECT {address}", timeout=10.0)

    def disconnect_audio(self) -> str:
        """Disconnect current audio connection."""
        return self.send_command("DISCONNECT")

    # ==================== Audio Controls ====================

    def play(self) -> str:
        """Send play command (AVRCP)."""
        return self.send_command("AVRCP PLAY")

    def pause(self) -> str:
        """Send pause command (AVRCP)."""
        return self.send_command("AVRCP PAUSE")

    def next_track(self) -> str:
        """Skip to next track (AVRCP)."""
        return self.send_command("AVRCP FORWARD")

    def previous_track(self) -> str:
        """Go to previous track (AVRCP)."""
        return self.send_command("AVRCP BACKWARD")

    def volume_up(self) -> str:
        """Increase volume."""
        return self.send_command("AVRCP VOL_UP")

    def volume_down(self) -> str:
        """Decrease volume."""
        return self.send_command("AVRCP VOL_DOWN")

    # ==================== Utility ====================

    def reset(self) -> bool:
        """
        Reset the device.

        Returns:
            True if reconnection successful after reset
        """
        self.send_command("RESET")
        self.disconnect()
        time.sleep(3.0)  # Wait for device to restart
        return self.connect()


def print_ports():
    """Print available serial ports."""
    ports = ATSBT.list_ports()
    if not ports:
        print("No serial ports found.")
        return

    print("\nAvailable Serial Ports:")
    print("-" * 60)
    for p in ports:
        marker = " <-- ATS-BT" if p['is_ats_bt'] else ""
        vid_pid = f"{p['vid']:04X}:{p['pid']:04X}" if p['vid'] else "Unknown"
        print(f"  {p['device']}")
        print(f"    Description: {p['description']}")
        print(f"    VID:PID: {vid_pid}{marker}")
        print()


def print_device_info(bt: ATSBT):
    """Print device information."""
    info = bt.get_device_info()
    print("\nATS-BT Device Information:")
    print("-" * 40)
    print(f"  Port:        {info['port']}")
    print(f"  MAC Address: {info['mac_address']}")
    print(f"  Name:        {info['name']}")
    print(f"  Version:     {info['version']}")
    print(f"  Status:      {info['status']}")
    print()


def interactive_mode(bt: ATSBT):
    """Run interactive command mode."""
    print("\nATS-BT Interactive Mode")
    print("=" * 40)
    print("Type commands to send to the device.")
    print("Type 'help' for available commands.")
    print("Type 'quit' or 'exit' to exit.")
    print()

    help_text = """
Available Commands:
  info          - Show device information
  status        - Get device status
  list          - List paired devices
  discover      - Start Bluetooth discovery
  play/pause    - Media controls
  next/prev     - Track controls
  vol+/vol-     - Volume controls
  reset         - Reset device
  quit/exit     - Exit interactive mode

  Any other text is sent as a raw command.
"""

    while True:
        try:
            cmd = input("ats-bt> ").strip()

            if not cmd:
                continue

            if cmd.lower() in ('quit', 'exit', 'q'):
                break

            if cmd.lower() == 'help':
                print(help_text)
                continue

            if cmd.lower() == 'info':
                print_device_info(bt)
                continue

            # Shortcut commands
            shortcuts = {
                'status': 'STATUS',
                'list': 'LIST',
                'discover': 'INQUIRY',
                'play': 'AVRCP PLAY',
                'pause': 'AVRCP PAUSE',
                'next': 'AVRCP FORWARD',
                'prev': 'AVRCP BACKWARD',
                'vol+': 'AVRCP VOL_UP',
                'vol-': 'AVRCP VOL_DOWN',
            }

            if cmd.lower() in shortcuts:
                cmd = shortcuts[cmd.lower()]

            if cmd.lower() == 'reset':
                print("Resetting device...")
                if bt.reset():
                    print("Device reset and reconnected successfully.")
                else:
                    print("Failed to reconnect after reset.")
                continue

            # Send command
            response = bt.send_command(cmd)
            if response:
                print(response)

        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='ATS-BT Bluetooth Device Control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                    List available serial ports
  %(prog)s --info                    Show device information
  %(prog)s --cmd "GET STATUS"        Send a single command
  %(prog)s --interactive             Start interactive mode
  %(prog)s --port /dev/cu.usbmodem1234 --info   Use specific port
"""
    )

    parser.add_argument('--list', '-l', action='store_true',
                       help='List available serial ports')
    parser.add_argument('--port', '-p', type=str, default=None,
                       help='Serial port (auto-detect if not specified)')
    parser.add_argument('--info', '-i', action='store_true',
                       help='Show device information')
    parser.add_argument('--cmd', '-c', type=str, default=None,
                       help='Send a command and print response')
    parser.add_argument('--interactive', '-I', action='store_true',
                       help='Start interactive command mode')

    args = parser.parse_args()

    # List ports only
    if args.list:
        print_ports()
        return 0

    # All other operations need a connection
    if not (args.info or args.cmd or args.interactive):
        parser.print_help()
        return 0

    # Create device and connect
    bt = ATSBT(port=args.port)

    if not bt.connect():
        print("\nTip: Use --list to see available ports")
        print("     Use --port to specify a port manually")
        return 1

    print(f"Connected to {bt.port}")

    try:
        if args.info:
            print_device_info(bt)

        if args.cmd:
            response = bt.send_command(args.cmd)
            print(response)

        if args.interactive:
            interactive_mode(bt)

    finally:
        bt.disconnect()

    return 0


if __name__ == '__main__':
    sys.exit(main())
