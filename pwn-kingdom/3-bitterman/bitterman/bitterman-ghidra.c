// Compile: gcc -g -fno-stack-protector -no-pie -o bitterman-ghidra bitterman-ghidra.c

#include <stdio.h>
#include <unistd.h>

int read_nbytes(char *dst, size_t nbytes) {
  int iVar1;
  ssize_t sVar2;
  long lVar3;
  int i;

  i = 0;
  while (1) {
    if (nbytes <= (long)(long)i)
      return i;

    sVar2 = read(0, dst + i, 1);
    if (sVar2 == 0) break;
    iVar1 = i + 1;
    lVar3 = (long)i;
    i = iVar1;
    if (dst[lVar3] == '\n')
      return iVar1;
  }

  return i;
}

int main(int argc,char **argv) {
  int iVar1;
  size_t nbytes;
  char buf [64];
  char username [64];
  size_t size;

  puts("> What\'s your name? ");
  fflush(stdout);
  read_nbytes(username, 0x40);
  printf("Hi, %s\n", username);

  puts("> Please input the length of your message: ");
  fflush(stdout);
  scanf("%llu",&nbytes);

  puts("> Please enter your text: ");
  fflush(stdout);
  iVar1 = read_nbytes(buf, nbytes);  // <-- УЯЗВИМЫЙ КОД
  if (iVar1 != 0) {
    puts("> Thanks!");
    fflush(stdout);
  }

  return 0;
}
