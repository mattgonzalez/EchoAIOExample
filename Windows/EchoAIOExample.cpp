#include <iostream>
#include <Windows.h>
#include "../EchoAIOInterface.h"

void libraryAccessDemo(HMODULE handle)
{
    //
    // Always call AIO_initialize first
    //
    auto pAIO_initialize = GetProcAddress(handle, "AIO_initialize");
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
    auto pAIO_getInputGain = reinterpret_cast<AIO_getInputGainPointer>(GetProcAddress(handle, "AIO_getInputGain"));
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
    if (auto pAIO_shutdown = GetProcAddress(handle, "AIO_shutdown"))
    {
        pAIO_shutdown();
    }
    else
    {
        std::cout << "Unable to find AIO_shutdown function";
    }
}

int main()
{
    //
    // Load the DLL
    // 
    auto handle = LoadLibrary(L"c:/aio/EchoAIOInterface.dll");
    if (nullptr == handle)
    {
        std::cout << "Unable to load Echo AIO library";
        return 0;
    }

    //
    // Access the DLL
    //
    libraryAccessDemo(handle);
    
    //
    // Unload the DLL
    //
    FreeLibrary(handle);
}
