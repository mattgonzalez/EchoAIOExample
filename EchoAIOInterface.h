/*
  ==============================================================================

    EchoAIOInterface library exports

    Copyright (c) 2022 - Echo Digital Audio Corporation

  ==============================================================================
*/

#if _WIN32
#if ECHO_AIO_EXPORTS
#define ECHO_AIO_API __declspec(dllexport)
#else
#define ECHO_AIO_API __declspec(dllimport)
#endif
#endif

#ifdef __APPLE__
#if ECHO_AIO_EXPORTS
#define ECHO_AIO_API __attribute__((visibility("default")))
#else
#define ECHO_AIO_API
#endif
#endif



/*-----------------------------------------------------------------------------------------------------------------
 *
 * Return codes
 *
 *---------------------------------------------------------------------------------------------------------------*/

#define ECHO_AIO_OK 0
#define ECHO_AIO_NOT_INITIALIZED 1
#define ECHO_AIO_INVALID_INPUT_CHANNEL 2
#define ECHO_AIO_INVALID_OUTPUT_CHANNEL 3
#define ECHO_AIO_INVALID_PARAMETER 4
#define ECHO_AIO_INVALID_TEDS_SIZE 5
#define ECHO_AIO_NOT_FOUND 6
#define ECHO_AIO_USB_COMMAND_FAILED 7
#define ECHO_AIO_INVALID_MODULE_SLOT 8
#define ECHO_AIO_BUFFER_TOO_SMALL 9
#define ECHO_AIO_NOT_SUPPORTED 10
#define ECHO_AIO_TEDS_DEVICE_NOT_FOUND 11
#define ECHO_AIO_INVALID_VALUE 12

#ifdef __cplusplus
extern "C"
{
#endif

    /*-----------------------------------------------------------------------------------------------------------------
     *
     * Library startup and shutdown
     *
     *---------------------------------------------------------------------------------------------------------------*/

    /*
        AIO_initialize
        AIO_shutdown

		Call AIO_initialize before calling any other library functions to set up the library
		Call AIO_shutdown before unloading the library to release memory and resources

    */
    ECHO_AIO_API void AIO_initialize();
    ECHO_AIO_API void AIO_shutdown();


    /*-----------------------------------------------------------------------------------------------------------------
     *
     * Inquiry functions
     *
     *---------------------------------------------------------------------------------------------------------------*/

    /*
        AIO_getLibraryVersion

        Parameters
            text                    Pointer to the buffer to receive the zero-terminated UTF-8 encoded string
            textBufferBytes         Length of the buffer in bytes

    */
    ECHO_AIO_API void AIO_getLibraryVersion(char* const text, size_t textBufferBytes);

    /*
        AIO_isAIOConnected

        Returns true if an AIO is connected
    */
    ECHO_AIO_API int AIO_isAIOConnected();

    /*
        AIO_getNumInputChannels

        Returns the total number of input channels for the AIO
    */
    ECHO_AIO_API int AIO_getNumInputChannels();

    /*
        AIO_getNumOutputChannels

        Returns the total number of output channels for the AIO
    */
    ECHO_AIO_API int AIO_getNumOutputChannels();

    /*
        AIO_isComboModulePresent

        Parameter
            moduleSlot      0 for center audio module slot, 1 for outer audio module slot

        Returns true if an AIO is connected and if the AIO has an AIO-C module in the specified slot
    */
    ECHO_AIO_API int AIO_hasComboModule(int moduleSlot);
    
    /*
    	AIO_isTModulePresent

    	Parameter
        	moduleSlot      0 for center audio module slot, 1 for outer audio module slot

    	Returns true if an AIO is connected and if the AIO has an AIO-T module in the specified slot
    */
    ECHO_AIO_API int AIO_hasTModule(int moduleSlot);

    /*
    AIO_getErrorString

    Parameters
        text                    Pointer to the buffer to receive the zero-terminated UTF-8 encoded string
        textBufferBytes         Length of the buffer in bytes

    */
    ECHO_AIO_API void AIO_getErrorString(char* const text, size_t textBufferBytes);


    /*-----------------------------------------------------------------------------------------------------------------
     *
     * IEPE microphone inputs
     *
     *---------------------------------------------------------------------------------------------------------------*/

    /*
        AIO_hasInputGainControl

        Parameter
            inputChannel    Input channel number, starting at 0

        Returns true if inputChannel has an input gain control
    */
    ECHO_AIO_API int AIO_hasInputGainControl(int inputChannel);

    /*
        AIO_getInputGain

        Parameters
            inputChannel    Input channel number, starting at 0
            gain            Pointer to the variable to receive the gain value

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_getInputGain(int inputChannel, int* const gain);

    /*
        AIO_setInputGain

        Parameters
            inputChannel    Input channel number, starting at 0
            gain            Gain value (1, 10, or 100)

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setInputGain(int inputChannel, int gain);


    /*
        AIO_hasConstantCurrentControl

        Parameter
            inputChannel    Input channel number, starting at 0

        Returns true if inputChannel has a constant current power supply
    */
    ECHO_AIO_API int AIO_hasConstantCurrentControl(int inputChannel);

    /*
        AIO_getConstantCurrentState

        Parameters
            inputChannel    Input channel number, starting at 0
            enabled         Pointer to the variable to receive the constant current power setting

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_getConstantCurrentState(int inputChannel, int* const enabled);

    /*
        AIO_setConstantCurrentState

        Parameters
            inputChannel    Input channel number, starting at 0
            enabled         0 to disable the constant current power, 1 to enable

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setConstantCurrentState(int inputChannel, int enabled);


    /*
        AIO_hasTEDS

        Parameter
            inputChannel    Input channel number, starting at 0

        Returns true if inputChannel can read TEDS data
    */
    ECHO_AIO_API int AIO_hasTEDS(int inputChannel);


    /*

        AIO_getTEDSProperties

        Read and parse TEDS data from a specific microphone input; then, write TEDS properties to the specified buffer as JSON-formatted text.

        Parameters
            inputChannel        Input channel number, starting at 0
            jsonText            Points to a buffer to receive the JSON-formatted text
            jsonBufferBytes     Length of the JSON text buffer in bytes
            jsonBytesRequired   Points to a value to receive the number of bytes needed for the JSON text buffer

        Both jsonText and jsonBytesRequired are optional parameters.

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_getTEDSProperties(int inputChannel, char* const jsonText, size_t jsonBufferBytes, size_t* jsonBytesRequired);



    /*-----------------------------------------------------------------------------------------------------------------
     *
     * AMP outputs
     *
     *---------------------------------------------------------------------------------------------------------------*/

     /*
        AIO_hasOutputGainControl

        Output gain control is deprecated but still supported for backwards compatibility.

        Parameter
            outputChannel    Output channel number, starting at 0

        Returns true if outputChannel has an output gain control
    */
    ECHO_AIO_API int AIO_hasOutputGainControl(int outputChannel);

    /*
        AIO_getOutputGain

        Output gain control is deprecated but still supported for backwards compatibility.

        Parameters
            outputChannel   Output channel number, starting at 0
            gain            Pointer to the variable to receive the gain value

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_getOutputGain(int outputChannel, int* const gain);

    /*
        AIO_setOutputGain

        Output gain control is deprecated but still supported for backwards compatibility.

        Parameters
            outputChannel   Output channel number, starting at 0
            gain            Gain value
     
        Gain values range from 0 to 255.
            To match the 10x setting on the console, set the gain value to 255
            For the 1x console setting, set the gain value to 26

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setOutputGain(int outputChannel, int gain);

    /*
       AIO_hasOutputLimitControl

       Parameter
           outputChannel    Output channel number, starting at 0

       Returns true if outputChannel has an output limit control
    */
    ECHO_AIO_API int AIO_hasOutputLimitControl(int outputChannel);

    /*
        AIO_getOutputLimitVolts

        Parameters
            outputChannel   Output channel number, starting at 0
            limitVolts      Pointer to the variable to receive the limit value in volts

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_getOutputLimitVolts(int outputChannel, double* const limitVolts);

    /*
        AIO_setOutputLimitVolts

        Parameters
            outputChannel   Output channel number, starting at 0
            limitVolts      Limit value in volts

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setOutputLimitVolts(int outputChannel, double limitVolts);


    /*-----------------------------------------------------------------------------------------------------------------
     *
     * Windows audio driver
     *
     *---------------------------------------------------------------------------------------------------------------*/

#if _WIN32
    /*
        AIO_getASIOPreferredBufferSize

        Returns the ASIO driver preferred buffer size in samples

    */
    ECHO_AIO_API int AIO_getASIOPreferredBufferSize();

    /*
        AIO_setASIOPreferredBufferSize

        Parameter
            bufferSize              Preferred buffer size in samples

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setASIOPreferredBufferSize(int bufferSize);

    /*
        AIO_getSampleRate

        Returns the current sample rate in Hz

    */
    ECHO_AIO_API int AIO_getSampleRate();

    /*
        AIO_setSampleRate

        Parameter
            sampleRate              Sample rate in Hz

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setSampleRate(int sampleRate);
#endif


    /*-----------------------------------------------------------------------------------------------------------------
     *
     * Module parameters
     *
     *---------------------------------------------------------------------------------------------------------------*/

    /*
        AIO-C module parameters

        AIO_COMBO_MODULE_PARAMETER_FIRMWARE_VERSION
        Read-only integer parameter for the AIO-C module firmware version; reads -1 on error.

        AIO_COMBO_MODULE_PARAMETER_SERIAL_NUMBER
        Read-only integer parameter for the AIO-C module serial number; reads -1 on error

        AIO_COMBO_MODULE_PARAMETER_AUX_OUT
        Integer parameter for the AIO-C AUX OUT pins; bits 0-7 of the value are a bit mask corresponding to the
        state of the AUX OUT pins. 

        AIO_COMBO_MODULE_PARAMETER_AUX_IN
        Read-only integer parameter for the AIO-C AUX IN pins; bits 0-7 of the value are a bit mask corresponding to the
        state of the AUX IN pins.

        AIO_COMBO_MODULE_PARAMETER_5VDC_ENABLE
        Integer parameter to enable or disable the 5 VDC power supply; 0 to disable, 1 to enable

        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_ENABLE
        Integer parameter to enable or disable the variable DC power supply; 0 to disable, 1 to enable

        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_TARGET_MILLIVOLTS
        Integer parameter to set the target voltage in millivolts for the variable DC power supply, from 600 mV to 5000 mV.

        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_MILLIVOLTS
        Read-only integer parameter for the actual measured voltage for the variable DC power supply

        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_CURRENT
        Read-only double precision floating point parameter for the measured output current in amperes for the variable DC power supply.

        AIO_COMBO_MODULE_PARAMETER_MEASURED_CURRENT_RANGE
        Integer parameter to set the variable power supply current measurement range; must be one of the AIO_COMBO_MODULE_CURRENT_MEASUREMENT
        constants (see below)

        AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_SENSE_ENABLE
        Integer parameter to enable or disable over current sensing for the variable DC power supply; 0 to disable, 1 to enable

        AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_THRESHOLD
        Double precision floating point parameter for the over current threshold in amperes; note that the value range for this parameter is determined by the
        measured current range.

        AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_CONDITION
        Integer parameter for over current condition; if this parameter value reads as true, then then AIO-C module has detected an over current condition.
        Set this parameter to zero to clear the over current condition.
    */

    /*
        AIO_T_MODULE_PARAMETER_FIRMWARE_VERSION
        Read-only integer parameter for the AIO-T module firmware version; reads -1 on error.
        
        AIO_T_MODULE_PARAMETER_CLOCK_SINK
        Integer parameter for the AIO-T module clock sink; 0 to disable, 1 to enable.
        
        AIO_T_MODULE_PARAMETER_BITS_PER_FRAME
        Sets the number of bits per TDM Frame; 01 - 64 bits/frame(not implemented), 10 - 128 bits/frame(not implemented), 11 - 256 bits/frame.
        
        AIO_T_MODULE_PARAMETER_BITS_PER_WORD
        Sets the number of bits per TDM Word; 01 - 24 bits/word, 10 - 32 bits/word.
        
        AIO_T_MODULE_PARAMETER_INVERT_SCLK
        Integer parameter to invert the SCLK signal; 0 - to Data and FSYNC clocks out on the falling edge of SCLK, 1 - Data and FSYNC clocks out on the rising edge of SCLK.
        
        AIO_T_MODULE_PARAMETER_SHIFT_ENABLED
        [Clock source mode] Integer parameter that delays the sampling of input SHIFT bits; 0 - TDM input sampling is aligned with TDM input, 1 - TDM output is advanced "SHIFT" bits adead of the TDM input.
        [Clock sink mode] Integer parameter that enables SCLK output on BNC connector(Only valid for versions prior to 2.01. Must be set for versions 2.01 thru 2.0e, ignored for 2.0f and above)
        0 - TDM output is aligned with TDM input, 1 - TDM output is advanced "SHIFT" bits ahead of the TDM input.
        
        AIO_T_MODULE_PARAMETER_AUDIO_DATA_SHIFT_BITS,
        Integer parameter that set the number of bits to delay INPUT (clock source mode) or advance OUTPUT (clock sink mode) when SHIFT_EN is set. (7 max, 0 is interpreted as 1 for backward compatibility)
        
        AIO_T_MODULE_PARAMETER_FSYNC_PHASE_DELAY,
        [Clock source mode] Integer parameter that determines whether FSYNC clocks out along with data or is delayed by 1/2 SCLK cycle; 0 - FSYNC clocks out along with data, 1 - FSYNC is delayed by 1/2 SCLK cycle
        [Clock sink mode] Integer parameter that determines whether INPUT is delayed by 1/2 SLCK cycle; 0 - INPUT is sampled normally, 1 - INPUT sampling is delayed by 1/2 SCLK cycle

        AIO_T_MODULE_PARAMETER_FSYNC_START_POSISTION,
        8 Bit parameter that sets the position for start of positive portion of FSYNC. Valid positions are 0

        AIO_T_MODULE_PARAMETER_FSYNC_FRAME_WIDTH
        8 bit integer parameter that sets the bit position for the start of positive portion of FSYNC. Valid positions are 0 (first data bit position) through frame length - 1
        [clock source mode] bit 0 corresponds to the MSB of TDM output. [clock sink mode] bit 0 corresponds to the MSB of TDM input
    */

    enum AIOComboModuleParameters
    {
        AIO_COMBO_MODULE_PARAMETER_FIRMWARE_VERSION = 0xc0000,
        AIO_COMBO_MODULE_PARAMETER_SERIAL_NUMBER,
        AIO_COMBO_MODULE_PARAMETER_AUX_OUT,
        AIO_COMBO_MODULE_PARAMETER_AUX_IN,
        AIO_COMBO_MODULE_PARAMETER_5VDC_ENABLE,
        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_ENABLE,
        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_TARGET_MILLIVOLTS,
        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_MILLIVOLTS,
        AIO_COMBO_MODULE_PARAMETER_VARIABLE_DC_POWER_MEASURED_CURRENT,
        AIO_COMBO_MODULE_PARAMETER_MEASURED_CURRENT_RANGE,
        AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_THRESHOLD,
        AIO_COMBO_MODULE_PARAMETER_OVER_CURRENT_CONDITION
    };

    enum AIOTModuleParameters
    {
        AIO_T_MODULE_PARAMETER_FIRMWARE_VERSION = 0xd000,
        AIO_T_MODULE_PARAMETER_BITS_PER_WORD,
        AIO_T_MODULE_PARAMETER_BITS_PER_FRAME,
        AIO_T_MODULE_PARAMETER_FSYNC_PHASE_DELAY,
        AIO_T_MODULE_PARAMETER_INVERT_SCLK,
        AIO_T_MODULE_PARAMETER_SHIFT_ENABLED,
        AIO_T_MODULE_PARAMETER_CLOCK_SINK,
        AIO_T_MODULE_PARAMETER_AUDIO_DATA_SHIFT_BITS,
        AIO_T_MODULE_PARAMETER_LOGIC_LEVEL,
        AIO_T_MODULE_PARAMETER_FSYNC_POSITION,
        AIO_T_MODULE_PARAMETER_FSYNC_WIDTH
    };

    enum AIOComboCurrentMeasurementRanges
    {
        AIO_COMBO_MODULE_CURRENT_MEASUREMENT_250UA = 0, // 0 to 256 microamps
        AIO_COMBO_MODULE_CURRENT_MEASUREMENT_1250UA,    // 0 to 1280 microamps
        AIO_COMBO_MODULE_CURRENT_MEASUREMENT_250MA,     // 0 to 256 milliamps
        AIO_COMBO_MODULE_CURRENT_MEASUREMENT_1250MA,    // 0 to 1280 milliamps
    };

    /*
         AIO_getModuleIntParameter

         Parameters
             moduleSlot     0 for center audio module slot, 1 for outer audio module slot
             parameter      Parameter number (e.g. AIO_COMBO_MODULE_PARAMETER_AUX_OUT)
             value          Pointer to the integer variable to receive the parameter value

         Returns 0 if successful
     */
    ECHO_AIO_API int AIO_getModuleIntParameter(int moduleSlot, int parameter, int* const value);

    /*
        AIO_setModuleIntParameter

        Parameters
            moduleSlot     0 for center audio module slot, 1 for outer audio module slot
            parameter      Parameter number (e.g. AIO_COMBO_MODULE_PARAMETER_AUX_OUT)
            value          Integer parameter value

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setModuleIntParameter(int moduleSlot, int parameter, int value);
 
    /*
         AIO_getModuleDoubleParameter

         Parameters
             moduleSlot     0 for center audio module slot, 1 for outer audio module slot
             parameter      Parameter number (e.g. AIO_COMBO_MODULE_PARAMETER_AUX_OUT)
             value          Pointer to the double-precision floating point variable to receive the parameter value

         Returns 0 if successful
     */
    ECHO_AIO_API int AIO_getModuleDoubleParameter(int moduleSlot, int parameter, double* const value);

    /*
        AIO_setModuleDoubleParameter

        Parameters
            moduleSlot     0 for center audio module slot, 1 for outer audio module slot
            parameter      Parameter number (e.g. AIO_COMBO_MODULE_PARAMETER_AUX_OUT)
            value          Double-precision floating point value

        Returns 0 if successful
    */
    ECHO_AIO_API int AIO_setModuleDoubleParameter(int moduleSlot, int parameter, double value);

    /*
     	AIO_updateTDM

     	Parameters
        	moduleSlot     0 for center audio module slot, 1 for outer audio module slot

     	Returns 0 if successful
 	*/
    ECHO_AIO_API int AIO_updateTDM(int moduleSlot);


    /*-----------------------------------------------------------------------------------------------------------------
     *
     * Constants
     *
     *---------------------------------------------------------------------------------------------------------------*/
     
    /*
    
        String for control changed broadcast event

    */
    static const char AIO_notificationString[] = "Echo AIO control change";

    /*
    
        Number of AIO module slots

    */
    static const int AIO_numModuleSlots = 2;

#ifdef __cplusplus
}
#endif
