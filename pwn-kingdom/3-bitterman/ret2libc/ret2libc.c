/**
 * Buffer Overflow (64-bit). Case 2: Return-to-libc
 * Compile: gcc -g -fno-stack-protector -no-pie -o ret2libc ret2libc.c
 * ASLR: Off (sudo sh -c 'echo 0 > /proc/sys/kernel/randomize_va_space')
 */

#include <stdio.h>

void rop_gadgets() {
	asm("pop %rdi; ret");
	asm("nop; ret");
	asm("ret");
}

void vuln() {
	char buffer[100];
	gets(buffer);
}

int main(int argc, char* argv[]) {
	puts("Buffer Overflow (64-bit). Case 2: Return-to-libc\n");
	vuln();

	return 0;
}
