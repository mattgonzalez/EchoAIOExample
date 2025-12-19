"""
Echo API Python Wrapper

Python ctypes wrapper for EchoAPI.dll - provides access to the Echo API
for controlling Echo AIO and ATS devices.

Usage:
    from echo_api import EchoAPI

    api = EchoAPI()
    api.initialize()

    if api.is_ats_connected():
        api.set_input_gain_direct(0, 10)  # Set channel 0 to 10x gain

    api.shutdown()
"""

import ctypes
from ctypes import c_int, c_char_p, c_size_t, c_double, c_uint8, c_uint32, POINTER, byref
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import IntEnum
import platform


# Default DLL paths
# Windows: Installed by Echo Control Panel
# macOS: Copy libEchoAPI.dylib from the Echo Control Panel DMG to your project directory
if platform.system() == "Windows":
    DEFAULT_DLL_PATH = Path("C:/Program Files/Echo Test Interfaces/EchoAPI.dll")
else:
    DEFAULT_DLL_PATH = Path("./libEchoAPI.dylib")


class ModuleType(IntEnum):
    """Module types returned by AIO_getModuleType"""
    UNKNOWN = -1
    NONE = 0
    A = 1      # AIO-A (analog mic)
    S = 2      # AIO-S (speaker monitor)
    L = 3      # AIO-L (line)
    C = 4      # AIO-C (combo)
    H = 5      # AIO-H (headphone)
    T = 6      # AIO-T (TDM)
    B = 7      # AIO-B (Bluetooth)
    ATS_A = 8  # ATS analog
    ATS_D = 9  # ATS digital


class ClockSource(IntEnum):
    """Clock source values"""
    INTERNAL = 0
    USB = 1
    CENTER_MODULE = 2
    OUTER_MODULE = 3


@dataclass
class DeviceInfo:
    """Information about connected device"""
    is_aio_connected: bool
    is_ats_connected: bool
    num_inputs: int
    num_outputs: int
    module_slot_0: ModuleType
    module_slot_1: ModuleType
    library_version: str


@dataclass
class ChannelConfig:
    """Configuration for an input channel"""
    channel: int
    has_gain_control: bool
    gain: Optional[int]
    has_ccp_control: bool
    ccp_enabled: Optional[bool]
    has_teds: bool


class EchoAPI:
    """
    Python wrapper for EchoAPI.dll

    Provides access to all exported API functions for controlling
    Echo AIO and ATS devices.

    Usage:
        api = EchoAPI()
        api.initialize()

        if api.is_ats_connected():
            info = api.get_device_info()
            print(f"ATS connected with {info.num_inputs} inputs")
            api.set_input_gain_direct(0, 10)

        api.shutdown()
    """

    def __init__(self, dll_path: Optional[Path] = None):
        """
        Initialize the API wrapper.

        Args:
            dll_path: Path to EchoAPI.dll. Uses default if not specified.
        """
        self.dll_path = dll_path or DEFAULT_DLL_PATH
        self._dll = None
        self._initialized = False

    def _load_dll(self):
        """Load the DLL and set up function signatures."""
        if self._dll is not None:
            return

        if not self.dll_path.exists():
            raise FileNotFoundError(f"EchoAPI library not found at {self.dll_path}")

        if platform.system() == "Windows":
            self._dll = ctypes.WinDLL(str(self.dll_path))
        else:
            self._dll = ctypes.CDLL(str(self.dll_path))

        self._setup_functions()

    def _setup_functions(self):
        """Set up ctypes function signatures."""
        dll = self._dll

        # Library management
        dll.AIO_initialize.argtypes = []
        dll.AIO_initialize.restype = None
        dll.AIO_shutdown.argtypes = []
        dll.AIO_shutdown.restype = None
        dll.AIO_getLibraryVersion.argtypes = [c_char_p, c_size_t]
        dll.AIO_getLibraryVersion.restype = None
        dll.AIO_getErrorString.argtypes = [c_char_p, c_size_t]
        dll.AIO_getErrorString.restype = None

        # Device inquiry
        dll.AIO_isAIOConnected.argtypes = []
        dll.AIO_isAIOConnected.restype = c_int
        dll.AIO_isATSConnected.argtypes = []
        dll.AIO_isATSConnected.restype = c_int
        dll.AIO_getNumInputChannels.argtypes = []
        dll.AIO_getNumInputChannels.restype = c_int
        dll.AIO_getNumOutputChannels.argtypes = []
        dll.AIO_getNumOutputChannels.restype = c_int
        dll.AIO_getModuleType.argtypes = [c_int]
        dll.AIO_getModuleType.restype = c_int
        dll.AIO_hasComboModule.argtypes = [c_int]
        dll.AIO_hasComboModule.restype = c_int
        dll.AIO_hasTModule.argtypes = [c_int]
        dll.AIO_hasTModule.restype = c_int
        dll.AIO_hasBluetoothModule.argtypes = [c_int]
        dll.AIO_hasBluetoothModule.restype = c_int

        # Input channel functions
        dll.AIO_hasInputGainControl.argtypes = [c_int]
        dll.AIO_hasInputGainControl.restype = c_int
        dll.AIO_getInputGain.argtypes = [c_int, POINTER(c_int)]
        dll.AIO_getInputGain.restype = c_int
        dll.AIO_setInputGain.argtypes = [c_int, c_int]
        dll.AIO_setInputGain.restype = c_int
        dll.AIO_setInputGainDirect.argtypes = [c_int, c_int]
        dll.AIO_setInputGainDirect.restype = c_int
        dll.AIO_hasConstantCurrentControl.argtypes = [c_int]
        dll.AIO_hasConstantCurrentControl.restype = c_int
        dll.AIO_getConstantCurrentState.argtypes = [c_int, POINTER(c_int)]
        dll.AIO_getConstantCurrentState.restype = c_int
        dll.AIO_setConstantCurrentState.argtypes = [c_int, c_int]
        dll.AIO_setConstantCurrentState.restype = c_int
        dll.AIO_hasTEDS.argtypes = [c_int]
        dll.AIO_hasTEDS.restype = c_int
        dll.AIO_getTEDSProperties.argtypes = [c_int, c_char_p, c_size_t, POINTER(c_size_t)]
        dll.AIO_getTEDSProperties.restype = c_int

        # Output channel functions
        dll.AIO_hasOutputGainControl.argtypes = [c_int]
        dll.AIO_hasOutputGainControl.restype = c_int
        dll.AIO_getOutputGain.argtypes = [c_int, POINTER(c_int)]
        dll.AIO_getOutputGain.restype = c_int
        dll.AIO_setOutputGain.argtypes = [c_int, c_int]
        dll.AIO_setOutputGain.restype = c_int

        # Module parameters
        dll.AIO_getModuleIntParameter.argtypes = [c_int, c_int, POINTER(c_int)]
        dll.AIO_getModuleIntParameter.restype = c_int
        dll.AIO_setModuleIntParameter.argtypes = [c_int, c_int, c_int]
        dll.AIO_setModuleIntParameter.restype = c_int
        dll.AIO_getModuleDoubleParameter.argtypes = [c_int, c_int, POINTER(c_double)]
        dll.AIO_getModuleDoubleParameter.restype = c_int
        dll.AIO_setModuleDoubleParameter.argtypes = [c_int, c_int, c_double]
        dll.AIO_setModuleDoubleParameter.restype = c_int

        # Device parameters
        dll.AIO_getDeviceIntParameter.argtypes = [c_int, POINTER(c_int)]
        dll.AIO_getDeviceIntParameter.restype = c_int
        dll.AIO_setDeviceIntParameter.argtypes = [c_int, c_int]
        dll.AIO_setDeviceIntParameter.restype = c_int

        # Windows audio (may not exist on macOS)
        try:
            dll.AIO_getASIOPreferredBufferSize.argtypes = []
            dll.AIO_getASIOPreferredBufferSize.restype = c_int
            dll.AIO_setASIOPreferredBufferSize.argtypes = [c_int]
            dll.AIO_setASIOPreferredBufferSize.restype = c_int
            dll.AIO_getSampleRate.argtypes = []
            dll.AIO_getSampleRate.restype = c_int
            dll.AIO_setSampleRate.argtypes = [c_int]
            dll.AIO_setSampleRate.restype = c_int
            dll.AIO_isWASAPIEnabled.argtypes = []
            dll.AIO_isWASAPIEnabled.restype = c_int
            dll.AIO_setWASAPIEnabled.argtypes = [c_int]
            dll.AIO_setWASAPIEnabled.restype = c_int
            self._has_windows_functions = True
        except AttributeError:
            self._has_windows_functions = False

        # ATS-specific functions
        dll.ATS_writeI2C.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_uint8)]
        dll.ATS_writeI2C.restype = c_int
        dll.ATS_readI2C.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_uint8)]
        dll.ATS_readI2C.restype = c_int
        dll.ATS_getAuxOut.argtypes = [POINTER(c_uint8)]
        dll.ATS_getAuxOut.restype = c_int
        dll.ATS_setAuxOut.argtypes = [c_uint8]
        dll.ATS_setAuxOut.restype = c_int
        dll.ATS_getAuxIn.argtypes = [POINTER(c_uint8)]
        dll.ATS_getAuxIn.restype = c_int
        dll.ATS_getDigitalIOMode.argtypes = [POINTER(c_uint8)]
        dll.ATS_getDigitalIOMode.restype = c_int
        dll.ATS_setDigitalIOMode.argtypes = [c_uint8]
        dll.ATS_setDigitalIOMode.restype = c_int
        dll.ATS_getWordClockTerminated.argtypes = [POINTER(c_int)]
        dll.ATS_getWordClockTerminated.restype = c_int
        dll.ATS_setWordClockTerminated.argtypes = [c_int]
        dll.ATS_setWordClockTerminated.restype = c_int
        dll.ATS_getImpedanceMode.argtypes = [POINTER(c_int)]
        dll.ATS_getImpedanceMode.restype = c_int
        dll.ATS_setImpedanceMode.argtypes = [c_int]
        dll.ATS_setImpedanceMode.restype = c_int
        dll.ATS_getSerialNumber.argtypes = [POINTER(c_uint32)]
        dll.ATS_getSerialNumber.restype = c_int
        dll.ATS_getAnalogInputMode.argtypes = [c_int, POINTER(c_int)]
        dll.ATS_getAnalogInputMode.restype = c_int
        dll.ATS_setAnalogInputMode.argtypes = [c_int, c_int]
        dll.ATS_setAnalogInputMode.restype = c_int
        dll.ATS_getAnalogOutputMode.argtypes = [c_int, POINTER(c_int)]
        dll.ATS_getAnalogOutputMode.restype = c_int
        dll.ATS_setAnalogOutputMode.argtypes = [c_int, c_int]
        dll.ATS_setAnalogOutputMode.restype = c_int

    def _check_initialized(self):
        """Raise exception if API not initialized."""
        if not self._initialized:
            raise RuntimeError("API not initialized. Call initialize() first.")

    def _check_error(self, result: int, operation: str):
        """Check result code and raise exception on error."""
        if result != 0:
            error_msg = self.get_error_string()
            raise RuntimeError(f"{operation} failed (code {result}): {error_msg}")

    # --- Library Management ---

    def initialize(self):
        """Initialize the API library. Must be called first."""
        self._load_dll()
        self._dll.AIO_initialize()
        self._initialized = True

    def shutdown(self):
        """Shutdown the API library."""
        if self._dll and self._initialized:
            self._dll.AIO_shutdown()
            self._initialized = False

    def get_library_version(self) -> str:
        """Get the library version string."""
        self._load_dll()
        buffer = ctypes.create_string_buffer(256)
        self._dll.AIO_getLibraryVersion(buffer, len(buffer))
        return buffer.value.decode('utf-8')

    def get_error_string(self) -> str:
        """Get the last error message."""
        if not self._dll:
            return "DLL not loaded"
        buffer = ctypes.create_string_buffer(1024)
        self._dll.AIO_getErrorString(buffer, len(buffer))
        return buffer.value.decode('utf-8')

    # --- Device Inquiry ---

    def is_aio_connected(self) -> bool:
        """Check if an AIO device is connected."""
        self._check_initialized()
        return bool(self._dll.AIO_isAIOConnected())

    def is_ats_connected(self) -> bool:
        """Check if an ATS device is connected."""
        self._check_initialized()
        return bool(self._dll.AIO_isATSConnected())

    def get_num_inputs(self) -> int:
        """Get the number of input channels."""
        self._check_initialized()
        return self._dll.AIO_getNumInputChannels()

    def get_num_outputs(self) -> int:
        """Get the number of output channels."""
        self._check_initialized()
        return self._dll.AIO_getNumOutputChannels()

    def get_module_type(self, slot: int) -> ModuleType:
        """Get the module type for a slot (0 or 1)."""
        self._check_initialized()
        result = self._dll.AIO_getModuleType(slot)
        try:
            return ModuleType(result)
        except ValueError:
            return ModuleType.UNKNOWN

    def get_device_info(self) -> DeviceInfo:
        """Get comprehensive device information."""
        self._check_initialized()
        return DeviceInfo(
            is_aio_connected=self.is_aio_connected(),
            is_ats_connected=self.is_ats_connected(),
            num_inputs=self.get_num_inputs(),
            num_outputs=self.get_num_outputs(),
            module_slot_0=self.get_module_type(0),
            module_slot_1=self.get_module_type(1),
            library_version=self.get_library_version()
        )

    # --- Input Channel Functions ---

    def has_input_gain_control(self, channel: int) -> bool:
        """Check if input channel has gain control."""
        self._check_initialized()
        return bool(self._dll.AIO_hasInputGainControl(channel))

    def get_input_gain(self, channel: int) -> int:
        """Get input gain for a channel."""
        self._check_initialized()
        gain = c_int()
        result = self._dll.AIO_getInputGain(channel, byref(gain))
        self._check_error(result, f"Get input gain for channel {channel}")
        return gain.value

    def set_input_gain(self, channel: int, gain: int):
        """Set input gain for a channel."""
        self._check_initialized()
        result = self._dll.AIO_setInputGain(channel, gain)
        self._check_error(result, f"Set input gain for channel {channel}")

    def set_input_gain_direct(self, channel: int, gain: int):
        """
        Set input gain using direct multiplier values.

        Args:
            channel: Input channel (0-based)
            gain: Gain multiplier (ATS: 1/3/10/31/100, AIO: 1/10/100)
        """
        self._check_initialized()
        result = self._dll.AIO_setInputGainDirect(channel, gain)
        self._check_error(result, f"Set input gain direct for channel {channel}")

    def has_constant_current_control(self, channel: int) -> bool:
        """Check if input channel has CCP control."""
        self._check_initialized()
        return bool(self._dll.AIO_hasConstantCurrentControl(channel))

    def get_constant_current_state(self, channel: int) -> bool:
        """Get CCP state for a channel."""
        self._check_initialized()
        enabled = c_int()
        result = self._dll.AIO_getConstantCurrentState(channel, byref(enabled))
        self._check_error(result, f"Get CCP state for channel {channel}")
        return bool(enabled.value)

    def set_constant_current_state(self, channel: int, enabled: bool):
        """Set CCP state for a channel."""
        self._check_initialized()
        result = self._dll.AIO_setConstantCurrentState(channel, int(enabled))
        self._check_error(result, f"Set CCP state for channel {channel}")

    def has_teds(self, channel: int) -> bool:
        """Check if input channel supports TEDS."""
        self._check_initialized()
        return bool(self._dll.AIO_hasTEDS(channel))

    def get_teds_properties(self, channel: int) -> str:
        """Get TEDS properties as JSON string."""
        self._check_initialized()
        required_size = c_size_t()
        self._dll.AIO_getTEDSProperties(channel, None, 0, byref(required_size))
        if required_size.value == 0:
            return "{}"
        buffer = ctypes.create_string_buffer(required_size.value + 1)
        result = self._dll.AIO_getTEDSProperties(channel, buffer, len(buffer), byref(required_size))
        self._check_error(result, f"Get TEDS for channel {channel}")
        return buffer.value.decode('utf-8')

    def get_channel_config(self, channel: int) -> ChannelConfig:
        """Get complete configuration for an input channel."""
        self._check_initialized()
        has_gain = self.has_input_gain_control(channel)
        has_ccp = self.has_constant_current_control(channel)
        has_teds = self.has_teds(channel)

        gain = None
        if has_gain:
            try:
                gain = self.get_input_gain(channel)
            except RuntimeError:
                pass

        ccp = None
        if has_ccp:
            try:
                ccp = self.get_constant_current_state(channel)
            except RuntimeError:
                pass

        return ChannelConfig(
            channel=channel,
            has_gain_control=has_gain,
            gain=gain,
            has_ccp_control=has_ccp,
            ccp_enabled=ccp,
            has_teds=has_teds
        )

    # --- Output Channel Functions ---

    def has_output_gain_control(self, channel: int) -> bool:
        """Check if output channel has gain control."""
        self._check_initialized()
        return bool(self._dll.AIO_hasOutputGainControl(channel))

    def get_output_gain(self, channel: int) -> int:
        """Get output gain for a channel (0-255)."""
        self._check_initialized()
        gain = c_int()
        result = self._dll.AIO_getOutputGain(channel, byref(gain))
        self._check_error(result, f"Get output gain for channel {channel}")
        return gain.value

    def set_output_gain(self, channel: int, gain: int):
        """Set output gain for a channel (0-255)."""
        self._check_initialized()
        result = self._dll.AIO_setOutputGain(channel, gain)
        self._check_error(result, f"Set output gain for channel {channel}")

    # --- Module Parameters ---

    def get_module_int_parameter(self, slot: int, parameter: int) -> int:
        """Get an integer parameter for a module."""
        self._check_initialized()
        value = c_int()
        result = self._dll.AIO_getModuleIntParameter(slot, parameter, byref(value))
        self._check_error(result, f"Get module parameter {hex(parameter)}")
        return value.value

    def set_module_int_parameter(self, slot: int, parameter: int, value: int):
        """Set an integer parameter for a module."""
        self._check_initialized()
        result = self._dll.AIO_setModuleIntParameter(slot, parameter, value)
        self._check_error(result, f"Set module parameter {hex(parameter)}")

    def get_module_double_parameter(self, slot: int, parameter: int) -> float:
        """Get a floating-point parameter for a module."""
        self._check_initialized()
        value = c_double()
        result = self._dll.AIO_getModuleDoubleParameter(slot, parameter, byref(value))
        self._check_error(result, f"Get module parameter {hex(parameter)}")
        return value.value

    def set_module_double_parameter(self, slot: int, parameter: int, value: float):
        """Set a floating-point parameter for a module."""
        self._check_initialized()
        result = self._dll.AIO_setModuleDoubleParameter(slot, parameter, value)
        self._check_error(result, f"Set module parameter {hex(parameter)}")

    # --- Device Parameters ---

    def get_device_parameter(self, parameter: int) -> int:
        """Get an integer device parameter."""
        self._check_initialized()
        value = c_int()
        result = self._dll.AIO_getDeviceIntParameter(parameter, byref(value))
        self._check_error(result, f"Get device parameter {hex(parameter)}")
        return value.value

    def set_device_parameter(self, parameter: int, value: int):
        """Set an integer device parameter."""
        self._check_initialized()
        result = self._dll.AIO_setDeviceIntParameter(parameter, value)
        self._check_error(result, f"Set device parameter {hex(parameter)}")

    def get_clock_source(self) -> ClockSource:
        """Get the current clock source."""
        value = self.get_device_parameter(0xd000)
        return ClockSource(value)

    def set_clock_source(self, source: ClockSource):
        """Set the clock source."""
        self.set_device_parameter(0xd000, source.value)

    # --- Windows Audio Functions ---

    def get_asio_buffer_size(self) -> int:
        """Get ASIO buffer size (Windows only)."""
        self._check_initialized()
        if not self._has_windows_functions:
            raise RuntimeError("ASIO functions not available")
        return self._dll.AIO_getASIOPreferredBufferSize()

    def set_asio_buffer_size(self, size: int):
        """Set ASIO buffer size (Windows only)."""
        self._check_initialized()
        if not self._has_windows_functions:
            raise RuntimeError("ASIO functions not available")
        result = self._dll.AIO_setASIOPreferredBufferSize(size)
        self._check_error(result, "Set ASIO buffer size")

    def get_sample_rate(self) -> int:
        """Get sample rate (Windows only)."""
        self._check_initialized()
        if not self._has_windows_functions:
            raise RuntimeError("Sample rate functions not available")
        return self._dll.AIO_getSampleRate()

    def set_sample_rate(self, rate: int):
        """Set sample rate (Windows only)."""
        self._check_initialized()
        if not self._has_windows_functions:
            raise RuntimeError("Sample rate functions not available")
        result = self._dll.AIO_setSampleRate(rate)
        self._check_error(result, "Set sample rate")

    # --- ATS-Specific Functions ---

    def ats_get_serial_number(self) -> int:
        """Get ATS device serial number."""
        self._check_initialized()
        serial = c_uint32()
        result = self._dll.ATS_getSerialNumber(byref(serial))
        self._check_error(result, "Get ATS serial number")
        return serial.value

    def ats_get_aux_out(self) -> int:
        """Get AUX output state (4-bit)."""
        self._check_initialized()
        bits = c_uint8()
        result = self._dll.ATS_getAuxOut(byref(bits))
        self._check_error(result, "Get AUX out")
        return bits.value

    def ats_set_aux_out(self, bits: int):
        """Set AUX output state (4-bit, 0-15)."""
        self._check_initialized()
        result = self._dll.ATS_setAuxOut(c_uint8(bits & 0x0F))
        self._check_error(result, "Set AUX out")

    def ats_get_aux_in(self) -> int:
        """Get AUX input state (4-bit)."""
        self._check_initialized()
        bits = c_uint8()
        result = self._dll.ATS_getAuxIn(byref(bits))
        self._check_error(result, "Get AUX in")
        return bits.value

    def ats_get_digital_io_mode(self) -> int:
        """Get digital I/O mode (0=S/PDIF, 1=Word Clock)."""
        self._check_initialized()
        mode = c_uint8()
        result = self._dll.ATS_getDigitalIOMode(byref(mode))
        self._check_error(result, "Get digital I/O mode")
        return mode.value

    def ats_set_digital_io_mode(self, mode: int):
        """Set digital I/O mode (0=S/PDIF, 1=Word Clock)."""
        self._check_initialized()
        result = self._dll.ATS_setDigitalIOMode(c_uint8(mode))
        self._check_error(result, "Set digital I/O mode")

    def ats_get_word_clock_terminated(self) -> bool:
        """Check if word clock termination is enabled."""
        self._check_initialized()
        terminated = c_int()
        result = self._dll.ATS_getWordClockTerminated(byref(terminated))
        self._check_error(result, "Get word clock terminated")
        return bool(terminated.value)

    def ats_set_word_clock_terminated(self, terminated: bool):
        """Enable/disable word clock termination."""
        self._check_initialized()
        result = self._dll.ATS_setWordClockTerminated(int(terminated))
        self._check_error(result, "Set word clock terminated")

    def ats_get_impedance_mode(self) -> bool:
        """Check if impedance mode is enabled."""
        self._check_initialized()
        enabled = c_int()
        result = self._dll.ATS_getImpedanceMode(byref(enabled))
        self._check_error(result, "Get impedance mode")
        return bool(enabled.value)

    def ats_set_impedance_mode(self, enabled: bool):
        """Enable/disable impedance mode."""
        self._check_initialized()
        result = self._dll.ATS_setImpedanceMode(int(enabled))
        self._check_error(result, "Set impedance mode")

    def ats_get_analog_input_mode(self, channel: int) -> int:
        """Get analog input mode (0=Loopback, 1=Analog)."""
        self._check_initialized()
        mode = c_int()
        result = self._dll.ATS_getAnalogInputMode(channel, byref(mode))
        self._check_error(result, f"Get analog input mode for channel {channel}")
        return mode.value

    def ats_set_analog_input_mode(self, channel: int, mode: int):
        """Set analog input mode (0=Loopback, 1=Analog)."""
        self._check_initialized()
        result = self._dll.ATS_setAnalogInputMode(channel, mode)
        self._check_error(result, f"Set analog input mode for channel {channel}")

    def ats_get_analog_output_mode(self, channel: int) -> int:
        """Get analog output mode (0=Line, 1=Amp, 2=Headphone)."""
        self._check_initialized()
        mode = c_int()
        result = self._dll.ATS_getAnalogOutputMode(channel, byref(mode))
        self._check_error(result, f"Get analog output mode for channel {channel}")
        return mode.value

    def ats_set_analog_output_mode(self, channel: int, mode: int):
        """Set analog output mode (0=Line, 1=Amp, 2=Headphone)."""
        self._check_initialized()
        result = self._dll.ATS_setAnalogOutputMode(channel, mode)
        self._check_error(result, f"Set analog output mode for channel {channel}")

    def ats_write_i2c(self, sda_select: int, i2c_address: int,
                      register_address: int, register_length: int, data: int):
        """Write data via I2C."""
        self._check_initialized()
        data_byte = (c_uint8 * 1)(data)
        result = self._dll.ATS_writeI2C(sda_select, i2c_address, register_address,
                                        register_length, data_byte)
        self._check_error(result, "I2C write")

    def ats_read_i2c(self, sda_select: int, i2c_address: int,
                     register_address: int, register_length: int) -> int:
        """Read data via I2C."""
        self._check_initialized()
        data_byte = (c_uint8 * 1)()
        result = self._dll.ATS_readI2C(sda_select, i2c_address, register_address,
                                       register_length, data_byte)
        self._check_error(result, "I2C read")
        return data_byte[0]


# Convenience context manager
class EchoAPIContext:
    """
    Context manager for EchoAPI.

    Usage:
        with EchoAPIContext() as api:
            info = api.get_device_info()
            print(info)
    """

    def __init__(self, dll_path: Optional[Path] = None):
        self.api = EchoAPI(dll_path)

    def __enter__(self) -> EchoAPI:
        self.api.initialize()
        return self.api

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api.shutdown()


# Quick test when run directly
if __name__ == "__main__":
    print(f"Looking for library at: {DEFAULT_DLL_PATH}")
    print(f"Library exists: {DEFAULT_DLL_PATH.exists()}")

    if DEFAULT_DLL_PATH.exists():
        with EchoAPIContext() as api:
            print(f"\nLibrary version: {api.get_library_version()}")
            print(f"AIO connected: {api.is_aio_connected()}")
            print(f"ATS connected: {api.is_ats_connected()}")

            if api.is_aio_connected() or api.is_ats_connected():
                info = api.get_device_info()
                print(f"\nDevice Info:")
                print(f"  Inputs: {info.num_inputs}")
                print(f"  Outputs: {info.num_outputs}")
                print(f"  Slot 0: {info.module_slot_0.name}")
                print(f"  Slot 1: {info.module_slot_1.name}")
