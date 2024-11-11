#include <coroutine>
#include <iostream>

#include "gccpoc.h"

task task::promise_type::get_return_object() noexcept
{
    return task{std::coroutine_handle<promise_type>::from_promise(*this)};
}

std::suspend_always task::promise_type::initial_suspend() noexcept
{
    return {};
}

void task::promise_type::return_void() noexcept {}

void task::promise_type::unhandled_exception() noexcept
{
    std::terminate();
}

bool task::promise_type::final_awaiter::await_ready() noexcept
{
    return false;
}

std::coroutine_handle<> task::promise_type::final_awaiter::await_suspend(std::coroutine_handle<task::promise_type> h) noexcept
{
    if(h.promise().continuation){
        return h.promise().continuation;
    }

    return std::noop_coroutine();
}

void task::promise_type::final_awaiter::await_resume() noexcept
{}

task::promise_type::final_awaiter task::promise_type::final_suspend() noexcept
{
    return {};
}

void task::start() noexcept { coro_.resume(); }
void task::finalize() noexcept { coro_.destroy(); }

bool task::awaiter::await_ready() noexcept
{
    return false;
}

std::coroutine_handle<> task::awaiter::await_suspend(std::coroutine_handle<> continuation) noexcept
{
    coro_.promise().continuation = continuation;
    return coro_;
}

void task::awaiter::await_resume() noexcept
{}

std::coroutine_handle<task::promise_type> coro_;