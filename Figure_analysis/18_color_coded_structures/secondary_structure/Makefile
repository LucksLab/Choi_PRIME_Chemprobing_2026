# Makefile for compiling get_coords with ViennaRNA (macOS, arm64)

# Compiler and flags
CXX = g++
CXXFLAGS = -arch arm64 -std=c++11
INCLUDES = -I$(CONDA_PREFIX)/include
LDFLAGS = -L$(CONDA_PREFIX)/lib -lRNA -Wl,-rpath,/usr/lib

# Output binary
TARGET = get_coords

# Source file
SRC = get_coords.cpp

# Default rule
all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET)