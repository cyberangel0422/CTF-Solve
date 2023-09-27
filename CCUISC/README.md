# CCUISC CTF

## ret2libc
- something went wrong with pwnlib.elf so it can't obtain the correct address of puts@plt

the result from `pwnlib.elf` :

```python
>>> from pwn import *
>>> e=ELF('./chal')
[!] Could not populate PLT: invalid syntax (unicorn.py, line 110)
[*] '/home/ethan/workspace/ctf-solve/CCUISC/ret2libc/chal'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
>>> e.symbols['puts']
4210712
>>> hex(e.symbols['puts'])
'0x404018'
```

however if we track the address in gdb :

```asm
pwndbg> x/30i *0x404018
   0x401030:    endbr64
   0x401034:    push   0x0
   0x401039:    bnd jmp 0x401020
   0x40103f:    nop
   0x401040:    endbr64
   0x401044:    push   0x1
   0x401049:    bnd jmp 0x401020
   0x40104f:    nop
   0x401050:    endbr64
   0x401054:    push   0x2
   0x401059:    bnd jmp 0x401020
   0x40105f:    nop
   0x401060 <puts@plt>: endbr64
   0x401064 <puts@plt+4>:       bnd jmp QWORD PTR [rip+0x2fad]        # 0x404018 <puts@got.plt>
   0x40106b <puts@plt+11>:      nop    DWORD PTR [rax+rax*1+0x0]
   0x401070 <gets@plt>: endbr64
   0x401074 <gets@plt+4>:       bnd jmp QWORD PTR [rip+0x2fa5]        # 0x404020 <gets@got.plt>
   0x40107b <gets@plt+11>:      nop    DWORD PTR [rax+rax*1+0x0]

(skipping...)
```

the real entry of puts@plt is `0x401060`

- also for avoiding hitting segfault when calling `system` cause by `MOVAPS`, add one more extra `ret` before calling
