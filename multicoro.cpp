#include <coroutine>
#include <iostream>
#include <atomic>
#include <vector>

using namespace std;

class task {
public:
  class promise_type {
  public:
    task get_return_object() noexcept {
      return task{coroutine_handle<promise_type>::from_promise(*this)};
    }

    suspend_always initial_suspend() noexcept {
        //std::cout << "task initial_suspend" << std::endl;
        return {};
    }

    void return_void() noexcept {}

    void unhandled_exception() noexcept {
      std::terminate();
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
  : coro_(std::__exchange(t.coro_, {}))
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
      coro_.resume();
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

task foo() {
    std::cout << "inside foo()" << std::endl;
    co_return;
}

task bar() {
    for(int ii=0; ii<3; ii++)
    {
      std::cout << "in bar(), about to call foo()" << std::endl;
      co_await foo();
      std::cout << "in bar(), done calling foo()" << std::endl;
    }
    co_return;
}

int main() {
    char* vulnerableBuffer = (char*)malloc(10);
    task t = bar();
    std::cout << "Reading user input into insecure buffer (10 bytes)\n";
    std::cout << "coroutine initialized" <<std::endl;
    t.start();
    std::cout << "coroutine finalized" << std::endl;
    system("echo 'Hi! :D'");
    return 0;
}
