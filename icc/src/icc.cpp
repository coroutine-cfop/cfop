#include <coroutine>
#include <iostream>

class task
{
public:
    class promise_type
    {
    public:
        task get_return_object() noexcept
        {
            return task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_always initial_suspend() noexcept
        {
            return {};
        }

        void return_void() noexcept{}

        void unhandled_exception() noexcept {std::terminate();}

        struct final_awaiter
        {
            bool await_ready() noexcept {return false;};
            std::coroutine_handle<> await_suspend(std::coroutine_handle<promise_type> h) noexcept
            {
                promise_type& promise = h.promise();
                if(promise.continuation){
                    return promise.continuation;
                }

                return std::noop_coroutine();
            }
            void await_resume() noexcept {};
        };

        final_awaiter final_suspend() noexcept {return {};};

        std::coroutine_handle<> continuation;
    };

    task(task &&t) noexcept
        : coro_(std::__exchange(t.coro_, {})){}

    ~task()
    {
        // std::cout<<"calling destroy on task()"<<std::endl;
        if (coro_)
        {
            coro_.destroy();
        }
    }

    void start() noexcept { coro_.resume(); };
    void finalize() noexcept { coro_.destroy(); };

    class awaiter
    {
    public:
        bool await_ready() noexcept {return false;};

        std::coroutine_handle<> await_suspend(std::coroutine_handle<> continuation) noexcept
        {
            task::promise_type& promise = coro_.promise();
            promise.continuation = continuation;
            return coro_;
        }

        void await_resume() noexcept {};

    private:
        friend task;
        explicit awaiter(std::coroutine_handle<task::promise_type> h) noexcept
            : coro_(h){}

        std::coroutine_handle<task::promise_type> coro_;
    };

    awaiter operator co_await() && noexcept
    {
        return awaiter{coro_};
    }

private:
    explicit task(std::coroutine_handle<promise_type> h) noexcept
        : coro_(h){}

    std::coroutine_handle<promise_type> coro_;
};

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
    void* vuln_buf = malloc(10);
    task t = c1();
    std::cin.getline((char*)vuln_buf, 2000);
    t.start();
    std::cout << "ending coros" << std::endl;
    return 0;
}