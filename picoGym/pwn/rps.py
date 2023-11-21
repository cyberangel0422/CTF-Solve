#!/usr/bin/env python
from pwn import *
r = remote("saturn.picoctf.net", 60409)

for i in range(5):
    r.sendlineafter("Type '2' to exit the program", "1")
    r.sendlineafter("(rock/paper/scissors):", "rockpaperscissors")
    success(i+1)

while(1):
    print(r.recvline())
r.close()
