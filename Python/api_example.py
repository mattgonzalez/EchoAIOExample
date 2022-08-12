import ctypes

#
#    For EchoAIO API documentation see: EchoAIOInterface.h
#

#
#    Change the following path to the location of EchoAIOInterface.dll.
#    The default location is C:\Progam Files\Echo AIO\CLI + API\EchoAIOInterface.dll
#
path = 'C:\Program Files\Echo AIO\CLI + API\EchoAIOInterface.dll'
echoaio = ctypes.WinDLL(path)

#
#    Call AIO_initiatlize() before  calling any other function to set up the library.
#
echoaio.AIO_initialize()


#
#    AIO_setInputGain
#
#    Parameters
#        inputChannel    Input channel number, starting at 0
#        gain            Gain value (1, 10, or 100)
#
#    Returns 0 if successful
#
inputChannel = 2  # MIC3
gain = 100        # 100X Gain
if (echoaio.AIO_setInputGain(inputChannel, gain) == 0):
    print("Input channel " + str(inputChannel + 1) + " gain set to " + str(gain))
else:
    print("Unable to set input channel " + str(inputChannel + 1) + " gain to " + str(gain))

#
#    AIO_setConstantCurrentState
#
#    Parameters
#        inputChannel    Input channel number, starting at 0
#        enabled         0 to disable the constant current power, 1 to enable
#
#    Returns 0 if successful
#
inputChannel = 1  # MIC2
enabled = 1       # Enable constant current power
if (echoaio.AIO_setConstantCurrentState(inputChannel, enabled) == 0):
    print("Input channel " + str(inputChannel + 1) + " CCP enabled")
else:
    print("Unable to enable CCP on input channel " + str(inputChannel + 1))

#
#    AIO_getSampleRate
#
#    Returns the current sample rate in Hz
#
if (echoaio.AIO_getSampleRate()):
    print("Sample rate is: " + str(echoaio.AIO_getSampleRate()))
else:
    print("Unable to get sample rate")


#
#    Call AIO_shutdown() before unloading the library to release memory and resources
#
echoaio.AIO_shutdown()


