#include <coroutine>
#include <iostream>
#include <atomic>
#include <vector>
#include <unistd.h>

#include "bashtest.h"

class AClass
{
    public: 
    long randomStuff1;
    long randomStuff2;
    long randomStuff3;
    long randomStuff4;
    long randomStuff5;
    long randomStuff6;
    long randomStuff7;
    long randomStuff8;
    long randomStuff9;
    long randomStuff10;
    long randomStuff11;
    long randomStuff12;
    long randomStuff13;
    long randomStuff14;
    long data1;
    long data2;
    long data3;

    AClass(int _data1, int _data2, int _data3) : data1(_data1), data2(_data2), data3(_data3)
    {
        randomStuff1 = rand() % 100;
        randomStuff2 = rand() % 100;
        randomStuff3 = rand() % 100;
        randomStuff4 = rand() % 100;
        randomStuff5 = rand() % 100;
        randomStuff6 = rand() % 100;
        randomStuff7 = rand() % 100;
        randomStuff8 = rand() % 100;
        randomStuff9 = rand() % 100;
        randomStuff10 = rand() % 100;
        randomStuff11 = rand() % 100;
        randomStuff12 = rand() % 100;
        randomStuff13 = rand() % 100;
        randomStuff14 = rand() % 100;
    }

    float hiddenFunction(int a, int b, int c)
    {   
        system("whoami");
        return (float)(a*5+b*3+c*3);
    }

    float __attribute__((noinline)) argumentsFunction(int a, int b, int c)
    {
        this->data1 = a;
        this->data2 = b;
        this->data3 = c;
        std::cout << "inside argumentsFunction()" << std::endl;
        //float val = hiddenFunction(data1, data2, data3);
        return this->data1 < this->data2;
    }

    bool __attribute__((noinline)) simpleArgumentsFunction(int number)
    {
        /*this->data1 = this->randomStuff6;
        this->data2 = this->randomStuff7;
        this->data3 = this->randomStuff8;
        int results = this->data1 * this->data2 * this->data3;
        if(this->data2 > this->randomStuff1 && this->data3 > this->randomStuff2 && results > 500)
        {
            return false;
        }
        return true;*/

        long var1 = this->data1;
        long var2 = this->data2 + 50;
        long var3 = this->data3;

        if(var1 < var2  && var2 > var3 && var1 > 30 && var2 > 40 && var3 > 50)
        {
            return false;
        }
        else
        {
            return true;
        }
    }

    float superConvenientFunction()
    {
        std::cout << "inside superConvenientFunction()" << std::endl;
        //return (float)(data1*5+data2*3+data3*3);
        return -1;
    }
};



task lol(int param1, int param2, int param3, void* vuln_buf)
{
    AClass ac(rand() % 100, rand() % 100, rand() % 100);
    std::cout << "inside lol()" << std::endl; 
    std::cin.getline((char*)vuln_buf, 2000);
    std::cout << "lol() params: " << param1+param2+param3 << std::endl;
    //std::cout << "ac: " << ac.argumentsFunction(3, 4, 5) << std::endl;
    //co_await std::suspend_always{};
    std::cout << "ac: " << ac.simpleArgumentsFunction(3) << std::endl;
    co_return;
}

task foo(void* vuln_buf)
{
    std::cout << "starting foo()" << std::endl;
    co_await lol(6, 7, 8, vuln_buf);
    std::cout << "ending foo()" << std::endl;
    co_return;
}

task bar(void* vuln_buf)
{
    std::cout << "in bar(), about to call foo()" << std::endl;
    co_await foo(vuln_buf);
    //std::cout << "bar: " << vuln_ptr << std::endl;
    std::cout << "in bar(), done calling foo()" << std::endl;
    co_return;
}

void func()
{
    void* vuln_buf = malloc(10);
    std::cout << "coroutine initialized" << std::endl;
    task h = bar(vuln_buf);
    h.start();
    h.finalize();
    std::cout << "coroutine finalized" << std::endl;
    std::cout << "vuln_buf: " << vuln_buf << std::endl;
}

int main()
{
    func();
    //char* arg[] ={(char*)"/bin/sh" ,(char*)"-c", (char*)"/usr/bin/whoami", (char*)0};
    //execve(arg[0], arg, NULL);
    return 0;
}
