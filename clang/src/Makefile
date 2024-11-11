CXX := clang++
CXXFLAGS := -g -O3 -std=c++20 -fcf-protection=full
TARGET := clangpoc
SRC := clangpoc_1.cpp clangpoc_2.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
