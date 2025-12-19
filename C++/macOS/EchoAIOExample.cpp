/*
    Echo API Example - macOS C++

    This example demonstrates how to load and use libEchoAPI.dylib
    to control Echo AIO and ATS devices.

    See docs/getting-started.md for installation instructions.
    See docs/api-reference.md for complete API documentation.
*/

#include <iostream>
#include <dlfcn.h>
#include "../../EchoAIOInterface.h"

// Default path for Echo API - copy libEchoAPI.dylib from the Echo Control Panel DMG to your project directory
const char* ECHO_API_PATH = "./libEchoAPI.dylib";

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

void libraryAccessDemo(void* handle)
{
    // Get function pointers
    auto AIO_initialize = reinterpret_cast<AIO_initialize_t>(dlsym(handle, "AIO_initialize"));
    auto AIO_shutdown = reinterpret_cast<AIO_shutdown_t>(dlsym(handle, "AIO_shutdown"));
    auto AIO_getLibraryVersion = reinterpret_cast<AIO_getLibraryVersion_t>(dlsym(handle, "AIO_getLibraryVersion"));
    auto AIO_isAIOConnected = reinterpret_cast<AIO_isAIOConnected_t>(dlsym(handle, "AIO_isAIOConnected"));
    auto AIO_isATSConnected = reinterpret_cast<AIO_isATSConnected_t>(dlsym(handle, "AIO_isATSConnected"));
    auto AIO_getNumInputChannels = reinterpret_cast<AIO_getNumInputChannels_t>(dlsym(handle, "AIO_getNumInputChannels"));
    auto AIO_getNumOutputChannels = reinterpret_cast<AIO_getNumOutputChannels_t>(dlsym(handle, "AIO_getNumOutputChannels"));
    auto AIO_getInputGain = reinterpret_cast<AIO_getInputGain_t>(dlsym(handle, "AIO_getInputGain"));
    auto AIO_setInputGainDirect = reinterpret_cast<AIO_setInputGainDirect_t>(dlsym(handle, "AIO_setInputGainDirect"));
    auto AIO_hasInputGainControl = reinterpret_cast<AIO_hasInputGainControl_t>(dlsym(handle, "AIO_hasInputGainControl"));

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
    // Always call AIO_shutdown before unloading the library
    //
    AIO_shutdown();
}

int main(int /*argc*/, const char * /*argv*/ [])
{
    std::cout << "===========================================\n";
    std::cout << "Echo API Example - macOS C++\n";
    std::cout << "===========================================\n\n";

    //
    // Load the dynamic library from the default installation path
    //
    auto handle = dlopen(ECHO_API_PATH, RTLD_LOCAL | RTLD_NOW);
    if (nullptr == handle)
    {
        std::cout << "Unable to load libEchoAPI.dylib\n";
        std::cout << "Expected path: " << ECHO_API_PATH << "\n";
        std::cout << "Copy libEchoAPI.dylib from the Echo Control Panel DMG to your project directory.\n";
        std::cout << "Error: " << dlerror() << "\n";
        return 1;
    }

    std::cout << "Loaded: libEchoAPI.dylib\n\n";

    //
    // Access the dynamic library
    //
    libraryAccessDemo(handle);

    //
    // Unload the dynamic library
    //
    dlclose(handle);

    std::cout << "\nExample complete.\n";
    return 0;
}
