/**
 * :файл: overflow.c
 * :компиляция: gcc -g -Wall -Werror -O0 -m32 -fno-stack-protector -z execstack -no-pie -Wl,-z,norelro -mpreferred-stack-boundary=2 -o overflow overflow.c
 * :запуск: ./overflow <СТРОКА>
 */

#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
	char buf[128];               // 128-байтный массив типа char
	strcpy(buf, argv[1]);        // копирование первого аргумента в массив buf
	printf("Input: %s\n", buf);  // вывод содержимого буфера на экран

	return 0;
}
