#include <coroutine>
#include <utility>
#include <iostream>
#include <atomic>
#include <cstring>
#include <vector>

namespace std::experimental
{
  using namespace std;
};

using namespace std;

int mult(int a, int b){return a*b;}

void afunction()
{
  //std::cout<<"hello from afunction"<<std::endl;
  printf("hello from afunction\n");
}

class task {
public:
  class promise_type {
  public:
    task get_return_object() noexcept {
      return task{coroutine_handle<promise_type>::from_promise(*this)};
    }

    suspend_never initial_suspend() noexcept {
        //std::cout << "task initial_suspend" << std::endl;
        return {};
    }

    void return_void() noexcept {}

    void unhandled_exception() noexcept {
      std::__terminate();
    }

    struct final_awaiter {
      bool await_ready() noexcept {
        //std::cout << "task final_awaiter await_ready" << std::endl;
        return false;
      }
      void await_suspend(coroutine_handle<promise_type> h) noexcept {
        //std::cout << "task final_awaiter await_suspend" << std::endl;
      }
      void await_resume() noexcept {
        //std::cout << "task final_awaiter await_resume" << std::endl;
      }
    };

    final_awaiter final_suspend() noexcept {
        //std::cout << "task final_awaiter final_suspend" << std::endl;
        return {};
    }

  };

  task(task&& t) noexcept
  : coro_(__exchange(t.coro_, {}))
  {}

  ~task() {
    //std::cout<<"calling destroy on task()"<<std::endl;
    if (coro_){
      coro_.destroy();
    }
    //std::cout<<"called destroy on task()"<<std::endl;
  }

  void start() noexcept { coro_.resume(); }

  class awaiter {
  public:
    bool await_ready() noexcept {
        //std::cout << "awaiter await_ready" << std::endl;
        return false;
    }

    bool await_suspend(coroutine_handle<> continuation) noexcept {
      //std::cout << "awaiter await_suspend" << std::endl;
      //coro_.promise().continuation = continuation;
      //std::cout << "Value: " << intvalue <<std::endl;
      //printf("Value: %d\n", intvalue);
      // resume awaiting coroutine(caller) if current completed synchronously
      //return !std::__exchange(coro_.promise().ready, true);
      return false;
    }

    void await_resume() noexcept {
        //std::cout << "awaiter await_resume" << std::endl;
    }
  private:
    friend task;
    explicit awaiter(coroutine_handle<promise_type> h) noexcept
    : coro_(h)
    {}

    coroutine_handle<promise_type> coro_;
    //int intvalue = 2;
  };

  awaiter operator co_await() && noexcept {
    //std::cout << "awaiter co_await()" << std::endl;
    return awaiter{coro_};
  }

private:
  explicit task(coroutine_handle<promise_type> h) noexcept
  : coro_(h)
  {}

  coroutine_handle<promise_type> coro_;
};

task c4(){
    printf("coroutine c4\n");
    co_return;
}

task c3(){
    char* buf1 = (char*)malloc(10);
    char* buf2 = (char*)malloc(10);
    printf("coroutine c3\n");
    for(int ii=0; ii<3; ii++){
        co_await c4();
    }
    free(buf1);
    free(buf2);
}

task c2() {
    printf("coroutine c2\n");
    co_return;
}

task c1() {
    char* vulnerableBuffer = (char*)malloc(10);
    printf("coroutine c1\n");
    std::cin.read(vulnerableBuffer, 1);
    /*void* buf1 = (void*)malloc(0x10);
    std::memset(buf1, 'A', 0x10);
    void* buf2 = (void*)malloc(0x10);
    std::memset(buf2, 'B', 0x10);*/
    vector<int> vec1 = {1,2};
    vector<int> vec2 = {3,4};
    for(int ii=0; ii<3; ii++)
    {
      co_await c2();
    }
    co_return;
}

int main() {
    std::cout << "coroutine initialized" << std::endl;
    c1();
    //c3();
    std::cout << "coroutine finalized" << std::endl;
    system("echo 'Hi! :D'");
    return 0;
}
