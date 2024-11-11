#include <coroutine>
#include <iostream>
#include <atomic>
#include <vector>

#include "contjumping.h"

task task::promise_type::get_return_object() noexcept
{
    return task{std::coroutine_handle<promise_type>::from_promise(*this)};
}

std::suspend_always task::promise_type::initial_suspend() noexcept
{
    // std::cout << "task initial_suspend" << std::endl;
    return {};
}

void task::promise_type::return_void() noexcept {}

void task::promise_type::unhandled_exception() noexcept
{
    std::terminate();
}

bool task::promise_type::final_awaiter::await_ready() noexcept
{
    // std::cout << "task final_awaiter await_ready" << std::endl;
    return false;
}

std::coroutine_handle<> task::promise_type::final_awaiter::await_suspend(std::coroutine_handle<task::promise_type> h) noexcept
{
    //std::cout << "final_awaiter await_suspend" << std::endl;
    if(h.promise().continuation){
        return h.promise().continuation;
    }

    return std::noop_coroutine();
}

void task::promise_type::final_awaiter::await_resume() noexcept
{
    // std::cout << "task final_awaiter await_resume" << std::endl;
}

task::promise_type::final_awaiter task::promise_type::final_suspend() noexcept
{
    // std::cout << "task final_awaiter final_suspend" << std::endl;
    return {};
}

void task::start() noexcept { coro_.resume(); }
void task::finalize() noexcept { coro_.destroy(); }

bool task::awaiter::await_ready() noexcept
{
    // std::cout << "awaiter await_ready" << std::endl;
    return false;
}

std::coroutine_handle<> task::awaiter::await_suspend(std::coroutine_handle<> continuation) noexcept
{
    //std::cout << "awaiter await_suspend: " << (void*)continuation.address() << std::endl;
    coro_.promise().continuation = continuation;
    return coro_;
}

void task::awaiter::await_resume() noexcept
{
    // std::cout << "awaiter await_resume" << std::endl;
}

std::coroutine_handle<task::promise_type> coro_;