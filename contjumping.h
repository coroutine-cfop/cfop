#ifndef _NOHALOHOTSTART2_H_
#define _NOHALOHOTSTART2_H_

class task
{
public:
    class promise_type
    {
    public:
        task get_return_object() noexcept;

        std::suspend_always initial_suspend() noexcept;

        void return_void() noexcept;

        void unhandled_exception() noexcept;

        struct final_awaiter
        {
            bool await_ready() noexcept;
            std::coroutine_handle<> await_suspend(std::coroutine_handle<promise_type> h) noexcept;
            void await_resume() noexcept;
        };

        final_awaiter final_suspend() noexcept;

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

    void start() noexcept;
    void finalize() noexcept;

    class awaiter
    {
    public:
        bool await_ready() noexcept;

        std::coroutine_handle<> /*__attribute__ ((noinline))*/ await_suspend(std::coroutine_handle<> continuation) noexcept;

        void await_resume() noexcept;

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


#endif