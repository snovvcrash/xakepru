/**
 * Buffer Overflow (64-bit). Case 3: Return-to-PLT
 * Compile: gcc -g -fno-stack-protector -no-pie -o ret2plt ret2plt.c
 * ASLR: On
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
	puts("Buffer Overflow (64-bit). Case 3: Return-to-PLT\n");
	vuln();

	return 0;
}
