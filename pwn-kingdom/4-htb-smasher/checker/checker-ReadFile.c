// checker-ReadFile.c

int64_t sym.ReadFile(char *arg1)
{
    int32_t iVar1;
    int32_t iVar2;
    int64_t iVar3;
    int64_t ptr;
    
    ptr = 0;
    iVar3 = sym.imp.fopen(arg1, 0x400c68);
    if (iVar3 != 0) {
        sym.imp.fseek(iVar3, 0, 2);
        iVar1 = sym.imp.ftell(iVar3);
        sym.imp.rewind(iVar3);
        ptr = sym.imp.malloc((int64_t)(iVar1 + 1));
        iVar2 = sym.imp.fread(ptr, 1, (int64_t)iVar1, iVar3);
        *(undefined *)(ptr + iVar1) = 0;
        if (iVar1 != iVar2) {
            sym.imp.free(ptr);
            ptr = 0;
        }
        sym.imp.fclose(iVar3);
    }
    return ptr;
}
