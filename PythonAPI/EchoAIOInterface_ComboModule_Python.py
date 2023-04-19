'''
  ==============================================================================

    EchoAIOInterface library exports for AIO-C module

    Copyright (c) 2023 - Echo Digital Audio Corporation

  ==============================================================================
'''

import ctypes

#
# AIO Combo Module Int Parameters
#
class AIOComboModuleIntParameters(ctypes.c_int):
    AIO_comboParameterFirmwareVersion = 0xc0000
    AIO_comboParameterSerialNumber = 0xc0001
    AIO_comboParameterAuxout = 0xc0002
    AIO_comboParameterAuxIn = 0xc0003
    AIO_comboParameter5VDCEnable = 0xc0004
    AIO_comboParameterVariableDCPowerEnable = 0xc0005
    AIO_comboParameterVariableDCPowerOutputMillivolts = 0xc0006
    AIO_comboParameterVariableDCPowerMeasuredMillivolts = 0xc0007
    AIO_comboParameterVariableDCPowerMeasuredAmperes = 0xc0008
    AIO_comboParameterMeasuredCurrentRange = 0xc0009
    AIO_comboParameterOverCurrentThresholdAmperes = 0xc000a
    AIO_comboParameterOverCurrentCondition = 0xc000b
#
# AIO Combo Module Defines
#
class AIOComboModuleDefines(ctypes.c_int):
    AIO_comboParameterOverCurrentCondition = 600
    AIO_comboVariableDCMaximumAmperes = 5000
    AIO_comboVariableDCMaximumCurrentMicroamps = 1280000
    AIO_comboVariableDCMinimumCurrentMicroamps = 250
#
# AIO Combo Module Double Parameters
#
class AIOComboModuleDoubleParameters(ctypes.c_int):
    AIO_comboParameterVariableDCPowerMeasuredAmperes = 0
    AIO_comboParameterOverCurrentThresholdAmperes = 1
#
# AIO Combo Module Current Measurement Ranges
#
class AIOComboCurrentMeasurementRanges(ctypes.c_int):
    AIO_comboCurrentMeasurementRange_250uA = 0
    AIO_comboCurrentMeasurementRange_1250uA = 1
    AIO_comboCurrentMeasurementRange_250mA = 2
    AIO_comboCurrentMeasurementRange_1250mA = 3