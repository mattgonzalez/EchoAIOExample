'''
  ==============================================================================

    EchoAIOInterface library exports

    Copyright (c) 2023 - Echo Digital Audio Corporation

  ==============================================================================
'''
import ctypes

#
#  AIO Module Types
#
class AIO_moduleType(ctypes.c_int):
    AIO_moduleTypeUnkown = -1
    AIO_moduleTypeNone = 0
    AIO_moduleTypeA = 1
    AIO_moduleTypeS = 2
    AIO_moduleTypeL = 3
    AIO_moduleTypeC = 4
    AIO_moduleTypeH = 5
    AIO_moduleTypeT = 6
    AIO_moduleTypeB = 7

#
# AIO Error Codes
#
class AIO_errorCodes(ctypes.c_int):
    AIO_OK = 0
    AIO_notInitialized = -1
    AIO_invalidInputChannel = -2
    AIO_invalidOutputChannel = -3
    AIO_invalidParameter = -4
    AIO_invalidBufferSize = -5
    AIO_notFound = -6
    AIO_usbCommandFailed = -7
    AIO_invalidModuleSlot = -8
    AIO_notSupported = -9
    AIO_tedsDeviceNotFound = -10
    AIO_invalidValue = -11
    AIO_missingParameter = -12
    AIO_timeout = -13

AIO_notificationString =  "Echo AIO control change"

AIO_numModuleSlots = ctypes.c_int(2)
