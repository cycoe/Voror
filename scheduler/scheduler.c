#include <malloc.h>
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

#include "scheduler.h"

pthread_mutex_t mutex;

// Create a Scheduler
Scheduler *create_scheduler(unsigned num_task) {
  Scheduler *scheduler = (Scheduler *)malloc(sizeof(Scheduler));
  scheduler->num_task = num_task;
  scheduler->num_done = 0;

  return scheduler;
}

// Destroy the scheduler memory
void destroy_scheduler(Scheduler **sch_ptr) {
  free(*sch_ptr);
  *sch_ptr = NULL;
}

// Get the current task id
int get_task_id(Scheduler *scheduler) {
  pthread_t thread_id = pthread_self();
  // add lock
  if (pthread_mutex_lock(&mutex) != 0) {
    fprintf(stderr, "[Thread %lu] Lock error!\n", thread_id);
    pthread_mutex_unlock(&mutex);
    return LOCK_FAILED;
  }

  // get the current id
  unsigned task_id = scheduler->num_done++;
  // release lock
  pthread_mutex_unlock(&mutex);

  return task_id < scheduler->num_task ? task_id : EMPTY;
}

// The child thread function
void *thread(void *thread_argv) {
  // func is a wrapper that just need a task id as parameter
  int task_id = EMPTY;
  pthread_t thread_id = pthread_self();
  ThreadArgv *argv = (ThreadArgv *)thread_argv;

  while ((task_id = get_task_id(argv->scheduler)) != EMPTY) {
    if (task_id == LOCK_FAILED) {
      continue;
    }

    fprintf(stdout, "[Thread %lu] Start to process task %d...\n", thread_id,
            task_id);
    if (argv->func(&task_id, argv->argv) != 0)
      fprintf(stderr, "[Thread %lu] task %d failed!\n", thread_id, task_id);
  }

  return NULL;
}

int run_tasks(int func(int *task_id, void *argv), void *argv, unsigned num_task,
              unsigned num_thread) {
  // init mutex lock
  if (pthread_mutex_init(&mutex, NULL) != 0) {
    fprintf(stderr, "Mutex lock initiation failed!\n");
    pthread_mutex_destroy(&mutex);
    return 127;
  }

  // create scheduler
  Scheduler *scheduler = create_scheduler(num_task);
  // create the threads pool to store all thread pointers
  pthread_t *thread_pool = (pthread_t *)malloc(sizeof(pthread_t) * num_thread);
  // create the argv structure for thread function
  ThreadArgv thread_argv;
  thread_argv.func = func;
  thread_argv.argv = argv;
  thread_argv.scheduler = scheduler;

  // create all threads
  for (int thread_id = 0; thread_id < num_thread; thread_id++) {
    if (pthread_create(thread_pool + thread_id, NULL, thread, &thread_argv) !=
        0) {
      return 127;
    }
  }

  // the main thread wait all child threads to quit
  for (int thread_id = 0; thread_id < num_thread; thread_id++) {
    pthread_join(thread_pool[thread_id], NULL);
  }

  // destroy objects
  destroy_scheduler(&scheduler);
  pthread_mutex_destroy(&mutex);
  free(thread_pool);
  return 0;
}
