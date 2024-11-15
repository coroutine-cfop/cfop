#include <coroutine>
#include <iostream>
#include <atomic>
#include <vector>
#include <Windows.h>

class AClass
{
public:
    //All of this is any data used by the application, might be anything.
    //The only requirement is that these are variables belonging to a class
    long long randomData[14];
    long long data1;
    long long data2;
    long long data3;
    long long data4;
    long long data5;
    
    AClass(){
        for (int ii = 0; ii < 14; ii++) {
            randomData[ii] = rand() % 100;
        }
        data1 = (rand() % 100)>>16;
        data2 = rand() % 100;
        data3 = rand() % 100;
        data4 = rand() % 100;
        data5 = rand() % 100;
    }

    bool __declspec(noinline, dllexport) silverGadgetFunction()
    {
        //A sample function that plays with the registers in such a way that it replicates a Silver Gadget
        long long var1 = this->data1;
        long long var2 = this->data2;
        long long var3 = this->data3;
        long long var4 = this->data4;
        long long var5 = this->data5;

        if (var1 < var2 && var2 > var3 && var4 > var3 && var5 > var3 && var1 + var2 + var3 + var4 + var5 > 38)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
};

class task
{
public:
    class promise_type
    {
    public:
        task get_return_object() noexcept
        {
            return task{ std::coroutine_handle<promise_type>::from_promise(*this) };
        }

        std::suspend_always initial_suspend() noexcept
        {
            return {};
        }

        void return_void() noexcept {}

        void unhandled_exception() noexcept
        {
            std::terminate();
        }

        struct final_awaiter
        {
            bool await_ready() noexcept
            {
                return false;
            }
            std::coroutine_handle<> await_suspend(std::coroutine_handle<promise_type> h) noexcept
            {
                if (h.promise().continuation) {
                    return h.promise().continuation;
                }

                return std::noop_coroutine();
            }
            void await_resume() noexcept{}

        };

        final_awaiter final_suspend() noexcept
        {
            return {};
        }

        std::coroutine_handle<> continuation;
    };

    task(task&& t) noexcept
        : coro_(std::exchange(t.coro_, {})) {}

    ~task()
    {
        if (coro_)
        {
            coro_.destroy();
        }
    }

    void start() noexcept { coro_.resume(); }
    void finalize() noexcept { coro_.destroy(); }

    class awaiter
    {
    public:
        bool await_ready() noexcept
        {
            return false;
        }

        std::coroutine_handle<> await_suspend(std::coroutine_handle<> continuation) noexcept
        {
            coro_.promise().continuation = continuation;
            return coro_;
        }

        void await_resume() noexcept {}

        explicit awaiter(std::coroutine_handle<task::promise_type> h) noexcept
            : coro_(h) {}

        std::coroutine_handle<task::promise_type> coro_;
    };

    awaiter operator co_await() && noexcept
    {
        return awaiter{ coro_ };
    }

    explicit task(std::coroutine_handle<promise_type> h) noexcept
        : coro_(h) {}

    std::coroutine_handle<promise_type> coro_;

};

void __declspec(noinline) printParameters(long long param1, long long param2, long long param3, long long param4)
{
    std::cout << std::hex << "param1:" << param1 << " param2:" << param2 << " param3:" << param3 << " param4:" << param4 << std::dec << std::endl;
}

task c3()
{
    std::cout << "starting c3()" << std::endl;
    //
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
    //This is just one sample function called indirectly. Not necessary for an exploitation, this is just for the PoC.
    //This pointer is NOT hijacked, this is just to showcase how parameters can be set whilst bypassing Control Flow Guard
    void (*functionPtr)(long long, long long, long long, long long) = printParameters;

    //This is some buffer that, when it overflows, can overwrite the coroutine frames (or the handler, in this case)
    //It does not necessarily need to overflow here; e.g., could happen during the coroutine execution
    char vuln_buf[0x30];

    //Create the coroutine (configured to suspend once created)
    task h = c1();
    
    //These memory leaks are specific to this PoC -- you don't necessarily need to leak the handler address,
    //you may write into the coroutine frames directly
    std::cout << "Handler address: " << (void*)&h << std::endl;
    bool(__thiscall AClass:: * pFunc)() = &AClass::silverGadgetFunction;
    std::cout << "Silver gadget: " << (void*&)pFunc << std::endl;
    std::cout << "WinExec address: " << (void*)WinExec << std::endl;
    std::cout << "PrintParameters function: " << (void*)&printParameters << std::endl;

    std::cout << "Welcome to the CFOP PoC. Introduce some input!" << std::endl;

    //A buffer overflow vulnerability
    std::cin.getline(vuln_buf, 1000);
    
    functionPtr(1, 2, 3, 4);

    //Resume the coroutine for the first time
    h.start();

    return 0;
}
