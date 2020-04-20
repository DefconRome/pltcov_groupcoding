// https://gist.github.com/apsun/1e144bf7639b22ff0097171fa0f8c6b1
#define _GNU_SOURCE


#include "../../AFLplusplus/include/config.h"
#include <stdio.h>
#include <stdint.h>

#include <stdio.h>
#include <dlfcn.h>


extern uint8_t *__afl_area_ptr;
extern uint8_t *__afl_area_ptr;
extern void __afl_manual_init(void);

/* Trampoline for the real main() */
static int (*main_orig)(int, char **, char **);

/* Our fake main() that gets called by __libc_start_main() */
int main_hook(int argc, char **argv, char **envp) {
    for (int i = 0; i < argc; ++i) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    //printf("--- Before main ---\n");
    __afl_manual_init();
    int ret = main_orig(argc, argv, envp);
    printf("--- After main ----\n");
    printf("main() returned %d\n", ret);
    return ret;
}

/*
 * Wrapper for __libc_start_main() that replaces the real main
 * function with our hooked version.
 */
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


void pltcov_log(void* retaddr) {
    printf("%p\n", retaddr);
    // shitty hash for the address we call
    //__afl_area_ptr[((uintptr_t)retaddr) % MAP_SIZE]++;
    
    uintptr_t cur_loc = (uintptr_t)retaddr;
    cur_loc = (cur_loc >> 4) ^ (cur_loc << 8);
    cur_loc &= MAP_SIZE - 1;

    __afl_area_ptr[cur_loc]++;

}