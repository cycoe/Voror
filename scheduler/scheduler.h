#define EMPTY -1
#define LOCK_FAILED -2

// Scheduler to manage the tasks
typedef struct Scheduler {
  unsigned num_task;
  unsigned num_done;
} Scheduler;

typedef struct ThreadArgv {
  int (*func)(int *task_id, void *argv);
  void *argv;
  Scheduler *scheduler;
} ThreadArgv;

int run_tasks(int func(int *task_id, void *argv), void *argv, unsigned num_task,
              unsigned num_thread);
