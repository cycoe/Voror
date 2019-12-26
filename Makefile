CC = gcc
CFLAGS = -O3

target = voror

$(target): $(target).c
	$(CC) $(target).c -o $(target) $(CFLAGS)

clean:
	rm $(target)
