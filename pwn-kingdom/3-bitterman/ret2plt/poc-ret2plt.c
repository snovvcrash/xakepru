#include <stdio.h>

int main(int argc, char* argv[]) {
	char addr[16];
	sprintf(addr, "%p", &puts);
	puts(addr);

	return 0;
}
