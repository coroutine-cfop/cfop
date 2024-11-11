#include <coroutine>
#include <iostream>
#include <unistd.h>
#include <string.h>

#include "gccpoc.h"

class AClass
{
    public: 
    //All of this is any data used by the application, might be anything.
    //The only requirement is that these are variables belonging to a class
    long randomData[16];
    long data1;
    long data2;
    long data3;

    bool __attribute__((used, noinline)) silverGadgetFunction()
    {
        //A sample function that plays with the registers in such a way that it replicates a Silver Gadget
        long var1 = this->data1;
        long var2 = this->data2;
        long var3 = this->data3;

        if(var1 < var3  && var3 > var2 && var1 > 40 && var2 < 40 && var3 < 50)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
};



task c3()
{
    std::cout << "starting c3()" << std::endl;
    //This is some buffer that, when it overflows, can overwrite the coroutine frames
    void* vuln_buf = malloc(10);
    //A buffer overflow vulnerability
    std::cin.getline((char*)vuln_buf, 2000);
    std::cout << "ending c3()" << std::endl;
    co_return;
}

task c2()
{
    std::cout << "starting c2()" << std::endl;
    co_await c3();
    std::cout << "ending c2()" << std::endl;
    co_return;
}

task c1()
{
    std::cout << "starting c1()" << std::endl;
    co_await c2();
    std::cout << "ending c1()" << std::endl;
    co_return;
}

int main()
{
    //Some memory buffer that will be overflown later in c3().
    //For this PoC, we put it into the tcache so that it is right before the coroutine frame in the heap.
    //This is just an example, a vulnerable buffer could appear in many forms.
    void* some_buf = malloc(10);
    //Ensure all of this is not optimized by the compiler (in a real secenario, this buffer is used somehow)
    asm volatile("" :: "r"(some_buf) : "memory");
    free((void*)some_buf);

    std::cout << "starting coroutine chain" << std::endl;
    //Create the coroutine (configured to suspend once created)
    task h = c1();
    //Resume the coroutine for the first time
    h.start();
    return 0;
}
