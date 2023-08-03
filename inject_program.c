#include <stdio.h>
#include <stdlib.h>
#include <string.h>
__attribute__((constructor))
void inject()
{
  // @read str
  // @read arr
  // @read st
  int x = 1;
  // b = a + x;
  // char buf[100];
  // FILE* fp = fopen("/root/aoptrace/AOP-GDB/tmp", "a");
  // fwrite(query_string, sizeof(char), strlen(query_string), fp);
  // fclsoe(fp);
}
