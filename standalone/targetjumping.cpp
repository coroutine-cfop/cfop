#include <concepts>
#include <coroutine>
#include <exception>
#include <iostream>
#include <fstream>
#include <cstring>

struct ReturnObject
{
	struct promise_type
	{
		std::string value_;
		ReturnObject get_return_object()
		{
			return {
				.h_ = std::coroutine_handle<promise_type>::from_promise(*this)
			};
		}
		std::suspend_never initial_suspend() { return {}; }
		std::suspend_never final_suspend() noexcept { return {}; }
		void unhandled_exception() {}
		std::suspend_always yield_value(std::string value) {
			value_ = value;
			return {};
		}
	};

	std::coroutine_handle<promise_type> h_;
	operator std::coroutine_handle<promise_type>() const { return h_; }
	operator std::coroutine_handle<>() const { return h_; }
};

ReturnObject readAFileCoro(std::string filename)
{
	std::string userInput;
	std::ifstream file(filename);
	for (unsigned i = 0;; ++i)
	{
		std::cout << "Reading user input from coroutine (one line)" << std::endl;
		std::getline(std::cin, userInput);
		std::cout << "Here, the code will read the file " << filename << std::endl;
		if(file.is_open())
		{
			std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
			co_yield content;
		}else{
			std::cerr << "Error opening the file" << std::endl;
			co_yield "ERROR";
		}
	}
}

int main()
{
	char* vulnerableBuffer = (char*)malloc(10);
	std::coroutine_handle<ReturnObject::promise_type> h = readAFileCoro("randomfile").h_;
	std::cout << "Reading user input into insecure buffer (10 bytes)\n";
	std::cin.read(vulnerableBuffer, 1712);//2480
	std::cout << "Bytes read: " << vulnerableBuffer << std::endl;
	for (int i = 0; i < 2; ++i)//3 or 4
	{
		auto &promise = h.promise();
		std::cout << "Contents read from coroutine: " << promise.value_ << std::endl;
		h();
	}

	h.destroy();

	system("echo 'Hi! :D'");
}