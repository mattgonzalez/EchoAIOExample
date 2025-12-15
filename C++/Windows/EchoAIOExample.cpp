/*
    Echo API Example - Windows C++

    This example demonstrates how to load and use EchoAPI.dll
    to control Echo AIO and ATS devices.

    See docs/getting-started.md for installation instructions.
    See docs/api-reference.md for complete API documentation.
*/

#include <iostream>
#include <Windows.h>
#include "../../EchoAIOInterface.h"

// Default installation path for Echo API
const wchar_t* ECHO_API_PATH = L"C:\\Program Files\\Echo Test Interfaces\\EchoAPI.dll";

// Function pointer types
using AIO_initialize_t = void (*)();
using AIO_shutdown_t = void (*)();
using AIO_getLibraryVersion_t = void (*)(char*, size_t);
using AIO_isAIOConnected_t = int (*)();
using AIO_isATSConnected_t = int (*)();
using AIO_getNumInputChannels_t = int (*)();
using AIO_getNumOutputChannels_t = int (*)();
using AIO_getInputGain_t = int (*)(int, int* const);
using AIO_setInputGainDirect_t = int (*)(int, int);
using AIO_hasInputGainControl_t = int (*)(int);

void libraryAccessDemo(HMODULE handle)
{
    // Get function pointers
    auto AIO_initialize = (AIO_initialize_t)GetProcAddress(handle, "AIO_initialize");
    auto AIO_shutdown = (AIO_shutdown_t)GetProcAddress(handle, "AIO_shutdown");
    auto AIO_getLibraryVersion = (AIO_getLibraryVersion_t)GetProcAddress(handle, "AIO_getLibraryVersion");
    auto AIO_isAIOConnected = (AIO_isAIOConnected_t)GetProcAddress(handle, "AIO_isAIOConnected");
    auto AIO_isATSConnected = (AIO_isATSConnected_t)GetProcAddress(handle, "AIO_isATSConnected");
    auto AIO_getNumInputChannels = (AIO_getNumInputChannels_t)GetProcAddress(handle, "AIO_getNumInputChannels");
    auto AIO_getNumOutputChannels = (AIO_getNumOutputChannels_t)GetProcAddress(handle, "AIO_getNumOutputChannels");
    auto AIO_getInputGain = (AIO_getInputGain_t)GetProcAddress(handle, "AIO_getInputGain");
    auto AIO_setInputGainDirect = (AIO_setInputGainDirect_t)GetProcAddress(handle, "AIO_setInputGainDirect");
    auto AIO_hasInputGainControl = (AIO_hasInputGainControl_t)GetProcAddress(handle, "AIO_hasInputGainControl");

    if (!AIO_initialize)
    {
        std::cout << "Unable to find AIO_initialize function\n";
        return;
    }

    //
    // Always call AIO_initialize first
    //
    AIO_initialize();

    // Get library version
    char version[256];
    AIO_getLibraryVersion(version, sizeof(version));
    std::cout << "Echo API version: " << version << "\n";

    // Check for connected devices
    if (AIO_isATSConnected())
    {
        std::cout << "Device: Echo ATS\n";
    }
    else if (AIO_isAIOConnected())
    {
        std::cout << "Device: Echo AIO\n";
    }
    else
    {
        std::cout << "No device connected\n";
        AIO_shutdown();
        return;
    }

    // Get channel counts
    int numInputs = AIO_getNumInputChannels();
    int numOutputs = AIO_getNumOutputChannels();
    std::cout << "Input channels: " << numInputs << "\n";
    std::cout << "Output channels: " << numOutputs << "\n";

    //
    // Read the input gain setting for channel 0
    //
    int inputChannel = 0;
    if (AIO_hasInputGainControl(inputChannel))
    {
        int gain = 0;
        int status = AIO_getInputGain(inputChannel, &gain);
        if (ECHO_AIO_OK == status)
        {
            std::cout << "Channel " << inputChannel << " gain: " << gain << "x\n";

            // Example: Set gain to 10x
            status = AIO_setInputGainDirect(inputChannel, 10);
            if (ECHO_AIO_OK == status)
            {
                AIO_getInputGain(inputChannel, &gain);
                std::cout << "Set channel " << inputChannel << " gain to: " << gain << "x\n";
            }
        }
        else
        {
            std::cout << "Unable to read input gain; error " << status << "\n";
        }
    }
    else
    {
        std::cout << "Channel " << inputChannel << " does not have gain control\n";
    }

    //
    // Always call AIO_shutdown before unloading the DLL
    //
    AIO_shutdown();
}

int main()
{
    std::cout << "===========================================\n";
    std::cout << "Echo API Example - Windows C++\n";
    std::cout << "===========================================\n\n";

    //
    // Load the DLL from the default installation path
    //
    auto handle = LoadLibraryW(ECHO_API_PATH);
    if (nullptr == handle)
    {
        std::cout << "Unable to load EchoAPI.dll\n";
        std::cout << "Expected path: C:\\Program Files\\Echo Test Interfaces\\EchoAPI.dll\n";
        std::cout << "Please verify the Echo Control Panel is installed.\n";
        return 1;
    }

    std::cout << "Loaded: EchoAPI.dll\n\n";

    //
    // Access the DLL
    //
    libraryAccessDemo(handle);

    //
    // Unload the DLL
    //
    FreeLibrary(handle);

    std::cout << "\nExample complete.\n";
    return 0;
}
