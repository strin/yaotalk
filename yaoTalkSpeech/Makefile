CXXFLAGS=-ggdb -O3 -lpthread
LIBS=-lpthread
SOURCES = $(wildcard *.cpp utils/*.cpp)
HEADS = $(wildcard *.h utils/*.h)
OBJS := $(SOURCES:.cpp=.o)

all: yaoTalkSpeech

yaoTalkSpeech/%.o: 
		make -C utils/

%.o: %.cpp $(HEADS)
		g++ -std=c++0x $(CXXFLAGS) -lpthread -I . -I/usr/local/include -I/usr/local/include/sphinxbase -I/usr/local/include/pocketsphinx -c $<

yaoTalkSpeech: $(OBJS)
		g++ -o yaoTalkSpeech $(OBJS) $(CXXFLAGS) -lpthread -L/usr/local/Cellar/portaudio/19.20111121/lib -libportaudio

clean:
		rm *.o
		rm utils/*.o
