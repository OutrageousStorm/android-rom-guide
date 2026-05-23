CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = rom-flasher

all: $(TARGET)

$(TARGET): rom-flasher.c
	$(CC) $(CFLAGS) -o $(TARGET) rom-flasher.c

clean:
	rm -f $(TARGET)

install: $(TARGET)
	install -D $(TARGET) /usr/local/bin/$(TARGET)

.PHONY: all clean install
