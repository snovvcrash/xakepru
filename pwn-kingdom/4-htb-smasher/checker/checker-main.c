// checker-main.c

int main(int argc, char **argv) {
	if (getuid() == 0x3e9) {
		puts("[+] Welcome to file UID checker 0.1 by dzonerzy\n");

		if (argc < 2) {
			puts("Missing arguments");
		}

		else {
			filename = argv[1];
			buf_stat = malloc(0x90);

			if (stat(filename, buf_stat) == 0) {
				if (access(filename, 4) == 0) {
					char file_contents[520];

					setuid(0);
					setgid(0);
					sleep(1);
					strcpy(file_contents, ReadFile(arg1));
					printf("File UID: %d\n", (uint64_t)*(uint32_t *)((int64_t)buf_stat + 0x1c));
					printf("\nData:\n%s", (int64_t)&file_contents + 4);
				} else {
					puts("Acess failed , you don\'t have permission!");
				}
			} else {
				puts("File does not exist!");
			}
		}
		rax = 0;
	} else {
		sym.imp.puts("You\'re not \'smasher\' user please level up bro!");
		rax = 0xffffffff;
	}
	return rax;
}
