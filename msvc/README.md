# CFOP: Coroutine Frame-Oriented Programming -- MSVC PoC
This README details how to run our Coroutine Frame-Oriented Programming (CFOP) PoC.
This PoC demonstrates one of the main techniques under CFOP: how to achieve arbitrary code execution exploiting coroutines (calling arbitrary functions with arbitrary arguments).

Note: this is a minimal reproducible example with a single arbitrary call, but it is possible to create exploits with an infinite number of arbitrary calls too.

## PoC Explanation
The program ```msvc_cfop_poc.exe``` is a very simple program using nested coroutines.
This program features one buffer that can be overflown via a buffer overflow vulnerability. This overflow overwrites critical coroutine data (the coroutine handle, and injects new coroutine frames), which we exploit for our attack. 

We provide two scripts ```msvc_call_exploit.py``` and ```msvc_silver_exploit.py``` that showcase two different aspects of arbitrary code execution. In both of them, we make use of multiple hijacked ```resume``` and ```destroy``` pointers, together with other coroutine frame objects, to achieve code reuse.

In ```msvc_call_exploit.py```, we show how the program execution may be hijacked to call an arbitrary function (```WinExec```). For this, we hijack the coroutine handle and inject a series of counterfeit coroutine frames referenced by it (it is also possible, and usually easier, to just overwrite existing coroutine frames). Using the hijacked ```resume``` and ```destroy``` pointers, we call our arbitrary function. The expected result of the exploit is that the calculator program (```calc.exe```) gets executed. 

In ```msvc_silver_exploit.py``` we showcase how a _silver gadget_ can be used to set arbitrary values to registers, which are then used in an arbitrary call. In this case,we also hijack the coroutine handle and inject a series of counterfeit coroutine frames; and make use of internal ```resume```, ```destroy``` and other internal coroutine objects to set the needed register values according to the call convention (that are then printed calling ```printParameters()```). As indicated in our paper, the four first parameters can always be set in MSVC-compiled programs (although the first parameter is restricted to be a pointer to a controlled memory value). The expected result of the exploit is that the parameters values are printed on screen with clearly arbitrary values (e.g., 0x4242424242424242)

Note: the exploited program is just an example. The coroutine program does not necessarily need to feature three nested coroutines for an exploit to exist, and does not necessarily need to be using symmetric transfer (asymmetric is also vulnerable). All versions of MSVC which support coroutines are vulnerable, here we target the latest. We recommend reading Section 3 of our paper for complete detail of every possible attack.

## Building and Running
In order to test the PoCs, we provide an already compiled program ```msvc_cfop_poc.exe```, along with the source code of this (a complete Visual Studio solution).
The program was compiled using MSVC 19.39.33523

The Visual Studio solution can be consulted for all the relevant compilation settings.
* CET Shadow Stack Compatible: Yes (/CETCOMPAT) -- this technique bypasses SS
* Maximum optimization (favor speed): /O2
* Disabled Security Check /GS- : just for the sample buffer overflow
* Control Flow Guard: (/guard:cf) -- this technique bypasses CFG
* ISO C++20 Standard: (/std:c++20)
* Randomized Base Address: (/DYNAMICBASE:NO): just to ease the exploit, but otherwise is also possible

We recommend using our exploit scripts to run the program. We prepared them in such a way that a debugger (e.g., WinDbg) can be attached. Thus, in order to run the PoC, you should follow the next steps:
1. (Optional) Import the ```msvc_cfop_poc``` Visual Studio project and build it using the _PoC_ build configuration. If any issue arises, we also incorporate our already compiled program under ```x64/PoC/```.
2. Run the first PoC ```msvc_silver_exploit.py```. Only if necessary, update the path where the _.exe_ file is located in line 10 of the script.
```msvc_silver_exploit.py```
3. Run the first PoC ```msvc_silver_exploit.py```. Only if necessary, update the path where the _.exe_ file is located in line 10 of the script.


