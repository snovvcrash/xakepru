/**
 * Buffer Overflow (64-bit). Case 1: Classic Stack Smashing
 * Compile: gcc -g -fno-stack-protector -z execstack -no-pie -o classic classic.c
 * ASLR: Off (sudo sh -c 'echo 0 > /proc/sys/kernel/randomize_va_space')
 */

#include <stdio.h>

void vuln() {
	char buffer[100];
	gets(buffer);
}

int main(int argc, char* argv[]) {
	puts("Buffer Overflow (64-bit). Case 1: Classic Stack Smashing\n");
	vuln();

	return 0;
}
