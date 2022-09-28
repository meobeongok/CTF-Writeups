#include <unistd.h>

void main(void)
{
  char buff[20];
  read(0, buff, 0x90);
}
