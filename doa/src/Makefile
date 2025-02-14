CXX := g++
CXXFLAGS := -g -std=c++20 -fcf-protection=full
TARGET := fileopening
SRC := fileopening.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
