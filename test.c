#include <stdio.h>

struct st{
    int st_a;
    char st_b;
};

int main() {
    char buf[1000];
    int arr[10];
    char* str = "hello";
    sprintf(buf, "%s", "12345679\0");
    int a = 1;
    int b = 666;
    struct st s;
    s.st_a = 1;
    s.st_b = 2;
    while(b > 0) {
        s.st_a++;
    }
    return 0;
}