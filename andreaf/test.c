#include <stdio.h>
#include <unistd.h>

int main() {

  char buf[2] = {'a', 0};

  read(0, buf, 2);
  
  if (buf[0] == '0')
    return 1;
  
  return 0;

}
