#define _GNU_SOURCE

#include <stdio.h>
#include <stdint.h>
#include <dlfcn.h>

#include "../AFLplusplus/include/config.h"


extern uint8_t *__afl_area_ptr;
extern void __afl_manual_init(void);


void __pltcov_logger(void* ret_addr) 
{
        uintptr_t cur_loc = (uintptr_t)ret_addr;
        cur_loc = (cur_loc >> 4) ^ (cur_loc << 8);
        cur_loc &= MAP_SIZE - 1;
        __afl_area_ptr[cur_loc]++;
}



static int (*main_orig)(int, char**, char**);

int main_hook(int argc, char **argv, char **envp) 
{
        __afl_manual_init();
        int ret = main_orig(argc, argv, envp);
}

int __libc_start_main(
    int (*main)(int, char **, char **),
    int argc,
    char **argv,
    int (*init)(int, char **, char **),
    void (*fini)(void),
    void (*rtld_fini)(void),
    void *stack_end)
{
    main_orig = main;

    typeof(&__libc_start_main) orig = dlsym(RTLD_NEXT, "__libc_start_main");

    return orig(main_hook, argc, argv, init, fini, rtld_fini, stack_end);
}
