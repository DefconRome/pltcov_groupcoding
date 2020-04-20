#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <dlfcn.h>
#include "../AFLplusplus/include/config.h"

extern uint8_t *__afl_area_ptr;
extern void __afl_manual_init(void);

/* Trampoline for the real main() */
static int (*main_orig)(int, char **, char **);

int main_hook(int argc, char **argv, char **envp)
{
    // printf("--- Before main ---\n");
    __afl_manual_init();
    int ret = main_orig(argc, argv, envp);
    // printf("--- After main ----\n");
    return ret;
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
    /* Save the real main function address */
    main_orig = main;

    /* Find the real __libc_start_main()... */
    typeof(&__libc_start_main) orig = dlsym(RTLD_NEXT, "__libc_start_main");

    /* ... and call it with our custom main function */
    return orig(main_hook, argc, argv, init, fini, rtld_fini, stack_end);
}

void pltcov__instrument(void* ret) {
    printf("%p\n", ret);
    uintptr_t cur_loc = (uintptr_t)ret;
    cur_loc = (cur_loc >> 4) ^ (cur_loc << 8);
    cur_loc &= MAP_SIZE - 1;
    __afl_area_ptr[cur_loc]++;
    return;
}