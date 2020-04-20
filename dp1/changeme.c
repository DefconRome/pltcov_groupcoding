#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char s[128];
    scanf("%127s", s);
    if(!strcmp(s, "secretflag"))
        puts("Win");
}
