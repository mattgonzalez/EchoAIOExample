'''
  ==============================================================================

    EchoAIOInterface library exports for AIO-H module

    Copyright (c) 2023 - Echo Digital Audio Corporation

  ==============================================================================
'''

import ctypes

#
# AIO Headphone Module Parameters
#
class AIOHeadphoneModuleParameters(ctypes.c_int):
    AIO_headphoneParameterImpedanceSelect = 0xe0000
#
# AIO Headphone Impedance Channel
#
class AIOHeadphoneImpedanceChannel(ctypes.c_int):
    AIO_headphoneImpedanceChannelLeft = 1
    AIO_headphoneImpedanceChannelRight = 2