#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <dlfcn.h>
#include "../AFLplusplus/include/config.h"

extern void __afl_manual_init(void);

extern uint8_t *__afl_area_ptr;

void __pltcov_log(void* retaddr) {

  uintptr_t cur_loc = (uintptr_t)retaddr;
  cur_loc = (cur_loc >> 4) ^ (cur_loc << 8);
  cur_loc &= MAP_SIZE - 1;

  printf("called from %lx\n", cur_loc);

  __afl_area_ptr[cur_loc]++;

}

static int (*real_main)(int, char **, char **);

static int libcov_main(int argc, char** argv, char** env) {

  __afl_manual_init();

  return real_main(argc, argv, env);

}

int __libc_start_main(
    int (*main)(int, char **, char **),
    int argc,
    char **argv,
    int (*init)(int, char **, char **),
    void (*fini)(void),
    void (*rtld_fini)(void),
    void *stack_end) {

    typeof(&__libc_start_main) orig = dlsym(RTLD_NEXT, "__libc_start_main");
    real_main = main;

    return orig(main, argc, argv, init, fini, rtld_fini, stack_end);
}
