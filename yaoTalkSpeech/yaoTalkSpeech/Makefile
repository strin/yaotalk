CXXFLAGS=-ggdb -O3 -lpthread
LIBS=-lpthread
SOURCES = $(wildcard *.cpp)
HEADS = $(wildcard *.h)
OBJS := $(SOURCES:.cpp=.o)

all: 
	g++ -std=c++0x $(CXXFLAGS) -lpthread -I . -I/usr/local/include -I/usr/local/include/sphinxbase -I/usr/local/include/pocketsphinx -c $<

clean:
		rm *.o
