/**
 * Buffer Overflow (64-bit). Stage 1: Classic Stack Smashing
 * Compile: gcc -g -fno-stack-protector -z execstack -no-pie -o classic classic.c
 * ASLR: Off (sudo sh -c 'echo 0 > /proc/sys/kernel/randomize_va_space')
 */

/**
 * Buffer Overflow (64-bit). Stage 2: Return-to-libc
 * Compile: gcc -g -fno-stack-protector -no-pie -o ret2libc ret2libc.c
 * ASLR: Off (sudo sh -c 'echo 0 > /proc/sys/kernel/randomize_va_space')
 */

/**
 * Buffer Overflow (64-bit). Stage 3: Address Leak & ROP Attack
 * Compile: gcc -g -fno-stack-protector -o leak leak.c
 * ASLR: On
 */

#include <stdio.h>

void vuln() {
	char buffer[100];
	gets(buffer);
}

int main(int argc, char* argv[]) {
	puts("<NAME_OF_THE_STAGE>\n");
	vuln();

	return 0;
}
