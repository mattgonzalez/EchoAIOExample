#include <iostream>
#include <dlfcn.h>
#include "../EchoAIOInterface.h"

void libraryAccessDemo(void* handle)
{
    //
    // Always call AIO_initialize first
    //
    using AIO_initializePointer = void (*)();
    auto pAIO_initialize = reinterpret_cast<AIO_initializePointer>(dlsym(handle, "AIO_initialize"));
    if (pAIO_initialize)
    {
        pAIO_initialize();
    }
    else
    {
        std::cout << "Unable to find AIO_initialize function";
        return;
    }

    //
    // Read the input gain setting
    //
    using AIO_getInputGainPointer = int (*)(int, int* const);

    int inputChannel = 0; // MIC1
    auto pAIO_getInputGain = reinterpret_cast<AIO_getInputGainPointer>(dlsym(handle, "AIO_getInputGain"));
    if (pAIO_getInputGain)
    {
        int gain = 0;
        int status = pAIO_getInputGain(inputChannel, &gain);
        if (ECHO_AIO_OK == status)
        {
            std::cout << "Input channel " << inputChannel + 1 << " gain is " << gain;
        }
        else
        {
            std::cout << "Unable to read input gain; error " << status;
        }
    }
    else
    {
        std::cout << "Unable to find AIO_getInputGain function";
    }

    //
    // Always call AIO_shutdown before unloading the DLL
    //
    using AIO_shutdownPointer = void (*)();
    if (auto pAIO_shutdown = reinterpret_cast<AIO_shutdownPointer>(dlsym(handle, "AIO_shutdown")))
    {
        pAIO_shutdown();
    }
    else
    {
        std::cout << "Unable to find AIO_shutdown function";
    }
}

int main(int /*argc*/, const char * /*argv*/ [])
{
    //
    // Load the dynamic library; assume the library is in the same folder as this app
    //
    auto handle = dlopen("EchoAIOInterface.dylib", RTLD_LOCAL | RTLD_NOW);
    if (nullptr == handle)
    {
        std::cout << "Unable to load Echo AIO library";
        return 0;
    }

    //
    // Access the dynamic library
    //
    libraryAccessDemo(handle);
    
    //
    // Unload the dynamic library
    //
    dlclose(handle);
    
    return 0;
}
