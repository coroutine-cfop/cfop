CXX := g++
CXXFLAGS := -g -O3 -std=c++20 -fcf-protection=full
TARGET := gccpoc
SRC := gccpoc_1.cpp gccpoc_2.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
