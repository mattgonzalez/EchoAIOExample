
import ctypes
import EchoAIOInterface

#
#    Change the following path to the location of EchoAIOInterface.dll.
#    The default location is C:/Progam Files/Echo AIO/CLI + API/EchoAIOInterface.dll
#
path = 'C:\Program Files\Echo AIO\CLI + API\EchoAIOInterface.dll'
echoaio = ctypes.WinDLL(path)

#
#    Call AIO_initiatlize() before  calling any other function to set up the library.
# 
echoaio.AIO_initialize.restype = None
echoaio.AIO_initialize()

#
# Set the AUX_OUT pins
#
slot = 1
value = 0x55
status = echoaio.AIO_setModuleIntParameter(slot, EchoAIOInterface.AIO_COMBO_MODULE_PARAMETER_AUX_OUT, value)
print("AIO_setModuleIntParameter for AIO_COMBO_MODULE_PARAMETER_AUX_OUT   status:" + str(status) + " value:" + hex(value))

#
# Read back the AUX_OUT value
#
auxOutCheckValue = ctypes.c_int(0)
status = echoaio.AIO_getModuleIntParameter(slot, EchoAIOInterface.AIO_COMBO_MODULE_PARAMETER_AUX_OUT, ctypes.byref(auxOutCheckValue))
print("AIO_getModuleIntParameter for AIO_COMBO_MODULE_PARAMETER_AUX_OUT   status:" + str(status) + " value:" + hex(auxOutCheckValue.value))

#
# Read the AUX_IN value
#
auxInValue = ctypes.c_int(0)
status = echoaio.AIO_getModuleIntParameter(slot, EchoAIOInterface.AIO_COMBO_MODULE_PARAMETER_AUX_IN, ctypes.byref(auxOutCheckValue))
print("AIO_getModuleIntParameter for AIO_COMBO_MODULE_PARAMETER_AUX_IN    status:" + str(status) + " value:" + hex(auxOutCheckValue.value))

#
#    Call AIO_shutdown() before unloading the library to release memory and resources
#
echoaio.AIO_shutdown.restype = None
echoaio.AIO_shutdown()
