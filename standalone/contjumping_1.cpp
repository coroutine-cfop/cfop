#include <coroutine>
#include <iostream>
#include "contjumping.h"

using namespace std;

void afunction(){
  std::cout << "called arbitrary function!" << std::endl;
}

task c5() {
    std::cout << "c5" << std::endl;
    co_return;
}

task c4() {
    std::cout << "c4" << std::endl;
    co_await c5();
    co_return;
}

task c3() {
    std::cout << "c3" << std::endl;
    co_await c4();
    co_return;
}

task c2() {
    std::cout << "c2" << std::endl;
    co_await c3();
    co_return;
}

task c1() {
    std::cout << "c1" << std::endl;
    co_await c2();
    co_return;
}

int main() {
    std::cout << "starting coros" << std::endl;
    //long* ptr = (long*)0x555555558058;
    //*ptr = (char)0xAAAAAAAAAAA;
    void* vuln_buf = malloc(10);
    task t = c1();
    std::cin.getline((char*)vuln_buf, 2000);
    t.start();
    afunction();
    std::cout << "ending coros" << std::endl;
    return 0;
}
//clang++-18 -g -O3 contjumping_1.cpp contjumping_2.cpp -std=c++20 -o contjumping -fcf-protection=full -Wl,-z,relro -fPIE