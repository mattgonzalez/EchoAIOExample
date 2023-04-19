'''
  ==============================================================================

    EchoAIOInterface library exports for AIO-T module

    Copyright (c) 2023 - Echo Digital Audio Corporation

  ==============================================================================
'''
# \defgroup AIO-T AIO-T Module
# \brief Python API for AIO-T Module

# @{
# \code{.py}



import ctypes

#
# AIO TDM Module CLock Modes
#
class AIOTClockModes(ctypes.c_int):
    AIO_tdmClockSourceMode = 0
    AIO_tdmClockSinkMode = 1
#
# AIO TDM Module Parameters
#
class AIOTModuleParameters(ctypes.c_int):
    AIO_tdmParameterFirmwareVersion = 0xd000
    AIO_tdmParameterBitsPerWord = 0xd001
    AIO_tdmParameterBitsPerFrame = 0xd002
    AIO_tdmParameterFSYNCPhaseDelay = 0xd003
    AIO_tdmParameterInvertSCLK = 0xd004
    AIO_tdmParameterAudioDataShiftEnabled = 0xd005
    AIO_tdmParameterClockMode = 0xd006
    AIO_tdmParameterAudioDataShiftBits = 0xd007
    AIO_tdmParameterLogicLevel = 0xd008
    AIO_tdmParameterFSYNCPosition = 0xd009
    AIO_tdmParameterFSYNCWidth = 0xd00a
# \endcode
# }@