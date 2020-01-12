CC = gcc
CFLAGS = -O3
LFLAGS = -Lscheduler -lpthread

target = voror

$target: $(target).o scheduler/scheduler.o
	gcc $(target).o scheduler/scheduler.o $(LFLAGS) -o $(target)

$(target).o: $(target).c
	gcc -c $(target).c -o $(target).o $(CFLAGS)

scheduler/scheduler.o: scheduler/scheduler.c
	gcc -c scheduler/scheduler.c -o scheduler/scheduler.o $(CFLAGS)

clean:
	rm $(target) $(target).o scheduler/scheduler.o
